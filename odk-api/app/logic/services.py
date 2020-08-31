from typing import Dict
from datetime import datetime

from loguru import logger
from sqlalchemy.exc import DataError, OperationalError
from sqlalchemy.orm import Session

from app.models.frame import AnalysedFrame
from app.db.session import get_session


def persist_analysed_frame(analysed_frame: AnalysedFrame) -> AnalysedFrame:
    try:
        db = get_session()

        db.add(analysed_frame)
        db.commit()
        db.refresh(analysed_frame)

        return analysed_frame

    except DataError as e:
        logger.error(e)

    except OperationalError as e:
        logger.error(e)

    except Exception as e:
        logger.error(e)
        raise e

    finally:
        return AnalysedFrame()


def get_detected_objects(
    db: Session, stream_id: str, _from: datetime, _till: datetime
) -> Dict[str, str]:
    try:
        # 1) get only the object counts per stream_id in the selected time frame
        data = (
            db.query(AnalysedFrame.object_count)
            .filter(AnalysedFrame.stream_id == stream_id)
            .filter(AnalysedFrame.taken_at >= _from)
            .filter(AnalysedFrame.taken_at < _till)
            .all()
        )

    except Exception as e:
        logger.error(e)
        raise e

    # 2) declare dict for combining counts
    counts: Dict[str, str] = {}

    # 3) loop through every object counts
    for d in data:
        # 4) the counts dict is in the first and only element
        obj_dict = d[0]

        # 5) loop through the dict
        for key, value in obj_dict.items():
            # 6.1) if the key is known, add the value
            if counts.get(key):
                counts[key] += value
            # 6.2) if not known, create the key and set value
            else:
                counts[key] = value

    return counts
