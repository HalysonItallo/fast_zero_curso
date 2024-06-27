import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models.user_model import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:")
    # Cria a tabela usando os metadados
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Deleta a tabela usando os metadados
    table_registry.metadata.drop_all(engine)
