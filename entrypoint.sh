python manage.py migrate

if [[ $APP_ENV == "dev" ]]; then
    python manage.py runserver 0.0.0.0:8000
elif [[ $APP_ENV == "prod" ]]; then
    gunicorn Grotto.wsgi:application -b 0.0.0.0:8000
fi
