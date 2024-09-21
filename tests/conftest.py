import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session, model_registry
from fast_zero.security import get_password_hash
from fast_zero.todos.models import Todo, TodoState
from fast_zero.users.models import User


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}+senha")


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
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    model_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    model_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    password = "testtest"

    user = UserFactory(
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # Monkey Patch

    return user


@pytest.fixture()
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        "auth/token",
        data={
            "username": user.email,
            "password": user.clean_password,
        },
    )

    return response.json()["access_token"]
