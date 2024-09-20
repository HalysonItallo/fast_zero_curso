from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from fast_zero.security import get_password_hash
from fast_zero.types import T_CurrentUser, T_Session
from fast_zero.users.models import User
from fast_zero.users.schema import UserList, UserResponse, UserSchema

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserSchema, session: T_Session):
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


@user_router.get("/", response_model=UserList)
def read_users(
    session: T_Session,
    skip: int = 0,
    limit: int = 100,
):
    db_users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": db_users}


@user_router.get("/{user_id}", response_model=UserResponse)
def detail_user(user_id: int, session: T_Session):
    exist_user = session.scalar(select(User).where(User.id == user_id))

    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    return exist_user


@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserSchema, session: T_Session, current_user: T_CurrentUser):
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


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    session.delete(current_user)
    session.commit()
