FROM node:16 as build

ARG VUE_APP_ROOT_API=/api

WORKDIR /build

COPY ./client .
RUN npm ci --no-audit --ignore-scripts
RUN npm run build

FROM python:3.10-alpine

ARG S6_OVERLAY_VERSION=3.1.2.1
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME 0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

ENTRYPOINT ["/init"]

ENV DJANGO_SETTINGS_MODULE=paul_api.settings
ENV RUN_FEED="no"
ENV RUN_MIGRATION="yes"
ENV RUN_DEV_SERVER="no"
ENV RUN_COLLECT_STATIC="no"
ENV RUN_CREATE_SUPER_USER="yes"

WORKDIR /var/www

COPY ./api/requirements.txt ./

RUN apk update && \
    # build dependencies
    apk add --no-cache --virtual .build-deps \
    gettext \
    git \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    zlib-dev \
    python3-dev \
    jpeg-dev \
    make \
    cython && \
    #
    # production dependencies
    apk add --no-cache \
    jpeg \
    nginx && \
    #
    # install
    pip install -r requirements.txt && \
    #
    # cleanup
    apk del -f .build-deps

COPY docker/nginx/nginx.conf /etc/nginx/http.d/default.conf
COPY docker/s6-rc.d /etc/s6-overlay/s6-rc.d
COPY --from=build /build/dist /var/www/html

COPY ./api/paul_api/ /var/www/paul_api/

RUN mkdir -p /var/www/paul_api/media

EXPOSE 80
