# Health Coach AI System - Multi-stage Docker Build

# ============================================================================
# Base Stage - Common dependencies
# ============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.6.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create app user for security
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --shell /bin/bash --create-home app

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================================
# Development Stage
# ============================================================================
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    pytest-mock \
    black \
    isort \
    flake8 \
    mypy \
    jupyter \
    ipython

# Copy source code
COPY --chown=app:app . .

# Switch to app user
USER app

# Expose development port
EXPOSE 8000

# Development command with hot reload
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================================================
# Testing Stage
# ============================================================================
FROM development as testing

# Copy test files
COPY --chown=app:app tests/ tests/
COPY --chown=app:app pytest.ini .
COPY --chown=app:app .coveragerc .

# Run tests
RUN python -m pytest tests/ --cov=agents --cov=teams --cov=workflows --cov-report=html --cov-report=term

# ============================================================================
# Production Stage
# ============================================================================
FROM base as production

# Install production-only dependencies
RUN pip install --no-cache-dir \
    gunicorn \
    uvicorn[standard] \
    prometheus-client \
    structlog

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/backups && \
    chown -R app:app /app

# Copy application code
COPY --chown=app:app agents/ agents/
COPY --chown=app:app teams/ teams/
COPY --chown=app:app workflows/ workflows/
COPY --chown=app:app tools/ tools/
COPY --chown=app:app database/ database/
COPY --chown=app:app config/ config/
COPY --chown=app:app main.py .
COPY --chown=app:app requirements.txt .

# Copy configuration files
COPY --chown=app:app config/production/ config/production/

# Switch to app user for security
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose application port
EXPOSE 8000

# Production command with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--max-requests", "1000", "--max-requests-jitter", "100", "--preload", "--access-logfile", "-", "--error-logfile", "-", "main:app"]

# ============================================================================
# Worker Stage - Background task processing
# ============================================================================
FROM production as worker

# Switch to app user
USER app

# Worker-specific command
CMD ["python", "-m", "workers.task_worker", "--loglevel=info", "--concurrency=4"]

# ============================================================================
# Nginx Stage - Static file serving and reverse proxy
# ============================================================================
FROM nginx:alpine as nginx

# Copy nginx configuration
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/nginx/ /etc/nginx/conf.d/

# Copy SSL certificates (if available)
COPY config/ssl/ /etc/nginx/ssl/

# Create log directory
RUN mkdir -p /var/log/nginx

# Health check for nginx
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Expose HTTP and HTTPS ports
EXPOSE 80 443