from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
from typing import Optional

# Load .env once at import time
load_dotenv()


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = Field(alias="OPENAI_API_KEY")

    # Spotify
    spotipy_client_id: str = Field(alias="SPOTIPY_CLIENT_ID")
    spotipy_client_secret: str = Field(alias="SPOTIPY_CLIENT_SECRET")
    spotipy_redirect_uri: str = Field(alias="SPOTIPY_REDIRECT_URI")

    # Database
    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")
    db_host: str = Field(default="127.0.0.1", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="nichify", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")

    class Config:
        validate_assignment = True
        populate_by_name = True
        extra = "ignore"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


def reload_settings() -> None:
    get_settings.cache_clear()  # type: ignore[attr-defined]