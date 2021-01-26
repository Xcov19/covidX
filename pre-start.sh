#!/bin/sh

if [ -n  "$(find apps/*/migrations -name "*.py")" ]; then
  echo "====remove migrations====";
  rm -rf apps/*/migrations/*;
fi;

#create init files
for dir in apps/*/migrations; do touch "$dir/__init__.py"; done;

echo "===pip install========="
python -m pip --cache-dir=.pip install -r requirements.txt;
echo "=====drop db==========="
python manage.py reset_db -c --noinput;
echo "=====makemigrations====="
python manage.py makemigrations;
