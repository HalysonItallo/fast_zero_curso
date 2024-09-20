from fastapi import status
from jwt import decode

from fast_zero.config.settings import Settings
from fast_zero.security import create_access_token

settings = Settings()


def test_jwt():
    data = {"sub": "test@test.comn"}
    token = create_access_token(data)

    result = decode(
        token,
        settings.SECRET_KEY,
        algorithms=[
            settings.ALGORITHM,
        ],
    )

    assert result["sub"] == data["sub"]
    assert result["exp"]


def test_jwt_invalid_token(client):
    response = client.delete("users/1", headers={"Authorization": "Bearer token-invalido"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_should_be_raise_exception_when_claims_sub_is_none(client):
    data = {"sub": None}
    token = create_access_token(data)
    response = client.delete("users/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_should_be_raise_exception_when_claimms_sub_is_not_valid_user_email(client):
    data = {"sub": "notexist@not.com"}
    token = create_access_token(data)
    response = client.delete("users/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
