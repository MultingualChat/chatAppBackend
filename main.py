from fastapi import FastAPI
from controller import user, auth
from config import config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.config = config

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user.router, prefix=f"/user")
app.include_router(auth.router, prefix=f"/auth")


