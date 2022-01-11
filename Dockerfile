FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
EXPOSE 8000 8000

# Add system requirements
RUN apk add --no-cache jq gettext sed bash curl docker-cli git binutils
# Add runtime dependencies
RUN apk add --no-cache libpq libxslt libjpeg zlib jpeg postgresql-client

COPY requirements/requirements.dev.txt requirements/requirements.dev.txt
COPY Makefile Makefile

RUN apk add --no-cache --virtual build-deps gcc musl-dev postgresql-dev libxslt-dev jpeg-dev libffi-dev rust cargo make && make install

RUN rm -rf requirements

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add kubectl
RUN curl -sL https://sentry.io/get-cli/ | bash

VOLUME /app
VOLUME /static
WORKDIR /app
