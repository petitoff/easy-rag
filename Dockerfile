FROM python:3.12-slim AS builder
RUN pip install uv
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Sync deps and install the package (non-editable for Docker)
RUN uv sync --frozen --no-dev && \
    uv pip install .

FROM python:3.12-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libstdc++6 \
    libgcc1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN useradd --create-home --shell /bin/bash appuser

# Copy virtual env and source code from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src

RUN chmod -R +x /app/.venv/bin/* && \
    chown -R appuser:appuser /app

USER appuser
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "easyrag.main:app", "--host", "0.0.0.0", "--port", "8000"]

