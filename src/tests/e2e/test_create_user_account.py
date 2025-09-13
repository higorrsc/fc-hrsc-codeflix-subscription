from typing import Dict

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def valid_payload() -> Dict:
    """
    Fixture for creating a valid payload.
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


class TestCreateUserAccountAPIRoute:
    """
    Test create a new user account API route.
    """

    def test_create_user_account_success(
        self,
        client: TestClient,
        valid_payload: Dict,
    ) -> None:
        """
        Test create a new user account
        """

        response = client.post(
            "/accounts",
            json=valid_payload,
        )

        assert response.status_code == 201
        assert response.json()["user_id"] is not None
        assert response.json()["iam_user_id"] is not None

    def test_create_user_account_duplicated_email(
        self, client: TestClient, valid_payload: Dict
    ) -> None:
        """
        Test create a new user account with duplicated email
        """

        response = client.post(
            "/accounts",
            json=valid_payload,
        )

        assert response.status_code == 201

        response = client.post(
            "/accounts",
            json=valid_payload,
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Email is already registered"

    def test_create_user_account_invalid_data(
        self, client: TestClient, valid_payload: Dict
    ) -> None:
        """
        Test create a new user account with invalid data
        """

        valid_payload["email"] = ""

        response = client.post(
            "/accounts",
            json=valid_payload,
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "value is not a valid email address: An email address must have an @-sign."
        )
