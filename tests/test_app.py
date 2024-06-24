from http import HTTPStatus


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


def test_read_users_is_success(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK

    expected = [
        {
            "id": 1,
            "username": "testusername",
            "email": "test@test.com",
        }
    ]

    assert response.json() == expected


def test_detail_users_is_success(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK

    expected = {
        "id": 1,
        "username": "testusername",
        "email": "test@test.com",
    }

    assert response.json() == expected


def test_detail_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND

    expected = {
        "detail": "User not found",
    }

    assert response.json() == expected


def test_update_users_is_success(client):
    payload = {
        "username": "newusername",
        "email": "test@newtest.com",
        "password": "password",
    }

    response = client.put("/users/1", json=payload)

    assert response.status_code == HTTPStatus.OK

    expected = {
        "id": 1,
        "username": "newusername",
        "email": "test@newtest.com",
    }

    assert response.json() == expected


def test_update_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    payload = {
        "username": "newusername",
        "email": "test@newtest.com",
        "password": "password",
    }

    response = client.put("/users/2", json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND

    expected = {
        "detail": "User not found",
    }

    assert response.json() == expected


def test_delete_users_is_success(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_users_should_be_raise_excetion_when_user_id_is_not_valid(client):
    response = client.delete("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND

    expected = {
        "detail": "User not found",
    }

    assert response.json() == expected
