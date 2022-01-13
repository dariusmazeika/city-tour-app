FROM gitpod/workspace-full

ENV PYTHONUNBUFFERED 1

RUN brew install python@3.10 postgres || true

COPY requirements/requirements.dev.txt .
RUN pip install --no-cache-dir pip-tools==6.2.0 pip==21.2.4
RUN pip-sync requirements.dev.txt
RUN rm -f requirements.dev.txt
