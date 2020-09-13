# covidX

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aafaddbe77e549eda4a560ee7d9f76c5)](https://app.codacy.com/gh/Xcov19/covidX?utm_source=github.com&utm_medium=referral&utm_content=Xcov19/covidX&utm_campaign=Badge_Grade_Dashboard)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Xcov19/covidX/?ref=repository-badge)

![CI](https://github.com/Xcov19/covidX/workflows/CI/badge.svg)

[![Open Source Helpers](https://www.codetriage.com/xcov19/covidx/badges/users.svg)](https://www.codetriage.com/xcov19/covidx)

We are an open community of volunteers without a commercial purpose. We believe that through a utilitarian approach, we can do the most good in the quickest time. Applying unused engineering we can help the world cope with the threat of COVID-19.

#### Python Version
covidX will be run on python *3.7.6* and *3.8.5*

#### Installation
Clone this git repo and then build like:
```bash
bazel build :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=20 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS="$(pg_config --ldflags)" --action_env=CPPFLAGS="$(pg_config --cppflags)"

```

Run it like:
```bash
bazel run :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=20 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS="$(pg_config --ldflags)" --action_env=CPPFLAGS="$(pg_config --cppflags)" -- runserver_plus

```

DEPLOY like:
Enable following options on GAE:

```python
gcloud app deploy app.yaml --verbosity=debug --stop-previous-version
```


TODO:
    How to contribute. Coming soon.
