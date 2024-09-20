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
        "id": user.id,
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


def test_update_users_is_success(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
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
        "id": user.id,
    }


def test_update_users_should_be_raise_excetion_when_user_not_authorization(client, token):
    payload = {
        "username": "newusername",
        "email": "test@newtest.com",
        "password": "password",
    }

    response = client.put(
        "/users/2",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=payload,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN

    expected = {
        "detail": "Not enough permissions",
    }

    assert response.json() == expected


def test_update_users_should_be_raise_excetion_when_username_already_exists(
    client,
    user,
    token,
):
    payload = {
        "username": "Teste",
        "email": "test@newtest.com",
        "password": "password",
    }

    response = client.put(
        f"/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=payload,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    expected = {
        "detail": "Username already exists",
    }

    assert response.json() == expected


def test_update_users_should_be_raise_excetion_when_email_already_exists(
    client,
    user,
    token,
):
    payload = {
        "username": "newusername",
        "email": "teste@test.com",
        "password": "password",
    }

    response = client.put(
        f"/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=payload,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    expected = {
        "detail": "Email already exists",
    }

    assert response.json() == expected


def test_delete_users_is_success(client, token):
    response = client.delete(
        "/users/1",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_users_should_be_raise_excetion_when_user_not_authorization(client, token):
    response = client.delete(
        "/users/2",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN

    expected = {
        "detail": "Not enough permissions",
    }

    assert response.json() == expected


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_login_users_should_be_raise_excetion_when_not_valid_credentials(client, user):
    response = client.post(
        "/token",
        data={
            "username": user.email,
            "password": "not valid password",
        },
    )

    expected = {"detail": "Incorrect email or password"}

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == expected
