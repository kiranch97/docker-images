import logging
import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# from twilio.rest import Client

from odklib.AnalysedFrame import AnalysedFrame


# account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
# client = Client(account_sid, auth_token)


class DatabaseManager:
    RETURN_CODES = {'ERROR': 1,
                    'ERROR_SERVER_ERROR': 2,
                    'ERROR_INVALID_INPUT': 3
                    }

    db_uri = None
    db_engine = None
    db_session = None
    has_connection = False
    logger = None

    def __init__(self, uri=None):

        self.setup_logger()

        if uri is None:
            self.logger.error(
                """Cannot work with DatabaseManager without a SQLAlchemy connection URI
                """)

        else:
            self.db_uri = uri
            self.db_engine = create_engine(self.db_uri, echo=False)
            db_session_maker = sessionmaker()
            db_session_maker.configure(bind=self.db_engine)
            self.db_session = db_session_maker()

            self.test_connection()
            self.setup_database()

    # ----

    def setup_logger(self):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)

        try:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s %(name)s %(levelname)-4s %(message)s')
            handler.setFormatter(formatter)

            if (self.logger.hasHandlers()):  # see: http://tiny.cc/v5w6gz
                self.logger.handlers.clear()

            self.logger.addHandler(handler)

        except Exception as e:
            self.logger.error(e)

    # ----

    def setup_database(self):

        if self.has_connection:

            try:
                AnalysedFrame().create_table(self.db_engine)
                self.logger.info("Setup database with analysed frames")
            except Exception as e:
                self.logger.error("Error setting up database: {0}".format(e))

    # ----

    def test_connection(self):

        if self.db_engine is None:
            self.logger.error("Cannot connect to a database. \
                               Check the SQLAlchemy URI in settings!")
            return False

        try:
            self.db_engine.connect()
            self.has_connection = True
            self.logger.info("Succesfully connected to database!")
        except Exception as e:
            self.logger.error("Cannot connect to a database. \
                               Check the SQLAlchemy URI in settings!: \
                               {0}".format(e))

    # ----

    def get_analysed_frame(self, id):

        frame = self.db_session.query(AnalysedFrame).filter(
            AnalysedFrame.id == id).first()

        return frame

    # ----

    def add_analysed_frame(self, analysed_frame_data):

        # TODO: should this check be here?
        if not self.has_connection:
            return {
                "status": "error",
                "message": "There is a server problem! Please contact administrator"
            }

        if type(analysed_frame_data) is not dict:
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_INVALID_INPUT'],
                    "message": "Cannot create analysed frame: invalid input!"}

        # TODO: for now storing location data here,
        #  data model should be reviewed to handle more variable information from services

        # location_data = analysed_frame_data.get('location')
        # analysed_frame_data['take_frame']['location'] = location_data

        new_analysed_frame = AnalysedFrame(
            stream_id=analysed_frame_data.get(
                'stream_id'),
            created_at=analysed_frame_data.get(
                'timestamp'),
            frame_meta=analysed_frame_data.get(
                'frame_meta'),
            detected_objects=analysed_frame_data.get(
                'detected_objects'),
            counts=analysed_frame_data.get(
                'counts'),
            ml_done_at=analysed_frame_data.get(
                'ml_done_at'),
            ml_time_taken=analysed_frame_data.get(
                'ml_time_taken'),
            location=analysed_frame_data.get(
                'location'),
            frame_name=analysed_frame_data.get(
                'frame_name'),
            vehicle_type=analysed_frame_data.get(
                'vehicle_type'),
            driver_phone_number=analysed_frame_data.get(
                'driver_phone_number')
        )

        # new_analysed_frame = AnalysedFrame(
        #     created_at=analysed_frame_data.get(
        #         'take_frame', {}).get(
        #             'timestamp'),
        #     frame_meta=analysed_frame_data.get(
        #         'frame_meta'),
        #     detected_objects=analysed_frame_data.get(
        #         'detected_objects'),
        #     counts=analysed_frame_data.get(
        #         'counts'),
        #     ml_done_at=analysed_frame_data.get(
        #         'ml_done_at'),
        #     ml_time_taken=analysed_frame_data.get(
        #         'ml_time_taken'),
        #     frame_name=analysed_frame_data.get(
        #         'frame_name'),
        #     user_type=analysed_frame_data.get(
        #         'user_type'),
        #     take_frame=analysed_frame_data.get(
        #         'take_frame'),
        # )

        try:
            self.db_session.add(new_analysed_frame)
            self.db_session.commit()

            new_analysed_dict = new_analysed_frame.to_public_dict()

            # body = json.dumps(analysed_frame_data)
            # from_whatsapp_number = "whatsapp:+14155238886"
            # to_whatsapp_number = "whatsapp:+31{}".format(analysed_frame_data["vehicle_number"])
            # client.messages.create(body=body,
            #                        from_=from_whatsapp_number,
            #                        to=to_whatsapp_number)

            return {"status": "success",
                    "message": "Created frame!",
                    "data": new_analysed_dict}

        except Exception as e:
            self.logger.error(e)
            return {"status": "error",
                    "message": "There is a server problem! Please contact administrator"}

    # ----

    def get_detected_objects(self, stream_id: str, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            day = day.split(" ")[0]
            analysed_frames_by_stream_id = \
                self.db_session.query(AnalysedFrame).filter(
                    AnalysedFrame.stream_id == stream_id).filter(
                    AnalysedFrame.created_at >= day).all()

            detected_objects_by_type = {}

            for frame in analysed_frames_by_stream_id:

                for detected_obj in frame.detected_objects:

                    type = detected_obj.get("detected_object_type")

                    if type not in detected_objects_by_type.keys():
                        detected_objects_by_type[type] = 0

                    detected_objects_by_type[type] += 1

            return {
                "_entity_name": "detected_objects",
                "stream_id": stream_id,
                "day": day,
                "detected_objects_by_type": detected_objects_by_type
            }

        except Exception as e:
            self.logger.error(e)
            return {
                "status": "error",
                "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                "message": e
            }

    # ----

    def get_last_analysed_frames(self, stream_id: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            frame = self.db_session.query(AnalysedFrame).filter(
                AnalysedFrame.stream_id == stream_id).order_by(
                AnalysedFrame.created_at.desc()).first()

            frame.to_public_dict()

            return frame

        except Exception as e:
            self.logger.error(e)
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": e
                    }

    # ----

    def get_dash_stream_devices(self, stream_id: str, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            dash_stream_devices = {}
            stream_ids = []
            if "+" in stream_id:
                stream_ids = stream_id.split("+")
            else:
                stream_ids.append(stream_id)
            day = day.split(" ")[0]
            for stream_id in stream_ids:

                detected_objects_by_type = {}

                analysed_frames_by_stream_id = \
                    self.db_session.query(AnalysedFrame).filter(
                        AnalysedFrame.stream_id == stream_id).filter(
                        AnalysedFrame.created_at >= day).all()

                last_analysed_frame_by_stream_id = \
                    self.db_session.query(AnalysedFrame).filter(
                        AnalysedFrame.stream_id == stream_id).filter(
                        AnalysedFrame.created_at >= day).order_by(
                        AnalysedFrame.created_at.desc()).first()

                for frame in analysed_frames_by_stream_id:

                    for detected_obj in frame.detected_objects:

                        if "total" not in detected_objects_by_type.keys():
                            detected_objects_by_type["total"] = 0

                        type = detected_obj.get("detected_object_type")

                        if type not in detected_objects_by_type.keys():
                            detected_objects_by_type[type] = 0

                        detected_objects_by_type[type] += 1
                        detected_objects_by_type["total"] += 1

                dash_stream_devices[stream_id] = {
                    "_entity_name":
                        "dash_stream_devices",
                    "stream_id":
                        stream_id,
                    "day":
                        day,
                    "analysed_img":
                        last_analysed_frame_by_stream_id.take_frame.get("img"),
                    "detected_objects":
                        last_analysed_frame_by_stream_id.detected_objects,
                    "detected_objects_by_type":
                        detected_objects_by_type
                }

            return dash_stream_devices

        except Exception as e:
            self.logger.error(e)
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": e
                    }

    # ----

    def get_dash_day_total(self, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            analysed_frames = \
                self.db_session.query(AnalysedFrame).filter(
                    AnalysedFrame.created_at >= day).all()

            detected_objects_by_type = {}

            for frame in analysed_frames:

                for detected_obj in frame.detected_objects:

                    if "total" not in detected_objects_by_type.keys():
                        detected_objects_by_type["total"] = 0

                    type = detected_obj.get("detected_object_type")

                    if type == "container_small" \
                            or type == "cardboard" \
                            or type == "garbage_bag":
                        if type not in detected_objects_by_type.keys():
                            detected_objects_by_type[type] = 0

                        detected_objects_by_type[type] += 1
                        detected_objects_by_type["total"] += 1

            return {
                "_entity_name": "get_dash_day_total",
                "day": day,
                "detected_objects_by_type": detected_objects_by_type
            }

        except Exception as e:
            self.logger.error(e)
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": e
                    }

    # ----

    def get_dash_map_data(self, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            analysed_frames = \
                self.db_session.query(AnalysedFrame).filter(
                    AnalysedFrame.created_at >= day).order_by(
                    AnalysedFrame.created_at.desc()).all()

            dash_map_data = {}

            for frame in analysed_frames:

                detected_objects_by_type = {}

                for detected_obj in frame.detected_objects:

                    if "total" not in detected_objects_by_type.keys():
                        detected_objects_by_type["total"] = 0

                    type = detected_obj.get("detected_object_type")

                    if type not in detected_objects_by_type.keys():
                        detected_objects_by_type[type] = 0

                    detected_objects_by_type[type] += 1
                    detected_objects_by_type["total"] += 1

                dash_map_data[frame.id] = {
                    "_entity_name":
                        "dash_map_data",
                    "frame_id":
                        frame.id,
                    "stream_id":
                        frame.stream_id,
                    "created_at":
                        frame.created_at.strftime("%H:%M:%S"),
                    "location":
                        frame.take_frame.get("location"),
                    "detected_objects_by_type":
                        detected_objects_by_type
                }

            return dash_map_data

        except Exception as e:
            self.logger.error(e)
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": e
                    }
