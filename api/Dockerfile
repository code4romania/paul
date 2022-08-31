FROM python:3.10.5-slim

ARG ENVIRONMENT

ENV ENVIRONMENT ${ENVIRONMENT:-production}
ENV DJANGO_SETTINGS_MODULE=paul_api.settings

RUN apt update && \
    apt install -y gettext git gcc g++ && \
    pip install --upgrade pip setuptools cython

COPY --from=jwilder/dockerize:0.6.1 /usr/local/bin/dockerize /usr/local/bin/dockerize

WORKDIR /opt/

RUN mkdir -p /var/www/paul-api/media

# Copy just the requirements for caching
COPY ./requirements*.txt ./
RUN if [ "${ENVIRONMENT}" = "production" ]; \
    then pip install -r requirements.txt; \
    else pip install -r requirements-dev.txt; \
fi

WORKDIR /opt/paul_api/

COPY ./docker-entrypoint.sh /
COPY ./paul_api/ /opt/paul_api/

ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 8000
