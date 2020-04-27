# covidX 

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aafaddbe77e549eda4a560ee7d9f76c5)](https://app.codacy.com/gh/Xcov19/covidX?utm_source=github.com&utm_medium=referral&utm_content=Xcov19/covidX&utm_campaign=Badge_Grade_Dashboard)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Xcov19/covidX/?ref=repository-badge)

We are an open community of volunteers without a commercial purpose. We believe that through a utilitarian approach, we can do the most good in the quickest time. Applying unused engineering we can help the world cope with the threat of COVID-19.

#### Python Version
covidX will be run on python *3.7.6*

#### Installation
Clone this git repo and then run:
```bash
bazel build //:app --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=10 --loading_phase_threads=HOST_CPUS

```
Run it like:
```bash
bazel run --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=10 --loading_phase_threads=HOST_CPUS //:app -- runserver

```

TODO:
Enable following options on GAE:
* With a wsgi server => `gunicorn -c gunicorn.conf.py covidX.wsgi`

