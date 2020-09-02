from typing import List, Tuple, Dict
from datetime import datetime
import uuid

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.base_class import Base


class RawFrame(BaseModel):
    """
    A `RawFrame` is created from data received by typically the ODK app,
    or through an another form of transferring image data to the API.
    A `RawFrame` object is transferred as is to the message queue to be analysed.
    """

    # image encoded in base64
    img: str

    taken_at: datetime
    lat_lng: Dict[str, str]

    stream_id: str
    stream_meta: Dict[str, str] = {}


class AnalysedFrame(Base):
    """
    An `AnalysedFrame` is the continuation of a `RawFrame` in the data flow,
    exclusing the image data,
    including data added by a frame analyser,
    of which most importantly `detected_objects`.

        This model is used to store the collection of this data in a database.
    """

    __tablename__ = "analysed_frames_v1"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    taken_at = Column(DateTime())
    lat_lng = Column(JSONB())
    stream_id = Column(String())

    detected_objects = Column(JSONB())
    object_count = Column(JSONB())

    # e.g.: user type, vehicle type, driver info
    stream_meta = Column(JSONB())
    # e.g.: frame name, file size, frame size
    img_meta = Column(JSONB())
    # e.g.: done at, time taken
    analyser_meta = Column(JSONB())
