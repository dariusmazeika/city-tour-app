FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
EXPOSE 8000 8000

# Add system requirements
RUN apk add --no-cache jq gettext sed bash curl docker-cli git binutils
# Add runtime dependencies
RUN apk add --no-cache libpq libxslt libjpeg zlib jpeg postgresql-client

COPY requirements.dev.txt .

RUN apk add --no-cache --virtual build-deps gcc musl-dev postgresql-dev libxslt-dev jpeg-dev libffi-dev rust cargo \
	&& pip install --no-cache-dir --upgrade pip-tools awscli \
	&& pip-sync requirements.dev.txt

RUN rm -f requirements.dev.txt

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add kubectl

VOLUME /app
VOLUME /static
WORKDIR /app
