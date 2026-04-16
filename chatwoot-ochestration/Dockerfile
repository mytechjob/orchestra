# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build deps for packages that need compilation (e.g. cryptography, asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

WORKDIR /app

# Runtime system lib for psycopg2 / asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY main.py .
COPY src/ ./src/

# Expose FastAPI port
EXPOSE 8000

# Use uvicorn for production (reload disabled)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
