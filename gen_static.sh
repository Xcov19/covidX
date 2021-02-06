#!/bin/bash

python -m pip install -r requirements.txt;
SECRET_KEY=$(SECRET_KEY) python manage.py collectstatic;
