# covidX 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aafaddbe77e549eda4a560ee7d9f76c5)](https://app.codacy.com/gh/Xcov19/covidX?utm_source=github.com&utm_medium=referral&utm_content=Xcov19/covidX&utm_campaign=Badge_Grade_Dashboard)

We are an open community of volunteers without a commercial purpose. We believe that through a utilitarian approach, we can do the most good in the quickest time. Applying unused engineering we can help the world cope with the threat of COVID-19.

#### Python Version
covidX will be run on python >= *3.8*

#### Installation
Clone this git repo and then run `pip install -r requirement.txt`

You can run using following options:
* Regular django app => `python manage.py runserver`
* With a wsgi server => `gunicorn -c gunicorn.conf.py covidX.wsgi`

