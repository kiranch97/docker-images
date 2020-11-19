import logging
from typing import List
import secrets

from starlette.config import Config
from loguru import logger

from databases import DatabaseURL
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

ADMIN_EMAIL:str = config("ADMIN_EMAIL")
ADMIN_PASSWORD:str = config("ADMIN_PASSWORD", default="admin")
ADMIN_USERNAME: str = config("ADMIN_USERNAME", default="admin")

VERSION: str = config("VERSION")
PROJECT_NAME: str = config("PROJECT_NAME", default="ODK API")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
SECRET_KEY: str = config("SECRET_KEY", default=secrets.token_urlsafe(32))

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="",
)

DATABASE_URL: DatabaseURL = config("DATABASE_URL", cast=DatabaseURL)
BROKER_URL: str = config("BROKER_URL")

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

# RabbitMQ
QUEUE_RAW_FRAMES = "queue_raw_frames"
EXCHANGE_RAW_FRAMES = "exchange_raw_frames"

QUEUE_ANALYSED_FRAMES = "queue_analysed_frames"
EXCHANGE_ANALYSED_FRAMES = "exchange_analysed_frames"
SINGLE_ROUTING_KEY = "frame"
