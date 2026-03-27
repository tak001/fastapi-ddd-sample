FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml ./
RUN uv sync --frozen --no-install-project --extra dev 2>/dev/null || uv sync --no-install-project --extra dev

COPY src/ ./src/
COPY tests/ ./tests/

ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser --system --no-create-home appuser
USER appuser

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
