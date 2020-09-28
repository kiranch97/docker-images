from app.schemas.user import UserCreate
from typing import Callable

from loguru import logger
from sqlalchemy.orm import session

from app.db.events import ping as ping_db
from app.db.events import init as init_db
from app.broker.exchanges import setup_queues

from app.core.config import ADMIN_EMAIL, ADMIN_PASSWORD
from app.models import User
from app.crud import user
from app.db.session import get_session


async def create_base_user() -> User:
    db_session = get_session()

    try:

        if base_user := user.get_by_email(db=db_session, email=ADMIN_EMAIL):
            return base_user
        
        new_base_user = UserCreate(
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            is_superuser=True,
            full_name="Administrator"
        )

        db_user = user.create(
            db=db_session,
            obj_in=new_base_user
        )
        logger.debug("Created new admin user")
        return db_user
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db_session.close()

def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        try:
            await ping_db()
            await init_db()
            await setup_queues()

            base_user = await create_base_user()
            logger.info(f"Administrator: {base_user.email}")
        except Exception as e:
            logger.error(e)
            raise e

    return start_app

