#!/usr/bin/env bash
python -m gunicorn app.main:app --bind 0.0.0.0:$PORT
