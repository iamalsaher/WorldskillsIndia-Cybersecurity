#!/bin/bash
cd /app
python application.py
gunicorn --workers 5 --bind 0.0.0.0:8000 --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log --log-level debug application:app
