FROM ubuntu:focal


RUN apt-get update -y \
 && apt-get install -y --no-install-recommends lsb-release ca-certificates curl software-properties-common wget gnupg2 \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update -y \
 && apt-get install -y libpq-dev postgresql postgresql-client postgresql-contrib \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV PATH /usr/bin:$PATH

# Add bazel using bazelisk
RUN curl -Lo /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.7.4/bazelisk-linux-amd64
RUN chmod +x /usr/local/bin/bazel
RUN export PATH=$PATH:/usr/local/bin/
RUN alias bazel=/usr/local/bin/bazel
RUN bazel version

# Setup python, pip & dependency libs
RUN set -ex; if ! command -v gpg > /dev/null; then apt-get update; \
apt-get install -y --no-install-recommends gnupg dirmngr git mercurial openssh-client subversion procp \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* ; fi

RUN set -ex;apt-get update && apt-get install -y --no-install-recommends autoconf automake bzip2 \
dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev \
libffi-dev libgdbm-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev \
libmagickwand-dev libmaxminddb-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev \
libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils \
zlib1g-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ENV GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
ENV PYTHON_VERSION=3.8.6
RUN which python3

ENV PYTHON_PIP_VERSION=20.2.3
ENV PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
ENV PYTHON_GET_PIP_SHA256=6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c

RUN set -ex; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -; \
	\
	python3 get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py

RUN apt-get update -y && apt-get install -y make libssl-dev zlib1g-dev \
 libbz2-dev libreadline-dev libsqlite3-dev libncurses5-dev \
 libncursesw5-dev xz-utils libffi-dev liblzma-dev \
 libghc-zlib-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip git \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt

# For gevent
RUN apt-get update -y && apt-get install -y libevent-dev file make gcc musl-dev libffi-dev python-all-dev libpython3-dev python3-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN mkdir -p .pip
RUN CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python3 -m pip --cache-dir=.pip install -U pip
RUN python3 -m pip install cython && CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python3 -m pip --cache-dir=.pip install -r requirements.txt

RUN if test -f "/usr/bin/python"; then rm /usr/bin/python; fi;
RUN ln -s `which python3` /usr/bin/python;

# Install memcached
RUN apt-get update \
 && apt-get install -y --no-install-recommend   \
    memcached                                   \
    libmemcached-tools                          \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Setup celery project dir
ARG PROJECT_DIR=/
WORKDIR /
COPY . .

RUN if [ -d "static" ]; then chmod -R a+rx static/ && chown -R $(whoami) static/ && rm -rf static; fi;
RUN touch logs.log && chmod 0777 logs.log && chown $(whoami) logs.log

RUN if [ ! -f ".env" ]; then touch .env; fi;
COPY .env .env
ENV DEBUG_ENV=1
ENV SECRET_KEY=dskaj343
ENV CPPFLAGS="$(pg_config --cppflags)"
ENV LDFLAGS="$(pg_config --ldflags)"
COPY privateKey.key /privateKey.key
COPY certificate /certificate
RUN chmod +x /certificate && chmod +x /privateKey.key

#build
RUN CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" bazel build :manage --watchfs --spawn_strategy=standalone --copt --aspects=@bazel_tools//tools/python:srcs_version.bzl%find_requirements --verbose_failures=true --show_timestamps=true --python_version=PY3 --build_python_zip --sandbox_debug --color=yes --curses=yes --jobs=2000 --loading_phase_threads=HOST_CPUS --action_env=LDFLAGS --action_env=CPPFLAGS --action_env=DEBUG_ENV --action_env=SECRET_KEY

COPY pre-start.sh /pre-start.sh
COPY up-script.sh /up-script.sh

# Manually change the line format to UNIX format.
RUN sed -i 's/\r$//' /pre-start.sh && chmod +x /pre-start.sh && \
sed -i 's/\r$//' /up-script.sh && chmod +x /up-script.sh;

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait ./wait
RUN chmod +x ./wait
