"""Rate limit tests for /api/contact (slowapi 5/hour, key_func=real_client_ip).

IMPORTANT: run this LAST and restart the backend before running
(`sudo supervisorctl restart backend`) because the limiter uses in-memory storage.

Run serially: pytest tests/test_rate_limit.py -n 0
"""
import uuid

import pytest

IP_A = "1.2.3.4"
IP_B = "5.6.7.8"
EXPECTED_MSG = "Hai inviato troppi messaggi. Riprova tra qualche minuto."


def _payload(i):
    marker = uuid.uuid4().hex[:8]
    return {
        "name": f"TEST_RL_{i}",
        "email": f"test_rl_{marker}@example.com",
        "message": f"TEST_RATELIMIT_{marker} messaggio numero {i}",
    }


class TestRateLimitPerIP:
    """Bucket separation via X-Forwarded-For (real_client_ip key_func)."""

    def test_sixth_request_from_same_xff_returns_429(self, api_client, base_url):
        statuses = []
        last = None
        for i in range(6):
            last = api_client.post(
                f"{base_url}/api/contact",
                json=_payload(i),
                headers={"X-Forwarded-For": IP_A},
            )
            statuses.append(last.status_code)
        assert statuses[:5] == [200] * 5, f"first 5 must be 200, got {statuses}"
        assert statuses[5] == 429, f"6th must be 429, got {statuses}"

    def test_429_body_is_json_detail(self, api_client, base_url):
        # bucket for IP_A is already exhausted by the previous test
        r = api_client.post(
            f"{base_url}/api/contact",
            json=_payload(99),
            headers={"X-Forwarded-For": IP_A},
        )
        assert r.status_code == 429, r.text[:300]
        assert "application/json" in r.headers.get("content-type", ""), r.headers
        body = r.json()
        assert body == {"detail": EXPECTED_MSG}, body

    def test_different_xff_has_its_own_bucket(self, api_client, base_url):
        """IP_B must still get 200 for its own first 5 requests."""
        statuses = []
        for i in range(5):
            r = api_client.post(
                f"{base_url}/api/contact",
                json=_payload(i),
                headers={"X-Forwarded-For": IP_B},
            )
            statuses.append(r.status_code)
        assert statuses == [200] * 5, f"IP_B bucket appears shared with IP_A: {statuses}"

        # and IP_A is still blocked at the same time
        blocked = api_client.post(
            f"{base_url}/api/contact",
            json=_payload(100),
            headers={"X-Forwarded-For": IP_A},
        )
        assert blocked.status_code == 429, blocked.text[:300]

        # 6th for IP_B -> 429
        sixth = api_client.post(
            f"{base_url}/api/contact",
            json=_payload(6),
            headers={"X-Forwarded-For": IP_B},
        )
        assert sixth.status_code == 429, sixth.text[:300]
        assert sixth.json() == {"detail": EXPECTED_MSG}

    def test_health_not_rate_limited(self, api_client, base_url):
        for _ in range(8):
            r = api_client.get(f"{base_url}/api/health", headers={"X-Forwarded-For": IP_A})
            assert r.status_code == 200, r.text[:200]


class TestRateLimitRegression:
    """Honeypot + valid submit still work on a fresh bucket."""

    def test_honeypot_still_fake_200_no_db_save(self, api_client, base_url):
        from pymongo import MongoClient
        import os
        from dotenv import dotenv_values

        env = dotenv_values("/app/backend/.env")
        mc = MongoClient(os.environ.get("MONGO_URL") or env["MONGO_URL"])
        coll = mc[os.environ.get("DB_NAME") or env["DB_NAME"]].contacts

        marker = uuid.uuid4().hex[:10]
        payload = {
            "name": "TEST_HONEYPOT",
            "email": f"test_hp_{marker}@example.com",
            "message": f"TEST_HONEYPOT_{marker} messaggio bot",
            "website": "http://spam.example.com",
        }
        r = api_client.post(
            f"{base_url}/api/contact", json=payload,
            headers={"X-Forwarded-For": "9.9.9.9"},
        )
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert isinstance(data["id"], str) and len(data["id"]) == 36
        assert coll.count_documents({"email": payload["email"]}) == 0
        assert coll.count_documents({"id": data["id"]}) == 0
        mc.close()

    def test_valid_submit_200_and_persisted(self, api_client, base_url):
        from pymongo import MongoClient
        import os
        from dotenv import dotenv_values

        env = dotenv_values("/app/backend/.env")
        mc = MongoClient(os.environ.get("MONGO_URL") or env["MONGO_URL"])
        coll = mc[os.environ.get("DB_NAME") or env["DB_NAME"]].contacts

        marker = uuid.uuid4().hex[:10]
        payload = {
            "name": "TEST_VALID",
            "email": f"test_valid_{marker}@example.com",
            "organization": "TEST_Scuola",
            "role": "TEST_Docente",
            "message": f"TEST_VALID_{marker} vorrei collaborare con voi",
        }
        r = api_client.post(
            f"{base_url}/api/contact", json=payload,
            headers={"X-Forwarded-For": "9.9.9.10"},
        )
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert set(data.keys()) == {"id", "created_at"}
        doc = coll.find_one({"id": data["id"]})
        assert doc is not None
        assert doc["name"] == payload["name"]
        assert doc["email"] == payload["email"]
        assert doc["organization"] == payload["organization"]
        assert "website" not in doc
        mc.close()


class TestStaticAssets:
    def test_og_image_svg_served(self, api_client, base_url):
        r = api_client.get(f"{base_url}/og-image.svg")
        assert r.status_code == 200, r.text[:200]
        assert "image/svg+xml" in r.headers.get("content-type", ""), r.headers.get("content-type")
        assert "<svg" in r.text[:500].lower(), r.text[:200]

    def test_privacy_page_loads(self, api_client, base_url):
        r = api_client.get(f"{base_url}/privacy")
        assert r.status_code == 200, r.text[:200]
        assert "text/html" in r.headers.get("content-type", "")
