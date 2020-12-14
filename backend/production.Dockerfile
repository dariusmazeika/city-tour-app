FROM python:3.9

ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pipenv

COPY Pipfile.lock Pipfile tmp/
WORKDIR tmp/
RUN pipenv install --system --deploy

RUN mkdir -p /app
WORKDIR /app

COPY . /app/
EXPOSE 8000
CMD ./bin/start_production.sh
