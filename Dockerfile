FROM python:3.11.0-alpine

# Disable debian warnings!
ENV DEBIAN_FRONTEND noninteractive

# Set the default directory where CMD will execute
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# System Deps
# RUN apt-get update && apt-get install && apt-get clean

# Requirements.txt alone for caching
ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# ADD . /usr/src/app/