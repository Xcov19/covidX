FROM ubuntu:focal

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
RUN apt-get update -y

RUN apt-get install -y --no-install-recommends lsb-release ca-certificates curl software-properties-common wget

# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update -y
RUN apt-get install -y libpq-dev postgresql postgresql-client postgresql-contrib

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

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt

# Setup python, pip & dependency libs
RUN set -ex; if ! command -v gpg > /dev/null; then apt-get update; \
apt-get install -y --no-install-recommends gnupg dirmngr git mercurial openssh-client subversion procp; \
rm -rf /var/lib/apt/lists/*;fi

RUN set -ex;apt-get update && apt-get install -y --no-install-recommends autoconf automake bzip2 \
dpkg-dev file g++ gcc imagemagick libbz2-dev libc6-dev libcurl4-openssl-dev libdb-dev libevent-dev \
libffi-dev libgdbm-dev libglib2.0-dev libgmp-dev libjpeg-dev libkrb5-dev liblzma-dev libmagickcore-dev \
libmagickwand-dev libmaxminddb-dev libncurses5-dev libncursesw5-dev libpng-dev libpq-dev libreadline-dev \
libsqlite3-dev libssl-dev libtool libwebp-dev libxml2-dev libxslt-dev libyaml-dev make patch unzip xz-utils \
zlib1g-dev; rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ENV GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
ENV PYTHON_VERSION=3.8.6
RUN set -ex \
	\
	&& wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
	&& wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
	&& export GNUPGHOME="$(mktemp -d)" \
	&& gpg --batch --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
	&& gpg --batch --verify python.tar.xz.asc python.tar.xz \
	&& { command -v gpgconf > /dev/null && gpgconf --kill all || :; } \
	&& rm -rf "$GNUPGHOME" python.tar.xz.asc \
	&& mkdir -p /usr/src/python \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz \
	\
	&& cd /usr/src/python \
	&& gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
	&& ./configure \
		--build="$gnuArch" \
		--enable-loadable-sqlite-extensions \
		--enable-optimizations \
		--enable-option-checking=fatal \
		--enable-shared \
		--with-system-expat \
		--with-system-ffi \
		--without-ensurepip \
	&& make -j "$(nproc)" \
	&& make install \
	&& rm -rf /usr/src/python \
	\
	&& find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name '*.a' \) \) \
			-o \( -type f -a -name 'wininst-*.exe' \) \
		\) -exec rm -rf '{}' + \
	\
	&& ldconfig \
	\
	&& python3 --version

RUN cd /usr/local/bin && ln -s idle3 idle && ln -s pydoc3 pydoc && ln -s python3 python && \
ln -s python3-config python-config
ENV PYTHON_PIP_VERSION=20.2.3
ENV PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
ENV PYTHON_GET_PIP_SHA256=6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c

RUN set -ex; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -; \
	\
	python get-pip.py \
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

RUN if test -f "/usr/bin/python"; then rm /usr/bin/python; fi;
RUN ln -s /usr/local/bin/python3 /usr/bin/python;

# Prepare for pyenv
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev \
 libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev\
 libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl\
 git
RUN curl https://pyenv.run | bash
RUN export PATH="/root/.pyenv/bin:$PATH"

# Setup celery project dir
ARG PROJECT=app
ARG PROJECT_DIR=/${PROJECT}
RUN mkdir -p $PROJECT_DIR

# WORKDIR /app
WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR

RUN if [ -d "static" ]; then chmod -R a+rx static/ && chown -R `whoami` static/ && rm -rf static; fi;
RUN touch $PROJECT_DIR/logs.log && chmod 0777 $PROJECT_DIR/logs.log && chown `whoami` $PROJECT_DIR/logs.log

ENV MAIN_USER=$(whoami)
# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
USER postgres
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf
# Expose the PostgreSQL port
EXPOSE 5432
RUN echo "listen_addresses='*'" >> /etc/postgresql/13/main/postgresql.conf
RUN /etc/init.d/postgresql start;
ENTRYPOINT /usr/lib/postgresql/13/bin/postgres -D /var/lib/postgresql/13/main -c config_file=/etc/postgresql/13/main/postgresql.conf
