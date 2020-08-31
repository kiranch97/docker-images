#!/bin/bash
source venv/bin/activate
gunicorn -k "uvicorn.workers.UvicornWorker" --workers 3 -b localhost:8000 app.main:app --reload
