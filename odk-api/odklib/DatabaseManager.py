""" avatarslib.AvatarManager

"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from odklib.AnalysedFrame import AnalysedFrame
# import AnalysedFrame


import logging


class DatabaseManager():

    # SETTINGS #

    RETURN_CODES = {'ERROR': 1,
                    'ERROR_SERVER_ERROR': 2,
                    'ERROR_INVALID_INPUT': 3
                    }

    # END SETTINGS #

    # postgresql://{{USER}}:{{PASSWORD}}@{{IP}}:{{PORT}}/{{DB_NAME}}
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

        """ Add analysed frame

        :return: status dict { status : ['error','succes'], message }

        """

        if not self.has_connection:
            return {"status": "error", "message": "There is a server problem! \
                     Please contact administrator"}

        if type(analysed_frame_data) is dict:

            new_analysed_frame = AnalysedFrame(
                created_at=analysed_frame_data.get(
                    'take_frame', {}).get(
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
                take_frame=analysed_frame_data.get(
                    'take_frame'),
                )

            try:
                self.db_session.add(new_analysed_frame)
                self.db_session.commit()

                new_analysed_dict = new_analysed_frame.to_public_dict()

                return {"status": "success",
                        "message": "Created frame!",
                        "data": new_analysed_dict}
                # This time only we send over the raw passphrase

            except Exception as e:
                self.logger.error(e)
                return {"status": "error",
                        "message": "There is a server problem! \
                                    Please contact administrator"}

        else:
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_INVALID_INPUT'],
                    "message": "Cannot create analysed frame: invalid input!"}

    # ----

    def get_detected_objects(self, app_id: str, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            day = day.split(" ")[0]
            analysed_frames_by_app_id = \
                self.db_session.query(AnalysedFrame).filter(
                    AnalysedFrame.created_by_app == app_id).filter(
                        AnalysedFrame.created_at >= day).all()

            detected_objects_by_type = {}

            for frame in analysed_frames_by_app_id:

                for detected_obj in frame.detected_objects:

                    type = detected_obj.get("detected_object_type")

                    if type not in detected_objects_by_type.keys():
                        detected_objects_by_type[type] = 0

                    detected_objects_by_type[type] += 1

            return {
                    "_entity_name": "detected_objects",
                    "app_id": app_id,
                    "day": day,
                    "detected_objects_by_type": detected_objects_by_type
                   }

        except Exception as e:
            self.logger.error(e)
            return []

    # ----

    def get_last_analysed_frames(self, app_id: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            frame = self.db_session.query(AnalysedFrame).filter(
                AnalysedFrame.created_by_app == app_id).order_by(
                    AnalysedFrame.created_at.desc()).first()

            frame.to_public_dict()

            return frame

        except Exception as e:
            self.logger.error(e)
            return []

    # ----

    def get_dash_stream_devices(self, app_id: str, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            dash_stream_devices = {}
            app_ids = []
            if "+" in app_id:
                app_ids = app_id.split("+")
            else:
                app_ids.append(app_id)
            day = day.split(" ")[0]
            for stream_id in app_ids:

                detected_objects_by_type = {}

                analysed_frames_by_app_id = \
                    self.db_session.query(AnalysedFrame).filter(
                        AnalysedFrame.created_by_app == stream_id).filter(
                            AnalysedFrame.created_at >= day).all()

                last_analysed_frame_by_app_id = \
                    self.db_session.query(AnalysedFrame).filter(
                        AnalysedFrame.created_by_app == stream_id).filter(
                            AnalysedFrame.created_at >= day).order_by(
                                AnalysedFrame.created_at.desc()).first()

                for frame in analysed_frames_by_app_id:

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
                    "app_id":
                        stream_id,
                    "day":
                        day,
                    "analysed_img":
                        last_analysed_frame_by_app_id.take_frame.get("img"),
                    "detected_objects":
                        last_analysed_frame_by_app_id.detected_objects,
                    "detected_objects_by_type":
                        detected_objects_by_type
                }

            return dash_stream_devices

        except Exception as e:
            self.logger.error(e)
            return []

    # ----

    def get_dash_total(self, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            day = day.split(" ")[0]
            analysed_frames = \
                self.db_session.query(AnalysedFrame).filter(
                    AnalysedFrame.created_at >= day).all()

            detected_objects_by_type = {}

            for frame in analysed_frames:

                for detected_obj in frame.detected_objects:

                    if "total" not in detected_objects_by_type.keys():
                        detected_objects_by_type["total"] = 0

                    type = detected_obj.get("detected_object_type")

                    if type not in detected_objects_by_type.keys():
                        detected_objects_by_type[type] = 0

                    detected_objects_by_type[type] += 1
                    detected_objects_by_type["total"] += 1

            return {
                    "_entity_name": "dash_total",
                    "day": day,
                    "detected_objects_by_type": detected_objects_by_type
                   }

        except Exception as e:
            self.logger.error(e)
            return []

    # ----

    def get_dash_map_data(self, day: str):

        if not self.has_connection:
            self.logger.error("No connection to database! Check Settings")
            return {"status": "error",
                    "code": self.RETURN_CODES['ERROR_SERVER_ERROR'],
                    "message": "Cannot get analysed frames. \
                                Problem with server!"}

        try:
            dash_map_data = {}
            day = day.split(" ")[0]
            analysed_frames = \
                self.db_session.query(AnalysedFrame).filter(
                    AnalysedFrame.created_at >= day).all()

            for frame in analysed_frames:

                location = {}
                
                if "lat" not in location.keys():
                    location["lat"] = ""

                if "lng" not in location.keys():
                    location["lng"] = ""
                
                location["lat"] = frame.take_frame.get("lat")
                location["lng"] = frame.take_frame.get("lng")

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
                    "app_id":
                        frame.created_by_app,
                    "created_at":
                        frame.created_at,
                    # "analysed_img":
                    #     frame.take_frame.get("img"),
                    "location":
                        location,
                    "detected_objects_by_type": 
                        detected_objects_by_type
                }

            return dash_map_data
        
        except Exception as e:
            self.logger.error(e)
            return []