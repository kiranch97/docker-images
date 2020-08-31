from loguru import logger

from aio_pika import connect_robust, connect
from aio_pika.connection import Connection
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.config import BROKER_URL

max_tries = 20
wait_seconds = 1


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
async def get_connection() -> Connection:
    try:
        conn = await connect_robust(BROKER_URL)
        conn.add_close_callback(close_callback)
        conn.add_reconnect_callback(reconnect_callback)

        logger.debug("Connection setup with: {}".format(conn))
        return conn

    except Exception as e:
        logger.error(e)
        raise e


def close_callback(connection, message):
    logger.debug("Connection: {}".format(connection))
    logger.debug("Message: {}".format(message))

    logger.info("Connection closed with: {}".format(connection))


def reconnect_callback(arg1, arg2):
    logger.debug("arg1: {}".format(arg1))
    logger.debug("arg2: {}".format(arg2))

    logger.info("Reconnected with: {}".format(arg1))
