FROM node:22-alpine AS build_frontend

COPY ./frontend /frontend
WORKDIR /frontend

RUN npm ci
RUN npm run build

FROM python:3.12-slim AS server

ARG DOCKER_TAG
ARG UID=1000
ARG GID=1000
ENV APP_VERSION=$DOCKER_TAG
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install system dependencies needed for Python packages and Playwright
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
        wget \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user with configurable UID/GID
RUN groupadd --gid ${GID} app && \
    useradd --uid ${UID} --gid ${GID} --create-home --shell /bin/bash app

# Create app directories with proper ownership
RUN mkdir -p /app/dist /app/data && \
    chown -R app:app /app

# Copy application files and set ownership
COPY --chown=app:app ./server /app/server
COPY --chown=app:app ./pyproject.toml /app/
COPY --chown=app:app ./uv.lock /app/
COPY --from=build_frontend --chown=app:app /frontend/dist /app/dist

WORKDIR /app

# Install project dependencies as root (needed for uv sync)
RUN uv sync --frozen

# Install Playwright browsers with system dependencies as root
RUN PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright uv run python -m playwright install --with-deps chromium && \
    chown -R app:app /app/ms-playwright

# Fix ownership of the entire app directory including virtual environment
RUN chown -R app:app /app

# Switch to non-root user for runtime
USER app
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright

CMD ["uv", "run", "python", "-m", "server"]
