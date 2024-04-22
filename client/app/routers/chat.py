from fastapi.responses import Response
from fastapi import HTTPException
from fastapi import (
    WebSocket,
    WebSocketDisconnect,
    status,
    APIRouter,
)
import requests
from app.utils.main import add_message_to_database, add_file_to_database, msg2json, get_file, check_client_id, \
    generate_client_id, FileData
from ..web_socket import ClientConnectionManager, AdminConnectionManager
from ..settings import settings
import json
import base64

router = APIRouter(prefix="/chat", tags=["Chat"])
manager = ClientConnectionManager()
admin_manager = AdminConnectionManager(manager)


@router.websocket("/ws/admin/{admin_id}/{key}")
async def admin_websocket_endpoint(websocket: WebSocket, admin_id: str, key: str = ""):
    if settings.adminUid == key:
        await admin_manager.connect_user(websocket, admin_id)

        try:
            while True:
                message = await websocket.receive()
                if message["type"] == "websocket.disconnect":
                    await admin_manager.disconnect_user(admin_id)
                    break

                data = json.loads(message['text'])

                if data['operation'] == 'getClients':
                    await admin_manager.send_users(admin_id)
                elif data['operation'] == 'setConversation':
                    if admin_manager.set_conversation(admin_id, data['clientId']):
                        await admin_manager.notify_client_admin_connected(admin_id, data['clientId'])
                elif data['operation'] == 'releaseConversation':
                    admin_manager.release_conversation(admin_id)
                    await admin_manager.notify_client_admin_disconnected(admin_id, data['clientId'])
                elif data['operation'] == 'getConversationData':
                    await admin_manager.send_conversation_history(admin_id, data['clientId'])
        except WebSocketDisconnect:
            await admin_manager.disconnect_user(admin_id)
            return

    raise HTTPException(status_code=404)


@router.websocket("/ws/client/{client_id}/{key}")
@router.websocket("/ws/client/{client_id}")
async def client_websocket_endpoint(websocket: WebSocket, client_id: str, key: str = ""):
    is_admin = False
    if key == settings.adminUid:
        is_admin = True

    await manager.connect_user(websocket, client_id)
    if not is_admin:
        await manager.on_connect(client_id)
    try:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                await manager.disconnect_user(client_id)
                break

            data = json.loads(message['text'])

            if data['operation'] == 'file':
                file_data = FileData(requests.utils.unquote(data['content']), requests.utils.unquote(data['fileName']))
                data['content'] = ""
                data['fileUid'] = file_data.uid
                text = f"Client #{client_id} uploaded a file: {file_data.file_name}"
                await add_file_to_database(text, client_id, data['destClientId'], file_data)

                await manager.send_message(json.dumps(data), client_id)
                await manager.send_message(json.dumps(data), data['destClientId'])
            elif data['operation'] == 'msg':
                text = requests.utils.unquote(data['text'])
                await add_message_to_database(text, client_id, data['destClientId'])

                await manager.send_message(json.dumps(data), client_id)
                await manager.send_message(json.dumps(data), data['destClientId'])
            elif data['operation'] == 'requestConversation':
                admin_id = admin_manager.get_conversation(data['clientId'])

                if admin_id:
                    await admin_manager.notify_client_admin_connected(admin_manager.get_conversation(data['clientId']), data['clientId'])

    except WebSocketDisconnect:
        await manager.disconnect_user(client_id)


@router.get("/download/{uid}")
async def download_file(uid):
    file_data, file_name = get_file(uid)

    if file_data:
        encoded = file_data.split(',')[1]
        data = base64.b64decode(encoded)

        media_type = file_data[file_data.find('data:') + 5:file_data.find(';')]
        headers = {
            'Content-Disposition': f'attachment; filename="{file_name}"'
        }
        return Response(content=data, media_type=media_type, headers=headers)
    else:
        raise HTTPException(status_code=404)
