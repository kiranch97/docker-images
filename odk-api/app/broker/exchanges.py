from typing import Dict

from loguru import logger
from aio_pika import ExchangeType

from app.core.config import SINGLE_ROUTING_KEY
from app.core.config import EXCHANGE_RAW_FRAMES, QUEUE_RAW_FRAMES
from app.core.config import EXCHANGE_ANALYSED_FRAMES, QUEUE_ANALYSED_FRAMES

from app.broker.connection import get_connection
from app.broker.incoming import handle_analysed_frame

exchanges: Dict = {}


async def setup_queues() -> None:
    conn = await get_connection()
    channel = await conn.channel()

    # queue for sending RawFrame to frame analyser
    exchange_raw_frames = await channel.declare_exchange(
        EXCHANGE_RAW_FRAMES, ExchangeType.DIRECT
    )
    queue_raw_frames = await channel.declare_queue(QUEUE_RAW_FRAMES)

    exchanges[EXCHANGE_RAW_FRAMES] = exchange_raw_frames

    await queue_raw_frames.bind(
        exchange=exchange_raw_frames, routing_key=SINGLE_ROUTING_KEY
    )

    # queue for receiving AnalysedFrames from frame analyser
    exchange_analysed_frames = await channel.declare_exchange(
        EXCHANGE_ANALYSED_FRAMES, ExchangeType.DIRECT
    )
    queue_analysed_frames = await channel.declare_queue(QUEUE_ANALYSED_FRAMES)

    exchanges[EXCHANGE_ANALYSED_FRAMES] = exchange_analysed_frames

    await queue_analysed_frames.bind(
        exchange=exchange_analysed_frames, routing_key=SINGLE_ROUTING_KEY
    )

    # setup listining to queue
    await queue_analysed_frames.consume(handle_analysed_frame)

    logger.info("Exchanges & queues setup!")
