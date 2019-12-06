from pydantic import BaseModel
from datetime import datetime

""" We use pydantic models to validate the incoming and outgoing data

    NOTE: internal we use SQLAlchemy ORM classes

"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str = None

# TODO


class User(BaseModel):
    id: str
    name: str
    created_at: str = None

# TODO


class Session(BaseModel):
    id: str
    name: str
    created_at: str = None
    info: dict = {}


class AnalysedFrameData(BaseModel):
    # TODO: give needed input by removing the default values
    # created_at: datetime = None
    # created_by_app: str = None
    frame_meta: dict = {}
    detected_objects: list = []
    counts: dict = {}
    ml_done_at: datetime = None
    ml_time_taken: str = None
    take_frame: dict = {}
