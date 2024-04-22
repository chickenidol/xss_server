from pydantic_settings import BaseSettings, SettingsConfigDict
import uuid

class Settings(BaseSettings):
    charHeader: str
    enterMessage: str
    welcomeMessage: str
    hostUrl: str
    wsHostUrl: str
    adminUid: str
    chatSupportName: str
    chatIdLength: int
    dbFilename: str = "db/your_database.db"

    class Config:
        env_file = ".env"

adminUid = str(uuid.uuid4())
settings = Settings(adminUid=adminUid)

print(settings)
