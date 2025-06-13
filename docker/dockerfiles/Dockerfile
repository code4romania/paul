ARG PYTHON_VERSION=3.13.4
ARG S6_OVERLAY_VERSION=3.2.1.0


FROM python:${PYTHON_VERSION}-slim-bookworm AS build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates \
    gettext git gcc g++ && \
    python3 -m pip install --upgrade pip setuptools cython

# Download the latest UV installer
ADD ./docker/third-party/uv/installer.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Make sure scripts in .local are usable:
ENV PATH="/root/.local/bin:${PATH}"

# Python virtualenv paths
ENV VIRTUAL_ENV=/opt/venv
RUN uv venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /build
COPY ./backend/pyproject.toml ./backend/uv.lock /build/
# Install dependencies
RUN uv sync --locked --no-install-project --active --compile-bytecode


FROM python:${PYTHON_VERSION}-slim-bookworm

ENV PYTHONUNBUFFERED=1

ENV ENVIRONMENT=production
ENV DEBUG=${DEBUG:-False}

ENV RUN_MIGRATIONS=True
ENV RUN_COMPILE_MESSAGES=True
ENV RUN_COLLECT_STATIC=True
ENV RUN_CREATE_SUPER_USER=True

ENV IS_CONTAINERIZED=True

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates \
    nginx gcc xz-utils gettext build-essential postgresql-client libpq-dev

# Download the latest UV installer
ADD ./docker/third-party/uv/installer.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Make sure scripts in .local are usable:
ENV PATH="/root/.local/bin:${PATH}"

ARG S6_OVERLAY_VERSION
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz


COPY docker/nginx/nginx.conf /etc/nginx/sites-available/default
COPY docker/s6-rc.d /etc/s6-overlay/s6-rc.d


# Python virtualenv paths:
ENV VIRTUAL_ENV=/opt/venv
RUN uv venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"


# copy the backend source code and libraries from the build stage:
COPY --from=build "${VIRTUAL_ENV}" "${VIRTUAL_ENV}"

WORKDIR /var/www/paul/backend/
COPY ./backend/ /var/www/paul/backend/

# Setup the VERSION.REVISION of the build:
ARG VERSION
ARG REVISION

RUN touch /var/www/paul/.version && \
    echo "$VERSION+$(echo ${REVISION} | cut -c 1-7)" > /var/www/paul/.version


ENTRYPOINT ["/init"]

WORKDIR /var/www/paul/

EXPOSE 80
