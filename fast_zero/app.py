from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.users.models import User
from fast_zero.users.user_schema import UserResponse, UserSchema

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


@app.get("/users/", response_model=list[UserResponse])
def read_users(session: Session = Depends(get_session)):
    db_users = session.scalars(select(User))
    return db_users


# @app.get("/users/{user_id}", response_model=UserResponse)
# def detail_user(user_id: int):
#     if user_id < 1 or len(database) < user_id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     user = database[user_id - 1]

#     return user


# @app.put("/users/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user: UserSchema):
#     if user_id < 1 or len(database) < user_id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     user_db = UserDB(**user.model_dump(), id=user_id)
#     database[user_id - 1] = user_db

#     return user_db


# @app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int):
#     if user_id < 1 or len(database) < user_id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     del database[user_id - 1]
