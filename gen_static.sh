#!/bin/bash

python -m pip install -r requirements.txt;
python manage.py collectstatic;
