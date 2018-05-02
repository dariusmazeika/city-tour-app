FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN pip3 install --upgrade pip
COPY requirements.txt tmp/
RUN pip3 install -r tmp/requirements.txt

RUN mkdir -p /app/static /tmp/logs/app

VOLUME /app
VOLUME /static

WORKDIR /app
EXPOSE 8000
