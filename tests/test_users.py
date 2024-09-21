from fastapi import status

from fast_zero.users.schema import UserResponse


def test_create_user_is_success(client):
    payload = {
        "username": "testusername",
        "email": "test@test.com",
        "password": "password",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    expected = {
        "id": 1,
        "username": "testusername",
        "email": "test@test.com",
    }

    assert response.json() == expected


def test_create_user_raise_400_when_username_if_exists(client, user):
    payload = {
        "username": user.username,
        "email": "test@test.com",
        "password": "password",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    expected = {"detail": "Username already exists"}

    assert response.json() == expected


def test_create_user_raise_400_when_email_if_exists(client, user):
    payload = {
        "username": "testusername",
        "email": user.email,
        "password": "password",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    expected = {"detail": "Email already exists"}

    assert response.json() == expected


def test_read_users_is_success(client):
    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK

    expected = {"users": []}

    assert response.json() == expected


def test_read_users_with_users_success(client, user):
    user_schema = UserResponse.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK

    expected = {"users": [user_schema]}

    assert response.json() == expected


def test_detail_users_is_success(client, user):
    response = client.get(f"/users/{user.id}")

    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    assert response.json() == expected


def test_detail_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    response = client.get("/users/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND

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

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": user.id,
    }


def test_update_users_should_be_raise_excetion_when_user_not_authorization(client, other_user, token):
    payload = {
        "username": "newusername",
        "email": "test@newtest.com",
        "password": "password",
    }

    response = client.put(
        f"/users/{other_user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=payload,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

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
        "username": user.username,
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

    assert response.status_code == status.HTTP_400_BAD_REQUEST

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
        "email": user.email,
        "password": "password",
    }

    response = client.put(
        f"/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    expected = {
        "detail": "Email already exists",
    }

    assert response.json() == expected


def test_delete_users_is_success(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_users_should_be_raise_excetion_when_user_not_authorization(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    expected = {
        "detail": "Not enough permissions",
    }

    assert response.json() == expected
