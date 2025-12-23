FROM python:3.12-slim-trixie

RUN apt-get update && apt-get install -y libpq-dev gcc;

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY alembic.ini pyproject.toml uv.lock ./scripts/entrypoint.sh ./

COPY src ./src

COPY alembic ./alembic

ENV UV_NO_DEV=1

RUN uv sync --locked;

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
