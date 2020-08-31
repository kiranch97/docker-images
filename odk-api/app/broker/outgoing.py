from aio_pika import Message
from aio_pika.exchange import Exchange
from loguru import logger

from app.models.frame import RawFrame
from app.broker.exchanges import exchanges
from app.core.config import EXCHANGE_RAW_FRAMES, SINGLE_ROUTING_KEY


async def queue_raw_frame(raw_frame: RawFrame) -> None:
    """
    Queuing a RawFrame object.

    TODO: add more documentation
    """
    try:
        exchange_raw_frames: Exchange = exchanges.get(EXCHANGE_RAW_FRAMES)

        await exchange_raw_frames.publish(
            message=Message(raw_frame.json().encode("utf8")),
            routing_key=SINGLE_ROUTING_KEY,
        )
        logger.debug("Raw frame queued")

    except Exception as e:
        logger.error(e)
        raise e
