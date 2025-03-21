#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
uvicorn web.core.asgi:application --host 0.0.0.0 --port 8000