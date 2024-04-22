import json

from .models import MessageModel
from fastapi.websockets import WebSocket
from app.database import SessionLocal
from app.utils.main import msg2json, generate_client_id


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect_user(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.connections[user_id] = websocket

    async def disconnect_user(self, user_id: str):
        if user_id in self.connections:
            del self.connections[user_id]


class ClientConnectionManager(ConnectionManager):
    async def get_users(self):
        return list(self.connections.keys())

    async def send_message(self, message: str, dest_user_id: str):
        for user_id, ws in self.connections.items():
            if user_id == dest_user_id and ws:
                await ws.send_text(message)

    async def notify_client(self, client_id: str, message: str):
        if client_id in self.connections:
            await self.connections[client_id].send_text(message)

    async def on_connect(self, client_id: str):
        with SessionLocal() as session:
            messages = session.query(MessageModel).filter(
                (MessageModel.from_id == client_id) | (MessageModel.to_id == client_id)).all()

        for message in messages:
            data = msg2json(message)
            await self.connections[client_id].send_text(json.dumps(data))


class AdminConnectionManager(ConnectionManager):
    def __init__(self, clientManager: ClientConnectionManager):
        self.conversations = {}
        self.clientManager = clientManager
        super().__init__()

    async def get_users(self):
        res = []
        for user in await self.clientManager.get_users():
            if user not in self.conversations and user not in self.connections:
                res.append(user)
        return res

    async def send_users(self, admin_id: str):
        users = await self.get_users()
        ret = {
            "operation": "usersUpdate",
            "data": users
        }
        await self.connections[admin_id].send_text(json.dumps(ret))

    def set_conversation(self, admin_id: str, client_id: str):
        if client_id not in self.conversations:
            self.conversations[client_id] = admin_id
            return True

    def get_conversation(self, client_id: str):
        if client_id in self.conversations:
            return self.conversations[client_id]

    async def notify_client_admin_connected(self, admin_id: str, client_id: str):
        if client_id in self.conversations and self.conversations[client_id] == admin_id:
            ret = {
                "operation": "adminConnected",
                "data": {
                    "adminId": admin_id
                }
            }

            await self.clientManager.notify_client(client_id, json.dumps(ret))

    async def notify_client_admin_disconnected(self, admin_id: str, client_id: str):
        ret = {
            "operation": "adminDisconnected",
            "data": {
                "adminId": admin_id
            }
        }

        await self.clientManager.notify_client(client_id, json.dumps(ret))

    async def send_conversation_history(self, admin_id: str, client_id: str):
        with SessionLocal() as session:
            messages = session.query(MessageModel).filter(
                (MessageModel.from_id == client_id) | (MessageModel.to_id == client_id)).all()

        for message in messages:
            ret = {
                "operation": "userConversationData",
                "data": msg2json(message)
            }
            if ret['data']['sourceClientId'] == client_id:
                ret['data']['destClientId'] = admin_id
            else:
                ret['data']['sourceClientId'] = admin_id

            await self.connections[admin_id].send_text(json.dumps(ret))

    def release_conversation(self, admin_id: str):
        to_del = None
        for client_id, adm_id in self.conversations.items():
            if adm_id == admin_id:
                to_del = client_id
                break
        if to_del:
            del self.conversations[to_del]

    async def disconnect_user(self, admin_id: str):
        await super().disconnect_user(admin_id)
        self.release_conversation(admin_id)

