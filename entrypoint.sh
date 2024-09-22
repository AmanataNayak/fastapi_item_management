#!/bin/sh
alembic revision --autogenerate -m "All tables created" || true
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
