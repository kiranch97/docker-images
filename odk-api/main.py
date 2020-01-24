import os
import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.responses import JSONResponse
from odklib.DatabaseManager import DatabaseManager
from odklib.DiskWriter import DiskWriter
from odklib.StreamLogger import StreamLogger
from odklib.FrameBroker import FrameBroker

# TODO: change from string to dict with user, password, domain...
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_CONNECTION_STRING')
print(SQLALCHEMY_DATABASE_URI)
WAIT_FRAME_BROKER = 0.01  # in seconds 0.01 = 10 ms

app = FastAPI()
broker = FrameBroker()
# disk_writer = DiskWriter()
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


@app.get("/")
def index():
    return {
        "status": "succes",
        "message": "odk-video.stadswerken.amsterdam"
    }

# ==== WebSocket endpoints ====


@app.websocket("/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Get data from client
            frame_data = await ws.receive_json()

            if frame_data["img"] is not False:
                await broker.send_message_on_queues(frame_data)
    except WebSocketDisconnect:
        logger.info("WebSocket /stream [disconnect]")

# DISABLED
# @app.websocket("/dash_stream")
# async def ws_dashboard(websocket: WebSocket):
#     await broker.connect_to_websocket(websocket)
#     try:
#         while True:
#             # receive text from dashboard ( NEEDED? )
#             data = await websocket.receive_text()
#             # await websocket.send_text(f" Got data from dash: {data}")
#             pass
#     except WebSocketDisconnect:
#         broker.remove_websocket(websocket)


# ==== REST endpoints ====


@app.get("/detected_objects")
def get_detected_objects(app_id: str, day: str):
    status_code = 200
    r_do = dbm.get_detected_objects(app_id, day)
    if r_do["status"] == "error":
        status_code = 500
    return JSONResponse(content = r_do, status_code = status_code)


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
    if r_dsd["status"] == "error":
        status_code = 500
    return JSONResponse(content = r_dsd,status_code = status_code)


@app.get("/dash_total")
def get_dash_total(day: str):
    status_code = 200
    r_dt = dbm.get_dash_total(day)
    if r_dt["status"] == "error":
        status_code = 500
    return JSONResponse(content = r_dt,status_code = status_code)


@app.get("/dash_map_data")
def get_dash_map_data(day: str):
    status_code = 200
    r_dmd = dbm.get_dash_map_data(day)
    if r_dmd["status"] == "error":
        status_code = 500
    return JSONResponse(content = r_dmd,status_code = status_code)


if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8090, workers=1)
