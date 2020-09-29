import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.base_class import Base


class AnalysedFrame(Base):
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
