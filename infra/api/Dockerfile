FROM python:3.12-slim
ENV POETRY_VERSION=2.1.3

WORKDIR .

RUN apt-get update && apt-get install -y build-essential libpq-dev curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry==$POETRY_VERSION && \
    poetry config virtualenvs.create false

COPY infra/api/pyproject.toml infra/api/poetry.lock ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY infra/api/entrypoint.sh infra/api/run_tests.sh infra/api/log_config.yaml ./

RUN chmod +x entrypoint.sh
RUN chmod +x run_tests.sh

COPY ./api .
EXPOSE 8000
