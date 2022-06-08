FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update -y \
 && apt-get install -y --no-install-recommends --fix-missing \
    autoconf \
    automake \
    bzip2 \
    ca-certificates \
    curl \
    dirmngr \
    dpkg-dev \
    file \
    g++ \
    gcc \
    gettext \
    git \
    gnupg \
    gnupg2 \
    imagemagick \
    libtool \
    make \
    mercurial \
    openssh-client \
    patch \
    postgresql \
    postgresql-client \
    postgresql-contrib \
    python-all-dev \
    python3-dev \
    python3-pip \
    software-properties-common \
    subversion \
    sudo \
    build-essential \
    unzip \
    xz-utils \
    zlib1g-dev \
    memcached \
    libmemcached-tools \
    libssl-dev \
    libffi-dev \
    cargo \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add bazel using bazelisk
RUN curl -Lo /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.7.4/bazelisk-linux-amd64 \
 && chmod +x /usr/local/bin/bazel       \
 && export PATH=$PATH:/usr/local/bin/   \
 && alias bazel=/usr/local/bin/bazel    \
 && bazel version

## Add the wait script to the image
RUN curl -Lo ./wait https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait \
 && chmod +x ./wait

RUN if test -f "/usr/bin/python"; then rm /usr/bin/python; fi; \
    ln -s "$(which python3)" /usr/bin/python;

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt

#Fix setuptools_rust issue
#See: https://github.com/frappe/bench/issues/1117
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# For gevent
RUN mkdir -p .pip \
 && CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python3 -m pip --cache-dir=.pip install -U pip \
 && python3 -m pip install cython==0.29.21 \
 && CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python3 -m pip --cache-dir=.pip install -r requirements.txt \
 && rm -rf .pip

# Setup celery project dir
ARG PROJECT_DIR=/
WORKDIR /
COPY . .

RUN if [ -d "static" ]; then chmod -R a+rx static/ && chown -R "$(whoami)" static/ && rm -rf static; fi; \
    touch logs.log && chmod 0777 logs.log && chown "$(whoami)" logs.log

COPY .env.dev .env
ENV DEBUG_ENV=1
ENV SECRET_KEY=dskaj343
ENV CPPFLAGS="$(pg_config --cppflags)"
ENV LDFLAGS="$(pg_config --ldflags)"
ENV BAZEL_CACHE="/bazel-cache"

RUN openssl req -x509 -newkey rsa:4096 -keyout privateKey.key -out certificate -days 365 -nodes -subj "/C=IN/ST=NCR/L=DEL/O=XCoV19/OU=DEV/CN=XCoV19"

COPY pre-start.sh /pre-start.sh
COPY up-script.sh /up-script.sh

# Manually change the line format to UNIX format.
RUN sed -i 's/\r$//' /pre-start.sh && chmod +x /pre-start.sh \
 && sed -i 's/\r$//' /up-script.sh && chmod +x /up-script.sh

#build
RUN mkdir -p $BAZEL_CACHE
RUN PULLER_TIMEOUT=3600 CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" bazel build :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=2000 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS --action_env=CPPFLAGS --action_env=DEBUG_ENV --action_env=SECRET_KEY --action_env=$BAZEL_CACHE --action_env=PULLER_TIMEOUT --disk_cache=$BAZEL_CACHE

#See: https://github.com/gitpod-io/gitpod/issues/2614#issuecomment-752362094
### Gitpod user ###
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN useradd -l -u 33333 -G sudo -md /home/gitpod -s /bin/bash -p gitpod gitpod \
    # passwordless sudo for users in the 'sudo' group
    && sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
