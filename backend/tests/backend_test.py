"""Backend API regression tests for Spazio Sicuro (health, contact, downloads)."""
import re
import uuid

import pytest
import requests


# ---------- Health / root ----------
class TestHealth:
    def test_root(self, api_client, base_url):
        r = api_client.get(f"{base_url}/api/")
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert data["service"] == "Spazio Sicuro"
        assert data["status"] == "ok"

    def test_health(self, api_client, base_url):
        r = api_client.get(f"{base_url}/api/health")
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert data["status"] == "healthy"
        assert isinstance(data["time"], str) and len(data["time"]) > 0


# ---------- Contact endpoint ----------
class TestContact:
    def test_create_contact_valid(self, api_client, base_url):
        payload = {
            "name": "TEST_QA",
            "email": f"test_qa_{uuid.uuid4().hex[:8]}@example.com",
            "organization": "TEST_Scuola",
            "role": "TEST_docente",
            "message": "Messaggio di test automatico per verificare il salvataggio.",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        assert isinstance(data["id"], str)
        # id must be a valid uuid
        uuid.UUID(data["id"])
        assert isinstance(data["created_at"], str)
        assert re.match(r"^\d{4}-\d{2}-\d{2}T", data["created_at"]), data["created_at"]
        assert "_id" not in data

    def test_create_contact_minimal_optional_fields_omitted(self, api_client, base_url):
        payload = {
            "name": "TEST_Minimal",
            "email": f"test_min_{uuid.uuid4().hex[:8]}@example.com",
            "message": "Ciao mondo test",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]
        assert "id" in r.json()

    def test_contact_empty_optional_strings_accepted(self, api_client, base_url):
        """Frontend always sends organization/role as empty strings."""
        payload = {
            "name": "TEST_EmptyOpt",
            "email": f"test_eo_{uuid.uuid4().hex[:8]}@example.com",
            "organization": "",
            "role": "",
            "message": "Messaggio abbastanza lungo",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]

    @pytest.mark.parametrize(
        "payload,label",
        [
            ({"name": "", "email": "a@b.com", "message": "hello world"}, "empty name"),
            ({"name": "X", "email": "not-an-email", "message": "hello world"}, "bad email"),
            ({"name": "X", "email": "a@b.com", "message": "hi"}, "short message"),
            ({"email": "a@b.com", "message": "hello world"}, "missing name"),
            ({"name": "X", "message": "hello world"}, "missing email"),
            ({"name": "X", "email": "a@b.com"}, "missing message"),
        ],
    )
    def test_contact_validation_errors(self, api_client, base_url, payload, label):
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 422, f"{label}: expected 422, got {r.status_code} {r.text[:200]}"
        assert "detail" in r.json()


# ---------- Downloads ----------
class TestDownloads:
    @pytest.mark.parametrize(
        "key,expected_type,expected_name",
        [
            ("basic", "application/zip", "spazio-sicuro-basic.zip"),
            ("full-app", "application/zip", "spazio-sicuro-full-app.zip"),
            ("pdf", "application/pdf", "spazio-sicuro-presentazione.pdf"),
            ("pdf-full", "application/pdf", "spazio-sicuro-presentazione-full.pdf"),
        ],
    )
    def test_download_ok(self, base_url, key, expected_type, expected_name):
        r = requests.get(f"{base_url}/api/downloads/{key}", timeout=60)
        assert r.status_code == 200, r.text[:200]
        assert expected_type in r.headers.get("content-type", "")
        assert expected_name in r.headers.get("content-disposition", "")
        assert len(r.content) > 1000
        if expected_type == "application/zip":
            assert r.content[:2] == b"PK"
        else:
            assert r.content[:4] == b"%PDF"

    def test_download_invalid_key(self, base_url):
        r = requests.get(f"{base_url}/api/downloads/invalid", timeout=30)
        assert r.status_code == 404, r.text[:200]
        assert r.json()["detail"] == "File non trovato"
