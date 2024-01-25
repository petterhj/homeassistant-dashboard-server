FROM node:18-alpine AS build_frontend

COPY ./frontend /frontend
WORKDIR /frontend

RUN npm ci
RUN npm run build

FROM python:3.11-bullseye as serve

ARG DOCKER_TAG
ENV APP_VERSION=$DOCKER_TAG
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update && \
    apt-get install -y \
        nodejs

RUN mkdir -p /app/dist && mkdir /app/data

COPY ./server /app/server
COPY --from=build_frontend /frontend/dist /app/dist
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install --upgrade pip
RUN pip install -r ./server/requirements.txt

RUN PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright python -m playwright install --with-deps chromium
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright

CMD ["python", "-m", "server"]
