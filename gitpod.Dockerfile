FROM gitpod/workspace-full

ENV PYTHONUNBUFFERED 1

RUN brew update
RUN pyenv install 3.9.6 && pyenv global 3.9.6

COPY requirements/requirements.dev.txt .
RUN pip install --no-cache-dir --upgrade pip-tools pip
RUN pip-sync requirements.dev.txt
RUN rm -f requirements.dev.txt

RUN brew install postgres || true
