#!/usr/bin/env sh
alembic revision --autogenerate
alembic upgrade head
"python" "main.py"