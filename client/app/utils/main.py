from sqlalchemy import insert
from app.database import SessionLocal
from ..models import MessageModel, Link2ClientIdModel
import requests
import requests.utils
import uuid
from ..settings import settings
import hashlib

class FileData:
    def __init__(self, content, file_name):
        self.uid = str(uuid.uuid4())
        self.content = content
        self.file_name = file_name


async def add_message_to_database(message: str, from_id: str, to_id: str):
    with SessionLocal() as session:
        stmt = insert(MessageModel).values(
            message=requests.utils.unquote(message),
            from_id=from_id,
            to_id=to_id
        )
        session.execute(stmt)
        session.commit()


async def add_file_to_database(message: str, from_id: str, to_id: str, file: FileData):
    with SessionLocal() as session:
        stmt = insert(MessageModel).values(
            message=requests.utils.unquote(message),
            file_data=requests.utils.unquote(file.content),
            file_name=requests.utils.unquote(file.file_name),
            file_uid=file.uid,
            from_id=from_id,
            to_id=to_id
        )
        session.execute(stmt)
        session.commit()


def msg2json(message):
    data = {
        "operation": "msg",
        "sourceClientId": message.from_id,
        "destClientId": message.to_id,
        "text": requests.utils.quote(message.message)
    }

    if message.file_uid:
        data['fileUid'] = message.file_uid
        data['fileName'] = message.file_name
        data['operation'] = "file"

    return data


def get_file(uid: str):
    with SessionLocal() as session:
        file = session.query(MessageModel).filter(MessageModel.file_uid == uid).first()
        if file:
            return file.file_data, file.file_name
        else:
            return 0,0


def check_client_id(client_id: str):
    with SessionLocal() as session:
        db_id = session.query(Link2ClientIdModel).filter(Link2ClientIdModel.client_id == client_id).first()

        if db_id:
            return True
        else:
            return False


def generate_client_id(s: int = settings.chatIdLength):
    uid = str(uuid.uuid4())
    hash_str = hashlib.md5(uid.encode()).hexdigest()
    return str(hash_str)[:s]

