#!/usr/bin/env sh

alembic upgrade head
python add_test.py
python main.py