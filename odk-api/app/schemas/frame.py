from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class FrameBase(BaseModel):
    taken_at: datetime
    lat_lng: Dict[str, float]

    stream_id: str
    stream_meta: Dict[str, str] = {}


class RawFrame(FrameBase):
    """
    A `RawFrame` is created from data received by typically the ODK app,
    or through an another form of transferring image data to the API.
    A `RawFrame` object is transferred as is to the message queue to be analysed.
    """

    # image encoded in base64
    img: str


class AnalysedFrame(FrameBase):
    """
    An `AnalysedFrame` is the continuation of a `RawFrame` in the data flow,
    exclusing the image data,
    including data added by a frame analyser,
    of which most importantly `detected_objects`.

    This model is used to store the collection of this data in a database.
    """
    id: str

    classification: Dict[str, List[float]]
    detected_objects: Dict[str, str]
    object_count: Dict[str, int]

    img_meta: Dict[str, str]
    analyser_meta: Dict[str, str]
