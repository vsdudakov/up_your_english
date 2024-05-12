# syntax=docker/dockerfile:1.2
FROM python:3.12-alpine

RUN apk update && apk --no-cache add alpine-sdk bash python3-dev postgresql-dev libffi-dev openssh-client

WORKDIR /backend

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY Makefile Makefile

RUN make install

COPY src ./src
