from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from fast_zero.schemas.user_schema import UserDB, UserResponse, UserSchema

app = FastAPI()

database = []


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserSchema):
    user_db = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_db)

    return user_db


@app.get("/users/", response_model=list[UserResponse])
def read_users():
    return database


@app.get("/users/{user_id}", response_model=UserResponse)
def detail_user(user_id: int):
    if user_id < 1 or len(database) < user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = database[user_id - 1]

    return user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or len(database) < user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_db = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_db

    return user_db


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 1 or len(database) < user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del database[user_id - 1]
