ARG NODE_VERSION=16.20.2
ARG PYTHON_VERSION=3.11.8


FROM node:${NODE_VERSION}-bookworm-slim as frontend

ARG VUE_APP_ROOT_API=/api

WORKDIR /build

COPY ./client .
RUN npm ci --no-audit --ignore-scripts
RUN npm run build


FROM python:${PYTHON_VERSION}-slim-bookworm as build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends gettext git gcc g++
RUN pip install --upgrade pip setuptools cython

COPY ./api/requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt


FROM python:${PYTHON_VERSION}-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV RUN_FEED=no
ENV RUN_MIGRATION=yes
ENV RUN_DEV_SERVER=no
ENV RUN_COMPILE_MESSAGES=yes
ENV RUN_COLLECT_STATIC=no
ENV RUN_CREATE_SUPER_USER=yes
ENV DEBIAN_FRONTEND=noninteractive
ENV IS_CONTAINERIZED=True

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    nginx xz-utils gettext

ARG S6_OVERLAY_VERSION=3.1.2.1
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME 0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

ENTRYPOINT ["/init"]

WORKDIR /var/www

COPY --from=build /root/.local /root/.local
COPY docker/nginx/nginx.conf /etc/nginx/sites-available/default
COPY docker/s6-rc.d /etc/s6-overlay/s6-rc.d
COPY --from=frontend /build/dist /var/www/html

COPY ./api/paul_api/ /var/www/paul_api/

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

EXPOSE 80
