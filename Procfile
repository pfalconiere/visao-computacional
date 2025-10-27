# Render Standard: 1 worker para otimizar memória e conexões Redis
web: gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 180 --max-requests 100 --max-requests-jitter 10 api:app
worker: celery -A celery_config.celery_app worker --loglevel=info --concurrency=1
