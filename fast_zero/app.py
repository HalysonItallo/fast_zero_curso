from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.users.models import User
from fast_zero.users.user_schema import UserList, UserResponse, UserSchema

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

    db_user = User(**user.model_dump())
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
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    exist_user = session.scalar(select(User).where(User.id == user_id))

    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!",
        )

    exist_user.username = user.username
    exist_user.password = user.password
    exist_user.email = user.email
    session.commit()
    session.refresh(exist_user)

    return exist_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    exist_user = session.scalar(select(User).where(User.id == user_id))

    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")

    session.delete(exist_user)
    session.commit()
