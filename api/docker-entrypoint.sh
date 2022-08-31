#!/bin/sh

DOCKERIZE=""
prefix="dockerize"

PORT=${PORT:-"8000"}

RUN_FEED=${RUN_FEED:-"no"}
RUN_MIGRATION=${RUN_MIGRATION:-"yes"}
RUN_DEV_SERVER=${RUN_DEV_SERVER:-"no"}
RUN_COLLECT_STATIC=${RUN_COLLECT_STATIC:-"no"}
RUN_CREATE_SUPER_USER=${RUN_CREATE_SUPER_USER:-"no"}

if [ "${1}" = "${prefix}" ]; then
    DOCKERIZE="dockerize"
    shift
    while [ "${1}" != '--' ]; do
        DOCKERIZE="${DOCKERIZE} ${1}"
        shift
    done
    shift
fi

exec_web() {
    echo "Checking..."
    python3 manage.py check

    if [ "${RUN_MIGRATION}" = "yes" ]; then
        echo "Migrating databse"
        python3 manage.py migrate --run-syncdb
    fi

    if [ "${RUN_COLLECT_STATIC}" = "yes" ]; then
        echo "Collect static"
        mkdir -p /var/www/paul-api/static
        python3 manage.py collectstatic --noinput
    fi

    python3 manage.py seed-frontend-domain

    if [ "${RUN_FEED}" = "yes" ]; then
        echo "Feed"
        python3 manage.py feed-json
    fi

    if [ "${RUN_CREATE_SUPER_USER}" = "yes" ]; then
        echo "Create superuser"
        python3 manage.py createsuperuser --noinput \
            --username "${DJANGO_ADMIN_USERNAME}" --email "${DJANGO_ADMIN_EMAIL}"

        echo "Set superuser password"
        python3 manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username=\"${DJANGO_ADMIN_USERNAME}\"); u.set_password(\"${DJANGO_ADMIN_PASSWORD}\"); u.save()"
    fi

    if [ "${RUN_DEV_SERVER}" = "yes" ]; then
        echo "Start web server on ${PORT}"
        python3 manage.py runserver "0.0.0.0:${PORT}"
    else
        exec gunicorn paul_api.wsgi --bind "0.0.0.0:${PORT}" --log-level info -k gevent -w 10
    fi
}

exec_celery() {
    PROCESS_TYPE="${1}"

    if [ "${DEBUG}" = "True" ]; then
        echo "Start celery ${PROCESS_TYPE} in DEBUG mode"
        exec celery -A paul_api "${PROCESS_TYPE}" -l DEBUG
    else
        exec celery -A paul_api "${PROCESS_TYPE}"
    fi
}

case "${1}" in
"web") exec_web ;;
"celery") exec_celery worker ;;
"celerybeat") exec_celery beat ;;
esac

exec "${@}"
