FROM node:18-alpine AS build_frontend

COPY ./frontend /frontend
WORKDIR /frontend

ARG DOCKER_TAG
ENV APP_VERSION=$DOCKER_TAG

RUN npm ci
RUN npm run build


FROM python:3.11-bullseye as run_base

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


FROM run_base AS rpi

RUN apt-get update && apt-get install -y chromium

# https://pypi.org/project/playwright/
#   See "Built Distributions" under "Download files"
RUN wget https://files.pythonhosted.org/packages/e1/3f/871db50c0aaf8d7764d0b53de28dcdd00c5ee1c32e27452a60a6da606130/playwright-1.40.0-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
RUN mv playwright-1.40.0-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl playwright.whl

RUN pip install playwright.whl
RUN pip install -r ./server/requirements.txt
RUN rm playwright-1.32.0-py3-none-any.whl

RUN rm $VIRTUAL_ENV/lib/python3.9/site-packages/playwright/driver/node && \
    ln -s /usr/bin/node $VIRTUAL_ENV/lib/python3.9/site-packages/playwright/driver/node

RUN playwright install-deps
RUN mkdir -p /app/pw-browser/chromium-1055/chrome-linux
RUN ln -s /usr/bin/chromium /app/pw-browser/chromium-1055/chrome-linux/chrome
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browser

CMD ["python", "-m", "server"]


FROM run_base AS any

RUN apt-get update && apt-get upgrade
RUN pip install -r ./server/requirements.txt
RUN playwright install-deps
RUN playwright install chromium

CMD ["python", "-m", "server"]
