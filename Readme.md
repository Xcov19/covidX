# covidX

TL;DR Dive into coding right away by clicking here:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#snapshot/86df3ba3-ad70-4d11-a3a4-83fd0dd48684)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aafaddbe77e549eda4a560ee7d9f76c5)](https://app.codacy.com/gh/Xcov19/covidX?utm_source=github.com&utm_medium=referral&utm_content=Xcov19/covidX&utm_campaign=Badge_Grade_Dashboard)

[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Xcov19/covidX/?ref=repository-badge)

![CI](https://github.com/Xcov19/covidX/workflows/CI/badge.svg)

[![Open Source Helpers](https://www.codetriage.com/xcov19/covidx/badges/users.svg)](https://www.codetriage.com/xcov19/covidx)

We are an open community of volunteers without a commercial purpose. We believe that through a utilitarian approach, we can do the most good in the quickest time. Applying unused engineering we can help the world cope with the threat of COVID-19.

#### Python Version
covidX will be run on python *3.7.6* and *3.8.5*

#### Required Services for Self-Hosting
The following steps are necessary in order to ensure that you are able to self-host your own instance of the project smoothly:
* Install [PostgreSQL](https://www.postgresql.org/download/)
* Install [Bazel](https://docs.bazel.build/versions/master/install.html)
* Sign up to [Docker Hub](https://hub.docker.com/signup) and install [Docker Desktop](https://www.docker.com/get-started)
* Sign up to [Auth0](https://auth0.com/) (obtain domain, client id, and client secret)
* Sign up to [Algolia](https://www.algolia.com/users/sign_up) (obtain application id and admin API key)

#### How to Run Locally Using Docker (docker-compose)

* Create your `.env` file from the sample:
```shell
cp .env_sample .env
```

* Fill in the details based on the Auth0 and Algolia sign-ups

See https://github.com/Xcov19/covidX/issues/78

* Build and start the app
```shell
docker-compose up
```

The app should be built automatically on first run.

Note: to reflect changes made to `.env` after the application has been brought `up`, you need to force a rebuild:

```shell
docker-compose --build
```

### How to Setup for Development
Setup a virtualenv and run:

```shell script
CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python3 -m pip install -r requirements.txt 
```

### How to Build

#### No Docker: Local Machine Developer Setup

FIRST SEE HERE: https://forum.mycovidconnect.com/d/14-how-to-contribute-backenddjangopython-devs

Then,
- Clone this git repo. SECRET_KEY and DEBUG env vars are in settings.py.
- Pre-requisites:
```bash
export DEBUG_ENV=1
export SECRET_KEY=<YOUR_SECRET>
CPPFLAGS="$(pg_config --cppflags)"
LDFLAGS="$(pg_config --ldflags)"
```
- and then build like:
```bash
bazel build :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=20 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS --action_env=CPPFLAGS --action_env=DEBUG_ENV --action_env=SECRET_KEY

```

- Collectstatic
```bash
bazel run -s :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=200 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS --action_env=CPPFLAGS --action_env=DEBUG_ENV --action_env=SECRET_KEY -- collectstatic
```
- Then Run it like:

With Debug Mode:

```bash
DEBUG_ENV=1 SECRET_KEY=dskaj343 CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" bazel run :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=2000 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS --action_env=CPPFLAGS --action_env=DEBUG_ENV --action_env=SECRET_KEY -- runserver_plus 0.0.0.0:8000
```

Without Debug Mode:
```bash
bazel run :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=20 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS --action_env=CPPFLAGS --action_env=DEBUG_ENV --action_env=SECRET_KEY -- runserver_plus

```

#### Create Docker Image: Local Machine Developer Setup

Make sure to follow the steps above. Then follow these steps:

- Create a local docker bazel image
```shell
PULLER_TIMEOUT=3600 DOCKER_REPO_CACHE=$(pwd)/docker_repo_cache DEBUG_ENV=1 CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" SECRET_ID="SECRET_KEY" BUCKET_NAME="gae-bizlead" DJANGO_SETTINGS_MODULE="covidX.settings" WSGI_APPLICATION="covidX.wsgi.application" bazel run --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=2000 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS="$(pg_config --ldflags)" --action_env=CPPFLAGS="$(pg_config --cppflags)" --force_python=py3 --incompatible_use_python_toolchains=false  --loading_phase_threads=1 --http_timeout_scaling=2 :covidx_manage
```

- Run bazel image using docker
```shell
docker run --rm -it -e SECRET_KEY=<YOUR_SECRET_KEY> -e DEBUG_ENV=1 -e CPPFLAGS="$(pg_config --cppflags)" -e LDFLAGS="$(pg_config --ldflags)" -e SECRET_ID="SECRET_KEY" -e DJANGO_SETTINGS_MODULE="covidX.settings" -e WSGI_APPLICATION="covidX.wsgi.application" --security-opt apparmor=unconfined bazel:covidx_manage runserver_plus
```

This should set you up for local development.

### Installing Developer Packages
Setup a virtualenv and run:

```shell script
python3 -m pip install -r requirements_dev.txt 
```

#### Google Cloud Deployment

DEPLOY like:

Enable following options on GAE:

```python
gcloud app deploy app.yaml --verbosity=debug --stop-previous-version
```


### Common Issues:
* [Error when building local machine developer setup via docker image](https://github.com/Xcov19/covidX/issues/50)
* [No matching distribution found for ipython==7.18.1](https://github.com/Xcov19/covidX/issues/57)

### TODO/TBA:
    How to contribute. Coming soon.
    Project Roadmap

### Credits

    @codecakes
