"""Backend API regression tests for Spazio Sicuro (health, contact, honeypot, downloads).

NOTE: /api/contact is rate limited to 5/hour per IP (slowapi, in-memory).
This module intentionally performs at most 4 POSTs that reach the endpoint.
Rate limiting itself is covered in test_rate_limit.py (run separately after a backend restart).
"""
import os
import re
import uuid

import pytest
import requests
from dotenv import dotenv_values
from pymongo import MongoClient


BACKEND_ENV = dotenv_values("/app/backend/.env")


@pytest.fixture(scope="module")
def mongo_db():
    mongo_url = os.environ.get("MONGO_URL") or BACKEND_ENV.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME") or BACKEND_ENV.get("DB_NAME")
    client = MongoClient(mongo_url)
    yield client[db_name]
    client.close()


# ---------- Health / root / lifespan ----------
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

    def test_lifespan_startup_logged(self):
        """lifespan replaced @app.on_event: startup message must appear in supervisor logs."""
        found = False
        for path in ("/var/log/supervisor/backend.err.log", "/var/log/supervisor/backend.out.log"):
            if os.path.exists(path):
                with open(path, "r", errors="ignore") as fh:
                    if "Spazio Sicuro API — startup" in fh.read():
                        found = True
        assert found, "lifespan startup log message not found in backend supervisor logs"


# ---------- Contact endpoint (valid + persistence) ----------
class TestContact:
    def test_create_contact_valid_and_persisted(self, api_client, base_url, mongo_db):
        marker = uuid.uuid4().hex[:10]
        payload = {
            "name": "TEST_QA",
            "email": f"test_qa_{marker}@example.com",
            "organization": "TEST_Scuola",
            "role": "TEST_docente",
            "message": f"Messaggio di test automatico {marker}",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        uuid.UUID(data["id"])
        assert re.match(r"^\d{4}-\d{2}-\d{2}T", data["created_at"]), data["created_at"]
        assert "_id" not in data

        doc = mongo_db.contacts.find_one({"id": data["id"]})
        assert doc is not None, "contact not persisted in MongoDB"
        assert doc["name"] == payload["name"]
        assert doc["email"] == payload["email"]
        assert doc["organization"] == payload["organization"]
        assert doc["role"] == payload["role"]
        assert doc["message"] == payload["message"]

    def test_create_contact_minimal_optional_fields_omitted(self, api_client, base_url):
        payload = {
            "name": "TEST_Minimal",
            "email": f"test_min_{uuid.uuid4().hex[:8]}@example.com",
            "message": "Ciao mondo test",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]
        assert "id" in r.json()

    # ---------- Honeypot ----------
    def test_honeypot_returns_fake_success_and_does_not_persist(self, api_client, base_url, mongo_db):
        marker = uuid.uuid4().hex[:12]
        payload = {
            "name": "TEST_Bot",
            "email": f"test_bot_{marker}@example.com",
            "message": f"TEST_HONEYPOT_{marker} messaggio bot",
            "website": "http://spam.example.com",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]
        data = r.json()
        uuid.UUID(data["id"])  # fake but valid uuid
        assert re.match(r"^\d{4}-\d{2}-\d{2}T", data["created_at"])

        assert mongo_db.contacts.count_documents({"message": payload["message"]}) == 0
        assert mongo_db.contacts.count_documents({"id": data["id"]}) == 0
        assert mongo_db.contacts.count_documents({"email": payload["email"]}) == 0

    def test_website_field_never_stored_when_empty_string(self, api_client, base_url, mongo_db):
        marker = uuid.uuid4().hex[:12]
        payload = {
            "name": "TEST_EmptyHoneypot",
            "email": f"test_eh_{marker}@example.com",
            "organization": "",
            "role": "",
            "message": f"TEST_EMPTYHP_{marker} messaggio umano",
            "website": "",
        }
        r = api_client.post(f"{base_url}/api/contact", json=payload)
        assert r.status_code == 200, r.text[:300]
        doc = mongo_db.contacts.find_one({"id": r.json()["id"]})
        assert doc is not None, "empty honeypot must be treated as human and persisted"
        assert "website" not in doc

    # ---------- Validation (422 - does not consume rate limit quota) ----------
    @pytest.mark.parametrize(
        "payload,label",
        [
            ({"name": "", "email": "a@b.com", "message": "hello world"}, "empty name"),
            ({"name": "X", "email": "not-an-email", "message": "hello world"}, "bad email"),
            ({"name": "X", "email": "a@b.com", "message": "hi"}, "short message"),
            ({"name": "X", "email": "a@b.com", "message": ""}, "empty message"),
            ({"email": "a@b.com", "message": "hello world"}, "missing name"),
            ({"name": "X", "message": "hello world"}, "missing email"),
            ({"name": "X", "email": "a@b.com"}, "missing message"),
            ({"name": "X", "email": "a@b.com", "message": "x" * 4001}, "message too long"),
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

    @pytest.mark.parametrize("key", ["invalid", "tool", "BASIC", "pdf%20", "../server.py"])
    def test_download_invalid_key(self, base_url, key):
        r = requests.get(f"{base_url}/api/downloads/{key}", timeout=30)
        assert r.status_code == 404, f"{key}: {r.status_code} {r.text[:200]}"


# ---------- Removed public asset ----------
class TestRemovedTool:
    def test_tool_html_not_served_as_static(self, base_url):
        """/public/tool.html was removed; SPA fallback may return index.html but never the old tool page."""
        r = requests.get(f"{base_url}/tool.html", timeout=30)
        assert r.status_code in (200, 404)
        if r.status_code == 200:
            assert "<div id=\"root\">" in r.text, "tool.html still served as a standalone page"
