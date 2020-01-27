from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, Text, DateTime, Numeric
from sqlalchemy.dialects.postgresql import JSONB

import datetime
from passlib.context import CryptContext
import uuid
import simplejson as json

DBObj = declarative_base()


class AnalysedFrame(DBObj):

    __tablename__ = "analysed_frames"

    """

    id : str # uuid
    frameMeta: dict = {}
    detectedObjects: list = []
    counts : dict = {}
    mlDoneAt : datetime = None
    mlTimeTaken : datetime = None
    take_frame : dict = {}


    """

    id = Column(String(), primary_key=True)
    created_at = Column(DateTime())
    created_by_app = Column(String())
    frame_meta = Column(JSONB())
    detected_objects = Column(JSONB())
    counts = Column(JSONB())
    ml_done_at = Column(DateTime())
    ml_time_taken = Column(String())
    frame_name = Column(String())
    take_frame = Column(JSONB())

    # ----

    def __init__(self,
                 created_at=None,
                 created_by_app=None,
                 frame_meta={},
                 detected_objects={},
                 counts={},
                 ml_done_at=None,
                 ml_time_taken=None,
                 frame_name=None,
                 take_frame=None
                 ):

        self.id = str(uuid.uuid4())
        if type(take_frame) is dict:
            self.created_at = take_frame.get("timestamp")
            self.created_by_app = take_frame.get("app_id")
        self.frame_meta = frame_meta
        self.detected_objects = detected_objects
        self.counts = counts
        self.ml_done_at = ml_done_at
        self.ml_time_taken = ml_time_taken
        self.frame_name = frame_name
        self.take_frame = None

    # ----

    def __repr__(self):
        # string/unicode representation of object
        return "<AnalysedFrame id='{0}'".format(self.id)

    # ----

    def to_public_dict(self):

        return {"id": self.id,
                "created_at": str(self.created_at),
                "created_by_app": self.created_by_app,
                "frame_meta": self.frame_meta,
                "detected_objects": self.detected_objects,
                "counts": self.counts,
                "ml_done_at": self.ml_done_at,
                "ml_time_taken": self.ml_done_at,
                "frame_name": self.frame_name,
                "take_frame": self.take_frame
                }

    # ----

    def to_private_dict(self):

        return {"id": self.id,
                "created_at": str(self.created_at),
                "created_by_app": self.created_by_app,
                "frame_meta": self.frame_meta,
                "detected_objects": self.detected_objects,
                "counts": self.counts,
                "ml_done_at": self.ml_done_at,
                "ml_time_taken": self.ml_done_at,
                "frame_name": self.frame_name,
                "take_frame": self.take_frame
                }

    # ----

    def to_json(self):
        return json.dumps(self.to_dict())

    # ----

    def create_table(self, engine):

        if not engine:
            self.logger.error("create_table: Please supply engine")
            return False

        try:
            DBObj.metadata.create_all(engine)

        except Exception as e:
            print("ERROR: Can't create table for ApiCentral: {0}".format(
                unicode(e)))
