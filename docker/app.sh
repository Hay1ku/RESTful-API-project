#!/bin/bash

alembic upgrade 0a2f91403eba

gunicorn app.app_main.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000