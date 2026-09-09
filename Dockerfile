# ---- Build stage: compile deps that need gcc/libpq headers ----
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Runtime stage: slim, no compilers, non-root ----
FROM python:3.10-slim

WORKDIR /app

# libpq5 (runtime lib for psycopg2) without the -dev headers/gcc
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN mkdir -p uploads && chown -R appuser:appuser /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["./start.sh"]
