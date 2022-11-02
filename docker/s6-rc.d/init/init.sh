#!/command/with-contenv sh

cd /var/www/paul_api

echo "Checking..."
python3 manage.py check

if [ "${RUN_MIGRATION}" = "yes" ]; then
    echo "Migrating databse"
    python3 manage.py migrate --run-syncdb
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
    echo "Check superuser"
    SUPERUSERS=$(python3 manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username=\"${DJANGO_ADMIN_EMAIL}\").count())")

    if [ "${SUPERUSERS}" = "0" ]; then
        echo "Create superuser"
        python3 manage.py createsuperuser --noinput \
            --username "${DJANGO_ADMIN_EMAIL}" --email "${DJANGO_ADMIN_EMAIL}"

        echo "Set superuser password"
        python3 manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username=\"${DJANGO_ADMIN_EMAIL}\"); u.set_password(\"${DJANGO_ADMIN_PASSWORD}\"); u.save()"
    else
        echo "Superuser already exists"
    fi
fi
