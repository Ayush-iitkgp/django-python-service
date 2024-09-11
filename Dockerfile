FROM python:3.10.8

WORKDIR /opt/django-python-service

COPY pyproject.toml poetry.lock ./
COPY app app/
COPY manage.py ./
COPY Makefile ./
COPY translation translation/
COPY tests tests/

ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.6.1
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

EXPOSE 8000
