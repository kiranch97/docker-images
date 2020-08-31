from typing import Callable

from loguru import logger

from app.db.events import ping as ping_db
from app.db.events import init as init_db
from app.broker.exchanges import setup_queues


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        try:
            await ping_db()
            await init_db()
            await setup_queues()
        except Exception as e:
            logger.error(e)
            raise e

    return start_app
