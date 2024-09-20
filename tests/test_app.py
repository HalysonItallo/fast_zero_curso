from http import HTTPStatus

from fast_zero.users.user_schema import UserResponse


def test_create_user_is_success(client):
    payload = {
        "username": "testusername",
        "email": "test@test.com",
        "password": "password",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.CREATED

    expected = {
        "id": 1,
        "username": "testusername",
        "email": "test@test.com",
    }

    assert response.json() == expected


def test_create_user_raise_400_when_username_if_exists(client, user):
    payload = {
        "username": "Teste",
        "email": "test@test.com",
        "password": "password",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST

    expected = {"detail": "Username already exists"}

    assert response.json() == expected


def test_create_user_raise_400_when_email_if_exists(client, user):
    payload = {
        "username": "testusername",
        "email": "teste@test.com",
        "password": "password",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST

    expected = {"detail": "Email already exists"}

    assert response.json() == expected


def test_read_users_is_success(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK

    expected = {"users": []}

    assert response.json() == expected


def test_read_users_with_users_success(client, user):
    user_schema = UserResponse.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK

    expected = {"users": [user_schema]}

    assert response.json() == expected


def test_detail_users_is_success(client, user):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK

    expected = {
        "id": 1,
        "username": "Teste",
        "email": "teste@test.com",
    }

    assert response.json() == expected


def test_detail_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND

    expected = {
        "detail": "User not found!",
    }

    assert response.json() == expected


def test_update_users_is_success(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    payload = {
        "username": "newusername",
        "email": "test@newtest.com",
        "password": "password",
    }

    response = client.put("/users/2", json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND

    expected = {
        "detail": "User not found!",
    }

    assert response.json() == expected


def test_delete_users_is_success(client, user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    response = client.delete("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND

    expected = {
        "detail": "User not found!",
    }

    assert response.json() == expected
