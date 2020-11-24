#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020 The Authors.
# Authors: Bin Liang  <@liangbin>
#
# Summary: Zeta-manager service Dockerfile
#
# base image
FROM python:3.6-slim

# install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# set working directory
WORKDIR /usr/src/app

# Add app
COPY . /usr/src/app

# Setup app
RUN pip install -r requirements.txt && \
    chmod +x /usr/src/app/entrypoint.sh

# Run app
CMD ["/usr/src/app/entrypoint.sh"]
