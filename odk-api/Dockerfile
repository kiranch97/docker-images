FROM tiangolo/uvicorn-gunicorn:python3.7

# LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"
ENV API_PREFIX /
ENV DATABASE_CONNECTION_STRING postgresql://postgres:mysecretpassword@odk-db/odk
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY ./app /app
