import sqlite3
import time
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import chat, front, sliv
import logging
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.getLogger("passlib").setLevel(logging.ERROR)
models.Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = sqlite3.connect(settings.dbFilename)
        print("Connection was successfull")
        break
    except Exception as error:
        print("Connection was failed", error)
        time.sleep(3)


app.include_router(chat.router)
app.include_router(sliv.router)
app.include_router(front.router)

print(f"Use {settings.hostUrl}/admin/{settings.adminUid} to access admin interface.")