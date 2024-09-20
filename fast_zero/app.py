from fastapi import FastAPI

from fast_zero.auth.routes import auth_router
from fast_zero.users.routes import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
