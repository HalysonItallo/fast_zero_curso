from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_login_users_should_be_raise_excetion_when_not_valid_credentials(client, user):
    response = client.post(
        "auth/token",
        data={
            "username": user.email,
            "password": "not valid password",
        },
    )

    expected = {"detail": "Incorrect email or password"}

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == expected
