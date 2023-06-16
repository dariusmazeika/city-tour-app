FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
EXPOSE 8000 8000

# Add system requirements
RUN apk add --no-cache jq gettext sed bash curl docker-cli git binutils make
# Add runtime dependencies
RUN apk add --no-cache libpq libxslt libjpeg zlib jpeg postgresql-client

COPY requirements/requirements.dev.txt requirements/requirements.dev.txt
COPY Makefile Makefile

RUN apk add --no-cache --virtual build-deps gcc g++ musl-dev postgresql-dev libxslt-dev jpeg-dev libffi-dev rust cargo && make install

RUN rm -rf requirements
RUN rm -f Makefile

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk add kubectl
RUN curl -sL https://sentry.io/get-cli/ | bash

VOLUME /app
VOLUME /static
WORKDIR /app
