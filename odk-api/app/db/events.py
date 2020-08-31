from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    before_log,
    after_log,
    retry_if_exception_type,
)

from sqlalchemy.ext.declarative import declarative_base
from psycopg2 import OperationalError

from app.db.session import SessionLocal, engine
import app.db.base
from app.db.base_class import Base

max_tries = 20
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds),
)
async def ping() -> None:
    try:
        session = SessionLocal()
        session.execute("SELECT 1")
        logger.info("Can query to server!")
    except Exception as e:
        logger.error(e)
        raise e


async def init() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Initialized database")
    except Exception as e:
        logger.error(e)
        # raise e
