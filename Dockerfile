# Use phusion/baseimage as base image. To make your builds
# reproducible, make sure you lock down to a specific version, not
# to `latest`! See
# https://github.com/phusion/baseimage-docker/blob/master/Changelog.md
# for a list of version numbers.
FROM codecakes/buster_py:latest

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# Create the file repository configuration:
RUN (addgroup --system postgres && adduser --system postgres && usermod -a -G postgres postgres)
RUN mkdir -p /var/lib/postgresql/data
RUN mkdir -p /run/postgresql/
RUN chown -R postgres:postgres /run/postgresql/
RUN chmod -R 777 /var/lib/postgresql/data
RUN chown -R postgres:postgres /var/lib/postgresql/data
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7FCC7D46ACCC4CF8
RUN apt-get update -y && apt-get install -y lsb-release

RUN apt-get install -y ca-certificates curl software-properties-common wget

# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update -y
RUN apt-get install -y libpq-dev postgresql postgresql-client postgresql-contrib

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

#ENV PYTHON_VERSION 3.8.5
#RUN set -ex \
#	&& curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
#	&& curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
#	&& export GNUPGHOME="$(mktemp -d)" \
#	&& gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
#	&& gpg --batch --verify python.tar.xz.asc python.tar.xz \
#	&& rm -r "$GNUPGHOME" python.tar.xz.asc \
#	&& mkdir -p /usr/src/python \
#	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
#	&& rm python.tar.xz \
#	\
#	&& cd /usr/src/python \
#	&& ./configure --enable-shared --enable-unicode=ucs4 \
#	&& make -j$(nproc) \
#	&& make install \
#	&& ldconfig

# symlink python to /usr/bin/python3
ENV PATH /usr/bin:$PATH
#RUN ln -s `which python3` /usr/bin/python

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
#ENV PYTHON_PIP_VERSION 20.2.3
## https://github.com/pypa/get-pip
#ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
#ENV PYTHON_GET_PIP_SHA256 6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c
#
#RUN set -ex; \
#	\
#	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
#	# echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -; \
#	\
#	python get-pip.py \
#		--disable-pip-version-check \
#		--no-cache-dir \
#		"pip==$PYTHON_PIP_VERSION" \
#	; \
#	pip --version; \
#	\
#	find /usr/local -depth \
#		\( \
#			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
#			-o \
#			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
#		\) -exec rm -rf '{}' +; \
#	rm -f get-pip.py

# Add bazel using bazelisk
RUN curl -Lo /usr/local/bin/bazel https://github.com/bazelbuild/bazelisk/releases/download/v1.7.4/bazelisk-linux-amd64
RUN chmod +x /usr/local/bin/bazel
RUN export PATH=$PATH:/usr/local/bin/
RUN alias bazel=/usr/local/bin/bazel
RUN bazel version

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt
RUN python -m pip install cython
RUN CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python -m pip install -r requirements_dev.txt

# Setup celery project dir
ARG PROJECT=app
ARG PROJECT_DIR=/${PROJECT}
RUN mkdir -p $PROJECT_DIR

# WORKDIR /app
WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR

RUN if [ -d "static" ]; then chmod -R a+rx static/ && chown -R `whoami` static/ && rm -rf static; fi;
RUN touch $PROJECT_DIR/logs.log && chmod 0777 $PROJECT_DIR/logs.log && chown `whoami` $PROJECT_DIR/logs.log

# Calls for a random number to break the caching of step
# https://stackoverflow.com/questions/35134713/disable-cache-for-specific-run-commands/58801213#58801213
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN su - postgres -c "initdb /var/lib/postgresql/data"
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf
RUN su - postgres -c "pg_ctl start -D /var/lib/postgresql/data -l /var/lib/postgresql/log.log && psql --command \"ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';\" && psql --command \"CREATE DATABASE postgres;\""

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
