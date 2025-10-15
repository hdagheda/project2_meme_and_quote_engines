# syntax=docker/dockerfile:1

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=3000 \
    FLASK_APP=app.py

# Minimal OS packages; curl used for HEALTHCHECK (optional)
RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl; \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and working directory
RUN useradd --create-home --shell /usr/sbin/nologin appuser
WORKDIR /app

# Install Python dependencies first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser

# Expose the Flask port
EXPOSE 3000

# Optional healthcheck (adjust path if needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -fsS "http://127.0.0.1:${PORT}/" || exit 1

# Run the app using the provided command
CMD [ "sh", "-lc", "flask run --host 0.0.0.0 --port ${PORT} --reload" ]
