FROM node:18-alpine AS build_frontend

COPY ./frontend /frontend
WORKDIR /frontend

RUN npm ci
RUN npm run build


FROM python:3.9-bullseye

RUN mkdir -p /app/dist && mkdir /app/data

COPY ./server /app/server
COPY --from=build_frontend /frontend/dist /app/dist
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r ./server/requirements.txt
RUN playwright install-deps
RUN playwright install chromium

ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "server"]
