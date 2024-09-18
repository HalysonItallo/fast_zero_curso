import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session, model_registry


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    model_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    model_registry.metadata.drop_all(engine)
