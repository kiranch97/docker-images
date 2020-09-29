import json

from loguru import logger
from fastapi import APIRouter, WebSocket, Depends
from starlette.websockets import WebSocketDisconnect

from app.log.messages import JSON_DECODE_ERROR, KEY_ERROR
from app.broker.outgoing import queue_raw_frame

from app import models
from app import schemas
from app import crud

router = APIRouter()


@router.websocket("/stream")
async def stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        while True:
            # 1) Retrieve raw frame
            stream_data = await websocket.receive_json()

            # 2) Build RawFrame object
            raw_frame = models.RawFrame(
                img=stream_data["img"],
                taken_at=stream_data["timestamp"],
                lat_lng={"lat": stream_data["lat"], "lng": stream_data["lng"]},
                stream_id=stream_data["stream_id"],
                stream_meta={
                    "user_type": stream_data.get("user_type") or "",
                    "vehicle_type": stream_data.get("vehicle_type") or "",
                    "user_id": stream_data.get("user_id") or "",
                },
            )

            logger.debug("Received frame taken at: {}".format(raw_frame.taken_at))

            # 3) Queue RawFrame to be analysed
            await queue_raw_frame(raw_frame)

    except WebSocketDisconnect:
        logger.info("Websocket connection disconnected")

    except json.JSONDecodeError:
        logger.error(JSON_DECODE_ERROR)

    except KeyError as e:
        logger.error(KEY_ERROR.format(e))

    except Exception as e:
        logger.error(e)
        raise e