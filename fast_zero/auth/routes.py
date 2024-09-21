from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from fast_zero.auth.schema import Token
from fast_zero.security import create_access_token, verify_password
from fast_zero.types import T_CurrentUser, T_OAuth2Form, T_Session
from fast_zero.users.models import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
):
    exist_user = session.scalar(select(User).where(User.email == form_data.username))

    if not exist_user or not verify_password(form_data.password, exist_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": exist_user.email})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }


@auth_router.post("/refresh_token", response_model=Token)
def refresh_access_token(user: T_CurrentUser):
    new_access_token = create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "Bearer"}
