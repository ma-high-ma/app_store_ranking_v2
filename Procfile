release: python manage.py migrate
web: gunicorn app_store_ranking_v2.wsgi --log-file -
worker: celery -A app_store_ranking_v2 worker -l info
