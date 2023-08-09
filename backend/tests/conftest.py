import os
import sys

assert (sys.version_info.major, sys.version_info.minor) == (
    3,
    11,
), "Only Python 3.11 allowed"

POSTGRES_USER = "test_postrgres_user"
POSTGRES_PASSWORD = "test_postgres_password"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "25432"
POSTGRES_DB = "test_db"

os.environ["TESTING"] = "1"
os.environ["POSTGRES_USER"] = POSTGRES_USER
os.environ["POSTGRES_PASSWORD"] = POSTGRES_PASSWORD
os.environ["POSTGRES_HOST"] = POSTGRES_HOST
os.environ["POSTGRES_PORT"] = POSTGRES_PORT
os.environ["POSTGRES_DB"] = POSTGRES_DB

import asyncio
from asyncio import AbstractEventLoop
from pathlib import Path
from time import sleep
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.config import TORTOISE_ORM
from tests.containers import Docker
from tests.utils import clean_db
from tortoise import Tortoise

BASE_DIR = Path(__file__).parent.parent.resolve()

assert str(BASE_DIR).endswith("backend")


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def containers_setup(
    event_loop: AbstractEventLoop,
) -> Generator[None, None, None]:
    async with Docker(
        postgres_user=POSTGRES_USER,
        postgres_password=POSTGRES_PASSWORD,
        postgres_port=POSTGRES_PORT,
        postgres_db=POSTGRES_DB,
    ):
        sleep(1.3)
        yield


@pytest.fixture(scope="function")
async def databases(containers_setup) -> Generator[None, None, None]:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=False)
    yield
    await clean_db()


@pytest.fixture(name="http_client")
async def get_http_client(containers_setup) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client