import json
from json.decoder import JSONDecodeError

from loguru import logger
from aio_pika import IncomingMessage

from app.models.frame import AnalysedFrame
from app.logic.services import persist_analysed_frame
from app.log.messages import JSON_DECODE_ERROR, KEY_ERROR
from app.db.session import get_session


async def handle_analysed_frame(message: IncomingMessage) -> None:
    try:
        message.ack()
        analysed_frame_dict = json.loads(message.body.decode("utf-8"))

        logger.debug("Receiving analysed frame")

        analysed_frame = AnalysedFrame(
            taken_at=analysed_frame_dict["taken_at"],
            lat_lng=analysed_frame_dict["lat_lng"],
            stream_id=analysed_frame_dict["stream_id"],
            detected_objects=analysed_frame_dict["detected_objects"],
            object_count=analysed_frame_dict["object_count"],
            stream_meta=analysed_frame_dict["stream_meta"],
            img_meta=analysed_frame_dict["img_meta"],
            analyser_meta=analysed_frame_dict["analyser_meta"],
        )

        persist_analysed_frame(get_session(), analysed_frame)

    except JSONDecodeError:
        logger.error(JSON_DECODE_ERROR)

    # except TypeError as e:
    #     logger.error(e)

    except KeyError as e:
        logger.error(KEY_ERROR.format(e))

    except Exception as e:
        logger.error(e)
        raise e
