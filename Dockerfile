FROM python:3.13-slim as builder


RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir poetry

WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-root --no-ansi


FROM python:3.13-slim


COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app


COPY alembic.ini .
COPY migrations ./migrations
COPY app ./app

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host ${SERVER_HOST} --port ${SERVER_PORT}"]