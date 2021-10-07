release: ./manage.py migrate
web: gunicorn --bind 0.0.0.0:$PORT atlascope.wsgi
worker: REMAP_SIGTERM=SIGQUIT celery --app atlascope.celery worker --loglevel INFO --without-heartbeat
