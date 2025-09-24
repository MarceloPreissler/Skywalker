import asyncio
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.config import get_settings
from backend.main import app
from backend.scrapers.runner import initialize_database

TEST_DB_PATH = Path("test_api.db")


@pytest.fixture(scope="session", autouse=True)
def configure_env():
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH}"
    os.environ["SCHEDULER_ENABLED"] = "false"
    os.environ["API_KEY"] = "test-key"
    # reset cached settings
    get_settings.cache_clear()  # type: ignore[attr-defined]
    yield
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    asyncio.get_event_loop().run_until_complete(initialize_database())


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_scrape_endpoint_requires_api_key(client):
    response = client.post("/scrape")
    assert response.status_code == 422  # missing header

    response = client.post("/scrape", headers={"x-api-key": "wrong"})
    assert response.status_code == 401


def test_scrape_and_fetch_plans(client):
    response = client.post("/scrape", headers={"x-api-key": "test-key"})
    assert response.status_code == 202

    plans_response = client.get("/plans")
    assert plans_response.status_code == 200
    plans = plans_response.json()
    assert plans
    assert {plan["provider_id"] for plan in plans}
