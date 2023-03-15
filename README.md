# homeassistant-inkplate-dashboard

...

## Configuration

The server itself is configured using the environment variables specified below (see `server/models/server.py::ServerConfig` for defaults and more options).

```sh
# .env
DATA_PATH=data
HOST=127.0.0.1
PORT=8089
LOG_LEVEL=info
LOG_FILE=current.log
LOG_JSON=false
```

Other runtime config, including the dashboard itself, is defined in a YAML file (by default) called `configuration.yaml` placed at the root of the application data path (`DATA_PATH`).

```yml
# config.yml
homeassistant:
  host: !secret homeassistant_host
  port: 8123
  ssl: false
  token: !secret homeassistant_token

timezone: Europe/Oslo

locale:
  default: nb
  fallback: en

dashboard:
  components: !include components.yaml
```

### Components

#### Groups

#### Cards

##### Sun

```yaml
- type: sun
  entity: sun.sun
```

## Development

### Server

```sh
# .env
# ...
DEBUG=true
STATIC_PATH=frontend/dist
VITE_SERVER_URL=http://localhost:8089
```

```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r server/requirements.txt

$ playwright install [chromium]  # Download new browsers

$ python -m server [--data-path <path>] # Start uvicorn server
```

### Frontend

```
$ cd frontend/
$ npm install

$ npm run dev

$ npm run build
```

#### Home Assistant test instance

```sh
$ docker-compose -f dev/homeassistant/docker-compose.yml up
```

Username/password: `foobar`/`foobar`
