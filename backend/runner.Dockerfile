FROM docker:latest

# Dependencies
RUN apk add --no-cache jq python3 python3-dev py3-pip gettext libpq libxslt libjpeg zlib jpeg sed

COPY requirements.txt /tmp/

# Build dependencies and pip requirements
RUN apk add --no-cache --virtual build-deps gcc musl-dev postgresql-dev libxslt-dev jpeg-dev libffi-dev\
    && pip install --no-cache-dir --upgrade pip wheel setuptools awscli tblib\
    && pip install --no-cache-dir -r /tmp/requirements.txt\
    && rm -f /tmp/requirements.txt\
    && apk del build-deps
