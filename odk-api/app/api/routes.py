from app import models
import json
from typing import Any, Dict
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

from loguru import logger
from fastapi import APIRouter, WebSocket, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.websockets import WebSocketDisconnect
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, QR_LOGIN_STRING
from app.core.security import create_access_token
from app.models.frame import RawFrame
from app.log.messages import JSON_DECODE_ERROR, KEY_ERROR
from app.broker.outgoing import queue_raw_frame
from app.db.session import get_db
from app.logic.services import get_detected_objects

from app import schemas
from app import crud
from app.logic.users import get_current_active_user

router = APIRouter()


@router.websocket("/stream")
async def stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        while True:
            # 1) Retrieve raw frame
            stream_data = await websocket.receive_json()

            # 2) Build RawFrame object
            raw_frame = RawFrame(
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

    except JSONDecodeError:
        logger.error(JSON_DECODE_ERROR)

    except KeyError as e:
        logger.error(KEY_ERROR.format(e))

    except Exception as e:
        logger.error(e)
        raise e


# TODO: remove and replace with proper JWT authentication feature
@router.get("/authorized_login")
def check_credentials(credential_string: str) -> JSONResponse:
    status_code: int = 500
    content: dict = {}
    try:
        # credentials = credential_string.split("/")

        credentials = json.loads(credential_string)

        if credentials['s'] == QR_LOGIN_STRING:
            content = {
                "success": "Login successful",
                "vehicle_type": credentials['v'],
                "user_id": credentials['u'],
            }
            status_code = 200
        else:
            content = {"error": "Login can not be verified"}
            status_code = 400

    except Exception as e:
        status_code = 400
        content = {"error": str(e)}

    finally:
        return JSONResponse(content=content, status_code=status_code)


@router.get("/detected_objects")
async def detected_objects(stream_id: str, day: str, db: Session = Depends(get_db)) -> Dict:
    try:
        start_date = datetime.strptime(day, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)

        detected_objects = get_detected_objects(
            db=db, stream_id=stream_id, _from=start_date, _till=end_date
        )
        logger.debug("Returning detected objects from '{}' till '{}' of stream_id '{}'".format(
            start_date, end_date, stream_id
        ))
        return detected_objects

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Detected objects count could not be retrieved"
        )


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authentication(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/users/me", response_model=schemas.User)
def get_current_user(
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    return current_user