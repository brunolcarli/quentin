FROM python:3.9-alpine

RUN apk add make
RUN apk add --no-cache gcc libc-dev git libffi-dev openssl-dev

RUN mkdir /usr/src/code
WORKDIR /usr/src/code

ENV PYTHONPATH /usr/src/code

COPY quentin/requirements/common.txt .
COPY quentin/requirements/production.txt .
RUN pip3 install -r production.txt


RUN apk del gcc libc-dev git libffi-dev openssl-dev

COPY . .
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV NAME quentin