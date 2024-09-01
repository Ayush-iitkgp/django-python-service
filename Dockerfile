FROM python:3.10.8

WORKDIR /workspace

COPY . .

RUN poetry install --no-root

RUN apt-get update && \
    apt-get install -y make postgresql postgresql-contrib postgresql-client && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000