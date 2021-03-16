#!/bin/bash

python3 -m pip install -r requirements.txt;
SECRET_KEY=$(gcloud secrets versions access latest --secret='SECRET_KEY') python manage.py collectstatic;
