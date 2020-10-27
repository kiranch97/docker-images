import json

from loguru import logger
from fastapi import APIRouter, WebSocket, Depends
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect

from app.log.messages import JSON_DECODE_ERROR, KEY_ERROR
from app.broker.outgoing import queue_raw_frame
from app.logic.users import get_current_active_user

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


@router.post("/raw_frame")
async def receive_raw_frame(
    frame_dict: dict,
    current_user = Depends(get_current_active_user),
) -> JSONResponse:
    response_status_code: int = 500
    response_content: dict = {}

    try:
        raw_frame = schemas.RawFrame(
            img=frame_dict["img"],
            taken_at=frame_dict["timestamp"],
            lat_lng={"lat": frame_dict["lat"], "lng": frame_dict["lng"]},
            stream_id=frame_dict["stream_id"],
            stream_meta={
                "user_type": frame_dict.get("user_type") or "",
                "vehicle_type": frame_dict.get("vehicle_type") or "",
                "user_id": frame_dict.get("user_id") or "",
            },
        )

        logger.debug("Received frame taken at: {}".format(raw_frame.taken_at))

        await queue_raw_frame(raw_frame)

        response_status_code = 200
        response_content = {"success": "Raw frame successfully posted"}

        return JSONResponse(content=response_content, status_code=response_status_code)

    except json.JSONDecodeError:
        logger.error(JSON_DECODE_ERROR)
        response_status_code = 400
        response_content = {"error": JSON_DECODE_ERROR}

    except KeyError as e:
        logger.error(KEY_ERROR.format(e))
        response_status_code = 400
        response_content = {"error": JSON_DECODE_ERROR}

    except Exception as e:
        logger.error(e)
        raise e
