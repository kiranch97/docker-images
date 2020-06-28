import logging
import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from odklib.DatabaseManager import DatabaseManager
from odklib.DiskWriter import DiskWriter
from odklib.FrameBroker import FrameBroker

# TODO: change from string to dict with user, password, domain...
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_CONNECTION_STRING')
WAIT_FRAME_BROKER = 0.01  # in seconds 0.01 = 10 ms

app = FastAPI(openapi_prefix=os.environ.get('API_PREFIX', '/'))
broker = FrameBroker()
disk_writer = DiskWriter()
# stream_logger = StreamLogger()

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)-4s %(message)s')


# TODO: move to init function, include: setup queues + setup logging
dbm = DatabaseManager(SQLALCHEMY_DATABASE_URI)

# set cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==== endpoints ====

@app.get("/")
def index():
    return {
        "status": "succes",
        "message": "odk-video.stadswerken.amsterdam"
    }


# ==== WebSocket endpoints ====


@app.websocket("/stream-login")
async def ws_stream(ws: WebSocket):
    # Accept connection
    await ws.accept()

    try:
        while True:
            # Receive message (string/vehicle_type/number)
            login_data = await ws.receive_json()
            message = login_data["message"].split("/")

            # Get password from environment variables
            password = os.environ.get('QR_LOGIN_PASSWORD')

            # Check if string == password,
            # if so, send back success message,
            # else send error
            if message[0] == password:
                try:
                    content = {"success": "Login successful"}
                    await ws.send_json(content)
                except ConnectionError:
                    content = {"error": "LoginServer Not Available"}
                    await ws.send_json(content)
            else:
                try:
                    content = {"error": "Login can not be verified"}
                    await ws.send_json(content)
                except ConnectionError:
                    content = {"error": "LoginServer Not Available"}
                    await ws.send_json(content)

            # Clear message array
            message = []

    except WebSocketDisconnect:
        logger.info("WebSocket /stream [disconnect]")
    except Exception as e:
        logger.info(e)



@app.websocket("/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    await ws.send_text("Connection accepted")

    try:
        while True:
            # Get data from client
            frame_data = await ws.receive_json()

            if frame_data["img"] is not False:
                try:
                    await broker.send_message_on_queues(frame_data)
                except ConnectionError:
                    content = {"error": "MessageServer Not Available"}
                    await ws.send_json(content)
    except WebSocketDisconnect:
        logger.info("WebSocket /stream [disconnect]")
    except Exception as e:
        logger.info(e)

# ==== REST endpoints ====


@app.get("/detected_objects")
def get_detected_objects(app_id: str, day: str):
    status_code = 200
    r_do = dbm.get_detected_objects(app_id, day)
    if "status" in r_do and r_do["status"] == "error":
        status_code = 500
    return JSONResponse(content=r_do, status_code=status_code)


@app.get("/last_analysed_frames")
def get_last_analysed_frames(app_id: str):
    # TODO: store a single analysed frame in server memory which app can retrieve
    # r_laf = dbm.get_last_analysed_frames(app_id)
    # return r_laf
    return None


@app.get("/dash_stream_devices")
def get_dash_stream_devices(app_id: str, day: str):
    status_code = 200
    r_dsd = dbm.get_dash_stream_devices(app_id, day)
    if "status" in r_dsd and r_dsd["status"] == "error":
        status_code = 500
    return JSONResponse(content=r_dsd, status_code=status_code)


@app.get("/dash_day_total")
def get_dash_day_total(day: str):
    status_code = 200
    r_ddt = dbm.get_dash_day_total(day)

    if "status" in r_ddt and r_ddt["status"] == "error":
        status_code = 500
    return JSONResponse(content=r_ddt, status_code=status_code)


@app.get("/dash_map_data")
def get_dash_map_data(day: str):
    status_code = 200
    r_dmd = dbm.get_dash_map_data(day)
    if "status" in r_dmd and r_dmd["status"] == "error":
        status_code = 500
    return JSONResponse(content=r_dmd, status_code=status_code)


if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8090, workers=1)
