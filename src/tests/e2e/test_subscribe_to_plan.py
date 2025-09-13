from typing import Dict
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.infra.api import app, get_payment_gateway
from src.infra.db.repository import SQLModelSubscriptionRepository
from src.infra.payment import FakePaymentGateway


@pytest.fixture
def account_payload() -> Dict:
    """
    Fixture for creating a account payload.
    """

    return {
        "name": "Higor Cruz",
        "email": "higorrsc@gmail.com",
        "password": "password123",
        "billing_address": {
            "street": "CSB10",
            "city": "Brasilia",
            "state": "DF",
            "zip_code": "72015",
            "country": "BR",
        },
    }


@pytest.fixture
def plan_payload() -> Dict:
    """
    Fixture for creating a plan payload.
    """

    return {
        "name": "Standard",
        "price": {
            "amount": "10.00",
            "currency": "USD",
        },
    }


@pytest.fixture
def plan_id(client: TestClient, plan_payload: Dict) -> str:
    """
    Fixture for creating a plan.
    """

    response = client.post("/plans", json=plan_payload)
    assert response.status_code == 201

    return response.json()["id"]


@pytest.fixture
def user_id(client: TestClient, account_payload: Dict) -> str:
    """
    Fixture for creating a user.
    """
    response = client.post("/accounts", json=account_payload)
    assert response.status_code == 201

    return response.json()["user_id"]


@pytest.fixture
def subscription_payload(user_id: str, plan_id: str) -> Dict:
    """
    Fixture for creating a subscription payload.
    """

    return {
        "user_id": user_id,
        "plan_id": plan_id,
        "payment_token": "tok_visa",
    }


class TestSubscribeToPlanAPIRoute:
    """
    Test for API Route
    """

    def test_subscribe_to_plan_success(
        self,
        client: TestClient,
        subscription_payload: Dict,
        session: Session,
    ) -> None:
        """
        Test subscribe to a plan
        """

        response = client.post(
            "/subscriptions",
            json=subscription_payload,
        )

        assert response.status_code == 201

        data = response.json()
        assert data["subscription_id"] is not None

        repo = SQLModelSubscriptionRepository(session)
        subscription = repo.get_by_id(UUID(data["subscription_id"]))
        assert subscription is not None
        assert str(subscription.user_id) == subscription_payload["user_id"]
        assert str(subscription.plan_id) == subscription_payload["plan_id"]
        assert subscription.is_trial is False
        assert subscription.status == "ACTIVE"

    def test_subscribe_to_plan_failure_create_trial_subscription(
        self,
        client: TestClient,
        subscription_payload: Dict,
        session: Session,
    ) -> None:
        """
        Test subscribe to a plan
        """

        app.dependency_overrides[get_payment_gateway] = lambda: FakePaymentGateway(
            success=False
        )

        response = client.post(
            "/subscriptions",
            json=subscription_payload,
        )

        assert response.status_code == 201

        data = response.json()
        assert data["subscription_id"] is not None

        repo = SQLModelSubscriptionRepository(session)
        subscription = repo.get_by_id(UUID(data["subscription_id"]))
        assert subscription is not None
        assert str(subscription.user_id) == subscription_payload["user_id"]
        assert str(subscription.plan_id) == subscription_payload["plan_id"]
        assert subscription.is_trial is True
        assert subscription.status == "ACTIVE"

    def test_subscribe_to_plan_already_subscribed(
        self,
        client: TestClient,
        subscription_payload: Dict,
    ) -> None:
        """
        Test subscribe to a plan when already subscribed
        """

        response = client.post(
            "/subscriptions",
            json=subscription_payload,
        )

        assert response.status_code == 201

        response = client.post(
            "/subscriptions",
            json=subscription_payload,
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "User already has active subscription"

    def test_subscribe_to_plan_invalid_user_id(
        self,
        client: TestClient,
        subscription_payload: Dict,
    ) -> None:
        """
        Test subscribe to a plan with an invalid user id
        """

        subscription_payload["user_id"] = "invalid_user_id"

        response = client.post(
            "/subscriptions",
            json=subscription_payload,
        )

        assert response.status_code == 422
        assert "invalid character" in response.json()["detail"][0]["msg"]
