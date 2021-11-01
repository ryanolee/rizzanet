#! /usr/bin/env bash
export FLASK_APP=app.py
dockerize -wait tcp://es:9200
python -m flask rizzanet install 