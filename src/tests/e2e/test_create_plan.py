from fastapi.testclient import TestClient


class TestCreatePlanAPIRoute:
    """
    Test for API Route
    """

    def test_create_plan_success(self, client: TestClient) -> None:
        """
        Test create a new plan
        """

        response = client.post(
            "/plans",
            json={
                "name": "Standard",
                "price": {
                    "amount": "10.00",
                    "currency": "USD",
                },
            },
        )

        assert response.status_code == 201

        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Standard"
        assert data["price"]["amount"] == "10.00"
        assert data["price"]["currency"] == "USD"
        assert data["created_at"] is not None
        assert data["updated_at"] is not None
        assert data["is_active"] is True

    def test_create_plan_duplicate(self, client: TestClient) -> None:
        """
        Try to create a new plan with the same name
        """
        response = client.post(
            "/plans",
            json={
                "name": "Standard",
                "price": {
                    "amount": "10.00",
                    "currency": "USD",
                },
            },
        )

        assert response.status_code == 201

        response = client.post(
            "/plans",
            json={
                "name": "Standard",
                "price": {
                    "amount": "10.00",
                    "currency": "USD",
                },
            },
        )

        assert response.status_code == 400

        data = response.json()
        assert data["detail"] == "Plan with name 'Standard' already exists."

    def test_create_plan_invalid_data(self, client: TestClient) -> None:
        """
        Try to create a new plan with invalid data
        """

        response = client.post(
            "/plans",
            json={
                "name": "",
                "price": {
                    "amount": "10.00",
                    "currency": "USD",
                },
            },
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "String should have at least 1 character"
        )
