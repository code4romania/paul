FROM node:14 as build

WORKDIR /build

COPY ./client .
RUN yarn install
RUN yarn build

FROM python:3.10.5-slim

ARG ENVIRONMENT

ENV ENVIRONMENT ${ENVIRONMENT:-production}
ENV DJANGO_SETTINGS_MODULE=paul_api.settings

RUN apt update && \
    apt install -y nginx gettext git gcc g++ && \
    pip install --upgrade pip setuptools cython

COPY --from=jwilder/dockerize:0.6.1 /usr/local/bin/dockerize /usr/local/bin/dockerize
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /build/dist /usr/share/nginx/html

WORKDIR /opt/

RUN mkdir -p /var/www/paul-api/media

# Copy just the requirements for caching
COPY ./api/requirements*.txt ./
RUN if [ "${ENVIRONMENT}" = "production" ]; \
    then pip install -r requirements.txt; \
    else pip install -r requirements-dev.txt; \
fi

WORKDIR /opt/paul_api/

COPY ./api/docker-entrypoint.sh /
COPY ./api/paul_api/ /opt/paul_api/

ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 8000
