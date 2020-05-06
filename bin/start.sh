#!/bin/bash
source /home/lw/PycharmProjects/Flask_bird/venv/bin/activate
nohup gunicorn --workers=4 -b 0.0.0.0:8000 wsgi:app >../logs/start.log 2>&1 &
#gunicorn --workers=4 -b 0.0.0.0:8000 wsgi:app
