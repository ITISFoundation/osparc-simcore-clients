ARG PYTHON_VERSION="3.6.10"
FROM python:${PYTHON_VERSION}-slim-buster as base

RUN apt-get -y update
RUN apt-get -y install \
    git \
    make

WORKDIR /work
COPY . /work

RUN mkdir .git\
    && make .env \
    && pip install --upgrade \
        pip \
        wheel\
        setuptools \
    && pip install -r requirements-dev.txt \
    && pip install -r requirements-tests.txt \
    && pip install .
