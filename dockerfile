# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UVICORN_WORKERS=2 \
    UVICORN_PORT=8000

WORKDIR /app

# 시스템 의존성 (필요 최소)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 파이썬 의존성
COPY requirements.txt .
RUN pip install -r requirements.txt

# 앱 소스
COPY server.py ./server.py
COPY static ./static

# 비루트
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["bash", "-lc", "uvicorn server:app --host 0.0.0.0 --port ${UVICORN_PORT} --workers ${UVICORN_WORKERS}"]
