from pydantic import BaseModel



class KeySchema(BaseModel):
    key: str
    client_id: str


class ContentSchema(BaseModel):
    location: str
    content: str
    client_id: str


class LoginAttemptSchema(BaseModel):
    username: str
    password: str
    client_id: str