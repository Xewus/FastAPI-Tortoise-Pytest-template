import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent


class AppSettings(BaseSettings):
    """Get settings from `.env` file.

    Use uppercase for the names of the values in the file.
    """

    debug: bool = False
    path: str  # ENV PATH from os
    app_title: str
    app_version: str
    app_description: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    class Config:
        if os.environ.get("ENV") == "dev":
            env_file = ".env.dev"
        elif os.environ.get("ENV") == "prod":
            env_file = ".env.prod"
        else:
            env_file = ".env"


app_settings = AppSettings()

postgres_dsn: PostgresDsn = (
    f"{app_settings.postgres_user}:{app_settings.postgres_password}"
    f"@{app_settings.postgres_host}:{app_settings.postgres_port}"
    f"/{app_settings.postgres_db}"
)

postgres_db_url: PostgresDsn = "asyncpg://" + postgres_dsn

MODELS = [
    "src.databases.postgres.models.SOME_MODEL_1",
    "src.databases.postgres.models.SOME_MODEL_2",
]

TORTOISE_CONFIG = {
    "db_url": postgres_db_url,
    "modules": {"models": MODELS},
    "generate_schemas": True,
    "add_exception_handlers": True,
}

TORTOISE_ORM = {
    "connections": {
        "default": postgres_db_url,
    },
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        },
    },
    "use_tz": False,
}
