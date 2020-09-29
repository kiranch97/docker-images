import json

from loguru import logger
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from app.log.messages import JSON_DECODE_ERROR, KEY_ERROR
from app.broker.outgoing import queue_raw_frame

from app import schemas

router = APIRouter()


@router.websocket("/stream")
async def stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        while True:
            # 1) Retrieve raw frame
            stream_data = await websocket.receive_json()

            # 2) Build RawFrame object
            raw_frame = schemas.RawFrame(
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
        message = "Websocket connection disconnected"
        logger.info(message)

    except json.JSONDecodeError:
        message = JSON_DECODE_ERROR
        await websocket.send_text(message)
        logger.error(JSON_DECODE_ERROR)

    except KeyError as e:
        message = KEY_ERROR.format(e)
        await websocket.send_text(message)
        logger.error(message)

    except Exception as e:
        await websocket.send_text(e)
        logger.error(e)
        raise e