from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, Response
from ..models import Link2ClientIdModel, AdminModel
from app.database import SessionLocal
from sqlalchemy import insert
from ..settings import settings
from app.utils.main import generate_client_id
from .chat import manager

router = APIRouter()


@router.get("/")
async def get():
    with open("./templates/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)



@router.get("/admin/{key}")
async def get_admin(key: str):
    if key == settings.adminUid:
        with open("../admin/templates/index.html", "r", encoding="utf-8") as file:
            content = file.read()
            content = content.replace("${TOKEN}", settings.adminUid)
        return HTMLResponse(content=content)
    else:
        raise HTTPException(status_code=404)


@router.get("/admin/static/main.js/{key}")
async def get_admin_js(key: str):
    if key == settings.adminUid:
        client_id = generate_client_id()
        with SessionLocal() as session:
            stmt = insert(AdminModel).values(client_id=client_id)
            session.execute(stmt)
            session.commit()

        with open("../admin/templates/main.js", "r", encoding="utf-8") as file:
            content = file.read()
            content = content.replace("${TOKEN}", settings.adminUid)
            content = content.replace("${HOSTURL}", settings.hostUrl)
            content = content.replace("${WSHOSTURL}", settings.wsHostUrl)
            content = content.replace("${CLIENT_ID}", client_id)
        return Response(content=content, media_type="application/javascript")
    else:
        raise HTTPException(status_code=404)


@router.get("/main.js/{id}")
async def get_main_js(id: str):
    client_id = 0
    with SessionLocal() as session:
        client_link = session.query(Link2ClientIdModel).filter(Link2ClientIdModel.link_id == id).first()

        if client_link:
            if client_link.client_id not in await manager.get_users():
                client_id = client_link.client_id

        if not client_id:
            client_id = generate_client_id()

            stmt = insert(Link2ClientIdModel).values(
                link_id=id,
                client_id=client_id
            )

            session.execute(stmt)
            session.commit()

    with open("./templates/main.js", "r") as file:
        content = file.read()
        content = content.replace("${CLIENT_ID}", client_id)
        content = content.replace("${ADMIN_NAME}", settings.chatSupportName)
        content = content.replace("${HOSTURL}", settings.hostUrl)
        content = content.replace("${WSHOSTURL}", settings.wsHostUrl)

        content = content.replace("${CHAT_HEADER}", settings.charHeader)
        content = content.replace("${WELCOME_MESSAGE}", settings.welcomeMessage)
        content = content.replace("${ENTER_MESSAGE}", settings.enterMessage)
    return Response(content=content, media_type="application/javascript")


@router.get("/utils.js")
async def get_utils_js():
    with open("./templates/utils.js", "r") as file:
        content = file.read()
    return Response(content=content, media_type="application/javascript")


@router.get("/crawlUtils.js")
async def get_crawl_utils_js():
    with open("./templates/crawlUtils.js", "r") as file:
        content = file.read()
    return Response(content=content, media_type="application/javascript")


@router.get("/crawl.js")
async def get_crawl_js():
    with open("./templates/crawl.js", "r") as file:
        content = file.read()
    return Response(content=content, media_type="application/javascript")


@router.get("/styles.css")
async def get_index_css():
    with open("./templates/styles.css", "r") as file:
        return FileResponse("./templates/styles.css")


@router.get("/admin/static/styles.css")
async def get_admin_css():
    with open("../admin/templates/styles.css", "r", encoding="utf-8") as file:
        content = file.read()
    return Response(content=content, media_type="text/css")


@router.get("/static/icon/{file_name}")
async def get_admin_static(file_name: str):
    if file_name in [
        "Send-256x256.svg",
        "free-icon-add-file-1090923.svg",
        "chat-icon.png",
        "Vector.svg",
        "customer-service.png"
    ]:
        return FileResponse(f"./templates/{file_name}")
    else:
        raise HTTPException(status_code=404)

