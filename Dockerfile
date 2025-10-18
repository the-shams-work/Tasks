# syntax=docker/dockerfile:1

# Build stage: install dependencies into a virtual environment
ARG PYTHON_VERSION=3.13-slim
FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/opt/venv/bin:$PATH"

# Create virtual environment for dependencies
RUN python -m venv /opt/venv

# Install build tools (only in builder) for any wheels that need compiling
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for better layer caching
COPY requirements.txt ./
RUN /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt

# Runtime stage: copy only what we need
FROM python:${PYTHON_VERSION} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

# Copy project content
COPY . /app

# Create non-root user
RUN addgroup --system app \
    && adduser --system --ingroup app app \
    && chown -R app:app /app
USER app

# Expose default FastAPI/uvicorn port
EXPOSE 8000
ENV PORT=8000

# Start the FastAPI app with uvicorn, binding to 0.0.0.0 for Docker
# We import the ASGI app directly rather than running main.py to ensure proper host binding
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
