FROM gitpod/workspace-full

ENV PYTHONUNBUFFERED 1

RUN brew update
RUN pyenv install $(pyenv install -l | grep 3.10 | head -n 1) && pyenv global $(pyenv install -l | grep 3.10 | head -n 1)

COPY requirements/requirements.dev.txt .
RUN pip install --no-cache-dir pip-tools==6.1.0
RUN pip-sync requirements.dev.txt
RUN rm -f requirements.dev.txt

RUN brew install postgres || true
