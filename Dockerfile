FROM python:3

# RUN apt-get update && apt-get install python3-dbus libdbus-1-dev libgirepository1.0-dev &&
#     pip install gatt dbus-python gobject PyGObject

RUN apt-get update && apt-get install -y \
    build-essential \
    bluez \
    bluez-tools \
    libglib2.0-dev \
    libboost-python-dev \
    libboost-thread-dev \
    libbluetooth-dev && \
    pip install pybluez gattlib pyyaml
