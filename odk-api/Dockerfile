FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Stan Guldemond <s.guldemond@amsterdam.nl>"

RUN pip install --upgrade pip

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV API_PREFIX /

# copy `./app` to `/app/app`, because else it can not be found
COPY ./app /app/app
