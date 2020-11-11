from typing import Dict
from app.logic.utils import correct_date_string
import json

from loguru import logger
from fastapi import APIRouter, WebSocket, Depends, HTTPException
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketDisconnect

from app.log.messages import JSON_DECODE_ERROR, KEY_ERROR
from app.broker.producer import queue_raw_frame
from app.logic.users import get_current_active_user

from app import schemas

router = APIRouter()


def _create_raw_frame(data_incoming: Dict) -> schemas.RawFrame:
    raw_frame = schemas.RawFrame(
        img=data_incoming["img"],
        taken_at=correct_date_string(data_incoming["timestamp"]),
        lat_lng={"lat": data_incoming["lat"], "lng": data_incoming["lng"]},
        stream_id=data_incoming["stream_id"],
        stream_meta={
            "user_type": data_incoming.get("user_type") or "",
            "vehicle_type": data_incoming.get("vehicle_type") or "",
            "user_id": data_incoming.get("user_id") or "",
        },
    )
    return raw_frame


@router.websocket("/stream")
async def stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        while True:
            # 1) Retrieve raw frame
            stream_data = await websocket.receive_json()

            # 2) Build RawFrame object
            raw_frame = _create_raw_frame(stream_data)
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
        raw_frame = _create_raw_frame(frame_dict)
        logger.debug("Received frame taken at: {}".format(raw_frame.taken_at))

        await queue_raw_frame(raw_frame)

        response_status_code = 200
        response_content = {"success": "Raw frame successfully posted"}

        return JSONResponse(content=response_content, status_code=response_status_code)

    except json.JSONDecodeError:
        message = JSON_DECODE_ERROR
        logger.error(message)
        raise HTTPException(status_code=400, detail=message)

    except KeyError as e:
        message = KEY_ERROR.format(e)
        logger.error(message)
        raise HTTPException(status_code=400, detail=message)

    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
