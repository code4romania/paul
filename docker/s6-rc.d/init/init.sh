#!/command/with-contenv sh

cd /var/www/paul_api

echo "Checking..."
python3 manage.py check

if [ "${RUN_MIGRATION}" = "yes" ]; then
    echo "Migrating databse"
    python3 manage.py migrate --run-syncdb
fi

if [ "${RUN_COMPILE_MESSAGES}" = "yes" ]; then
    echo "Compiling translation messages"
    python3 manage.py compilemessages
fi

if [ "${RUN_COLLECT_STATIC}" = "yes" ]; then
    echo "Collect static"
    mkdir -p /var/www/paul_api/static
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
