import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from src.infra.api import app, get_auth_service
from src.infra.auth import InMemoryAuthService
from src.infra.db import get_session


@pytest.fixture(scope="function")
def session():
    """
    Fixture for creating a database session.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


@pytest.fixture(scope="function")
def auth_service():
    """
    Fixture for creating an authentication service.
    """

    return InMemoryAuthService()


@pytest.fixture
def client(session, auth_service):
    """
    Fixture for creating a test client.
    """

    def get_session_override():
        return session

    def get_auth_service_override():
        return auth_service

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_auth_service] = get_auth_service_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
