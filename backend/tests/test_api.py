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


def trigger_scrape(client: TestClient, *, providers: list[str] | None = None) -> dict:
    payload = {"providers": providers} if providers is not None else None
    response = client.post("/scrape", headers={"x-api-key": "test-key"}, json=payload)
    assert response.status_code == 202
    return response.json()


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
    scrape_result = trigger_scrape(client)
    assert scrape_result["status"] == "queued"
    assert scrape_result["results"]

    providers_response = client.get("/providers")
    assert providers_response.status_code == 200
    providers = providers_response.json()
    provider_lookup = {provider["id"]: provider["slug"] for provider in providers}

    plans_response = client.get("/plans")
    assert plans_response.status_code == 200
    plans = plans_response.json()
    assert plans
    assert {plan["provider_id"] for plan in plans}


def test_plan_detail_endpoint(client):
    trigger_scrape(client)

    plans = client.get("/plans").json()
    plan = plans[0]
    plan_id = plan["id"]

    detail_response = client.get(f"/plans/{plan_id}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["id"] == plan_id
    assert detail["provider_id"] == plan["provider_id"]
    assert detail["name"] == plan["name"]


def test_providers_endpoint_returns_data(client):
    trigger_scrape(client)

    providers_response = client.get("/providers")
    assert providers_response.status_code == 200
    providers = providers_response.json()
    assert providers
    assert {provider["slug"] for provider in providers}
    for provider in providers:
        assert provider["plans"]
        assert all(plan["provider_id"] == provider["id"] for plan in provider["plans"])


def test_scrape_rejects_empty_provider_list(client):
    response = client.post(
        "/scrape",
        headers={"x-api-key": "test-key"},
        json={"providers": []},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No providers requested"


def test_scrape_rejects_unknown_provider(client):
    response = client.post(
        "/scrape",
        headers={"x-api-key": "test-key"},
        json={"providers": ["unknown"]},
    )
    assert response.status_code == 400
    assert "Unknown provider slug" in response.json()["detail"]
    assert any("estimated_savings_vs_txu" in plan for plan in plans)

    txu_provider_id = next(
        (provider_id for provider_id, slug in provider_lookup.items() if slug == "txu"),
        None,
    )
    assert txu_provider_id is not None



def test_benchmark_against_txu_positive_for_cheaper_plan():
    from backend.routes import plans as plan_routes
    from backend import models

    usage = plan_routes.BENCHMARK_USAGE_KWH
    txu_plan = models.Plan(
        provider_id=1,
        name="TXU Benchmark",
        term_months=12,
        rate_cents_kwh=15.0,
        base_fee=10.0,
    )
    competitor = models.Plan(
        provider_id=2,
        name="Better Rate",
        term_months=12,
        rate_cents_kwh=10.0,
        base_fee=5.0,
    )

    savings = plan_routes._benchmark_against_txu(competitor, txu_plan, usage)
    assert savings is not None
    assert savings > 0
