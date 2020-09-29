from typing import Dict
from datetime import datetime, timedelta

from loguru import logger
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.logic.services import get_detected_objects

from app import models
from app import schemas
from app import crud

router = APIRouter()


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
