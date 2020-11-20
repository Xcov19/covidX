FROM alpine:3.12.1

# See: https://stackoverflow.com/questions/45028650/docker-image-with-python-alpine-failure-due-missing-compiler-error
RUN apk --update add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev libxml2 libxslt libxml2-dev libxslt-dev gcc build-base postgresql-libs musl-dev postgresql-dev postgresql-client postgresql redis bazel

RUN ln -s `which python3` /usr/bin/python

# symlink python to /usr/bin/python3
ENV PATH /usr/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 20.2.3
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
ENV PYTHON_GET_PIP_SHA256 6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c

RUN set -ex; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	# echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -; \
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

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt
RUN python -m pip install cython
RUN CPPFLAGS="$(pg_config --cppflags)" LDFLAGS="$(pg_config --ldflags)" python -m pip install -r requirements.txt

# Setup celery project dir
ARG PROJECT=app
ARG PROJECT_DIR=/${PROJECT}
RUN mkdir -p $PROJECT_DIR

# WORKDIR /app
WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR

RUN if [ -d "static" ]; then chmod -R a+rx static/ && chown -R `whoami` static/ && rm -rf static; fi;
RUN touch $PROJECT_DIR/logs.log && chmod 0777 $PROJECT_DIR/logs.log && chown `whoami` $PROJECT_DIR/logs.log


RUN sudo -u postgres psql -c"ALTER user postgres WITH PASSWORD postgres"
RUN sudo service postgresql restart

RUN if [ -n "$IS_WAIT" ]; then echo "/wait && sh pre_start.sh"; fi;
