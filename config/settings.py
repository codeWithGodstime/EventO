from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).parent.parent / ".env"

load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    
    SECRET_KEY: str
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int
    ALGORITHM: str

    @property
    def DATABASE_URI(self):
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class Config:
        env_file = str(env_path)
        env_file_encoding = "utf-8"


def get_settings():
    return Settings()
