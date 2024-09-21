from fastapi import status
from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        "auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_login_users_should_be_raise_excetion_when_not_valid_password_credential(client, user):
    response = client.post(
        "auth/token",
        data={
            "username": user.email,
            "password": "not valid password",
        },
    )

    expected = {"detail": "Incorrect email or password"}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected


def test_login_users_should_be_raise_excetion_when_not_valid_email_credential(client, user):
    response = client.post(
        "auth/token",
        data={
            "username": "not valid email",
            "password": user.clean_password,
        },
    )

    expected = {"detail": "Incorrect email or password"}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected


def test_token_expired_after_time(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "auth/token",
            data={"username": user.email, "password": user.clean_password},
        )

        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.delete("users/1", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Invalid or expired token"}


def test_refresh_token(client, token):
    response = client.post(
        "/auth/refresh_token",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["token_type"] == "Bearer"
    assert "access_token" in data


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "auth/token",
            data={"username": user.email, "password": user.clean_password},
        )

        assert response.status_code == status.HTTP_200_OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.post(
            "/auth/refresh_token",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Invalid or expired token"}
