FROM python:3.9-slim-buster

# RUN apt-get update && apt-get install python3-dbus libdbus-1-dev libgirepository1.0-dev &&
#     pip install gatt dbus-python gobject PyGObject

RUN apt-get update && apt-get install -y \
    build-essential \
    bluez \
    bluez-tools \
    git \
    libglib2.0-dev \
    libboost-python-dev \
    libboost-thread-dev \
    libbluetooth-dev

RUN pip install setuptools==57.5.0 && \
    pip install gattlib pyyaml && \
    pip install \
        beacontools==2.1.0 \
        requests==2.28.1

RUN pip install pybluez

#git+https://github.com/tonyfettes/pybluez.git

WORKDIR /usr/src/app


