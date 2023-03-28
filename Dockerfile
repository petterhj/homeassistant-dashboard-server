FROM node:18-alpine AS build_frontend

COPY ./frontend /frontend
WORKDIR /frontend

RUN npm ci
RUN npm run build


FROM python:3.9-bullseye as run_base

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
RUN wget https://files.pythonhosted.org/packages/c8/7d/b8c0d1e6e446704522773be63f1807af22390a796c9cc7b06e20d366907d/playwright-1.32.0-py3-none-manylinux1_x86_64.whl
RUN mv playwright-1.32.0-py3-none-manylinux1_x86_64.whl playwright-1.32.0-py3-none-any.whl

RUN pip install playwright-1.32.0-py3-none-any.whl
RUN pip install -r ./server/requirements.txt

RUN rm $VIRTUAL_ENV/lib/python3.9/site-packages/playwright/driver/node && \
    ln -s /usr/bin/node $VIRTUAL_ENV/lib/python3.9/site-packages/playwright/driver/node

RUN playwright install-deps
RUN mkdir -p /app/pw-browser/chromium-1048/chrome-linux
RUN ln -s /usr/bin/chromium /app/pw-browser/chromium-1048/chrome-linux/chrome
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browser

CMD ["python", "-m", "server"]


FROM run_base AS any

RUN pip install -r ./server/requirements.txt
RUN playwright install-deps
RUN playwright install chromium

CMD ["python", "-m", "server"]
