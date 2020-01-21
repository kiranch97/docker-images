import os
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi import Depends, HTTPException

from io_models import Token, TokenData, User

# for login
from passlib.context import CryptContext

from jwt import PyJWTError
import jwt

SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # noqa
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
TEST_USER_PASSWORD = "testodk"

CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8090"
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

templates = Jinja2Templates(directory="templates")


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


@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    return generate_jwt(form_data)

