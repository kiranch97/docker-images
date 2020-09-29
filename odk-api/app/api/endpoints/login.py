import json
from typing import Any
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, QR_LOGIN_STRING
from app.core.security import create_access_token
from app.db.session import get_db

from app import models
from app import schemas
from app import crud

router = APIRouter()

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
