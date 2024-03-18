FROM docker:25.0.4

ENV PYTHON_VERSION=3.11.8-r0

# download and extract python sources
RUN apk add python3="$PYTHON_VERSION" --repository=http://dl-cdn.alpinelinux.org/alpine/v3.19/main
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED

ENV PYTHON_PIP_VERSION 24.0
# https://github.com/docker-library/python/issues/365
ENV PYTHON_SETUPTOOLS_VERSION 65.5.1
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get-pip.py
ENV PYTHON_GET_PIP_SHA256 dfe9fd5c28dc98b5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9

RUN set -eux; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; \
	\
	export PYTHONDONTWRITEBYTECODE=1; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		--no-compile \
		"pip==$PYTHON_PIP_VERSION" \
		"setuptools==$PYTHON_SETUPTOOLS_VERSION" \
	; \
	rm -f get-pip.py; \
	\
	pip --version

WORKDIR /ci

COPY requirements.txt .
RUN pip install --upgrade pip==24.0
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py tasks.py gunicorn_conf.py ./
COPY ./swagger ./swagger

CMD ["gunicorn", "--config", "gunicorn_conf.py"]