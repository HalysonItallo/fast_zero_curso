from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.security import create_access_token, get_current_user, get_password_hash, verify_password
from fast_zero.users.models import User
from fast_zero.users.user_schema import Token, UserList, UserResponse, UserSchema

app = FastAPI()


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    exist_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if exist_user:
        if exist_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        if exist_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

    db_user = User(
        **user.model_dump(exclude=("password")),
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    db_users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": db_users}


@app.get("/users/{user_id}", response_model=UserResponse)
def detail_user(user_id: int, session: Session = Depends(get_session)):
    exist_user = session.scalar(select(User).where(User.id == user_id))

    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return exist_user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    exist_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if exist_user:
        if exist_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        if exist_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    session.delete(current_user)
    session.commit()


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
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
