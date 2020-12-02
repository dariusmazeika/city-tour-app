FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
EXPOSE 8000 8000

# Dependencies
RUN apk add --no-cache libpq libxslt libjpeg zlib jpeg

COPY requirements.txt /tmp/

# Build dependencies and pip requirements
RUN apk add --no-cache --virtual build-deps gcc musl-dev postgresql-dev libxslt-dev jpeg-dev libffi-dev\
    && pip install --no-cache-dir --upgrade pip wheel setuptools\
    && pip install --no-cache-dir -r /tmp/requirements.txt\
    && rm -f /tmp/requirements.txt\
    && apk del build-deps
