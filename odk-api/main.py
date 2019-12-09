from datetime import datetime, timedelta
import os

import uvicorn as uvicorn

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from starlette.templating import Jinja2Templates

from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

# for login
from passlib.context import CryptContext

from jwt import PyJWTError
import jwt

# from aiofile import AIOFile, Writer

from io_models import Token, TokenData, User, AnalysedFrameData
from odklib.DatabaseManager import DatabaseManager

from odklib.DiskWriter import DiskWriter
from odklib.StreamLogger import StreamLogger
from odklib.FrameBroker import FrameBroker

# SETTINGS #

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # noqa
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_CONNECTION_STRING')
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8090"
]
TEST_USER_PASSWORD = "testodk"
WAIT_FRAME_BROKER = 0.01  # in seconds 0.01 = 10 ms

# SETUP #

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# set cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# broker to exchange data among websockets channels
broker = FrameBroker()
diskwriter = DiskWriter()
streamlogger = StreamLogger()

# AUTH #


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(name: str):

    # return User()
    pass


def authenticate_user(name: str, password: str):

    # TODO
    # for now check basic user

    if name == "TEST_USER" and password == TEST_USER_PASSWORD:
        return User(name="testuser", created_at=None)
    else:
        False


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_jwt_user(token: str = Depends(oauth2_scheme)):

    """ Get current user from JWT token

    """

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        name: str = payload.get("identity")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)

    except PyJWTError:
        raise credentials_exception
    user = get_user(name=token_data.name)
    if user is None:
        raise credentials_exception

    return user


async def check_authorized_user(current_user: User = Depends(get_jwt_user)):

    """ This function get user from JWT token, if not found returns an error

    Protects an endpoint

    """

    return current_user


def generate_jwt(form_data):

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"identity": user.name}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# GLOBALS


running_clients = {}  # Dictionary for running streams
stats = {}  # Dictionary for frame statistics

# ROUTES #


@app.get("/")
def index():
    return {
        "status": "succes",
        "message": "odk-video.stadswerken.amsterdam"
    }

# ==== websocket endpoints ====


@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Get data from client
        frame_data = await websocket.receive_json()

        # streamlogger.active_streams_check(
        #     frame_data, running_clients)
        # diskwriter.fill_stats_dict(stats)
        # diskwriter.count_all_files(stats)
        # diskwriter.count_yearly_files(stats)
        # diskwriter.count_monthly_files(stats)
        # diskwriter.count_today_files(stats)

        if frame_data["img"] is not False:
            # await diskwriter.save_file(frame_data)
            # await diskwriter.count_app_id_today_files(
            #     frame_data, running_clients, stats)
            await broker.send_message_on_queues(
                frame_data, stats, running_clients)

        # if len(running_clients.keys()) > 1:
            # print(stats)
            # print(running_clients)


@app.websocket("/dash_stream")
async def websocket_dash_endpoint(websocket: WebSocket):
    await broker.connect_to_websocket(websocket)
    try:
        while True:
            # receive text from dashboard ( NEEDED? )
            data = await websocket.receive_text()
            # await websocket.send_text(f" Got data from dash: {data}")
            pass
    except WebSocketDisconnect:
        broker.remove_websocket(websocket)

# ==== REST endpoints ====

dbm = DatabaseManager(SQLALCHEMY_DATABASE_URI)


@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    return generate_jwt(form_data)


# ----


@app.get("/detected_objects")
def get_detected_objects(app_id: str, day: str):
    r_do = dbm.get_detected_objects(app_id, day)

    return r_do


# ----


@app.get("/last_analysed_frames")
def get_last_analysed_frames(app_id: str):
    r_laf = dbm.get_last_analysed_frames(app_id)

    return r_laf


# ----


@app.get("/dash_stream_devices")
def get_dash_stream_devices(app_id: str, day: str):
    r_dsd = dbm.get_dash_stream_devices(app_id, day)

    return r_dsd


# ----

@app.get("/dash_total")
def get_dash_total(day: str):
    r_dt = dbm.get_dash_total(day)

    return r_dt


# ----

# TEST SERVER
if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=8090, workers=1)
