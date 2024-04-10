###########
# BUILDER #
###########

# pull official base image
FROM python:3.10-alpine as builder

# set work directory
WORKDIR /home/skk/vzr

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install Celery and Redis dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    redis

# install dependencies
RUN pip install gunicorn
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /home/skk/vzr/wheels -r requirements.txt

# Install psycopg2
RUN pip install psycopg2-binary


#########
# FINAL #
#########

# pull official base image
FROM python:3.10-alpine

# create directory for the app user
RUN mkdir -p /home/skk

# create the app user
RUN addgroup -S skk && adduser -S skk -G skk

# create the appropriate directories
ENV HOME=/home/skk
ENV APP_HOME=/home/skk/vzr
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /home/skk/vzr/wheels /wheels
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /home/skk/vzr/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME
