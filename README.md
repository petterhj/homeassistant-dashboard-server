# homeassistant-inkplate-dashboard

...

## Development

### Configuration

Configured using `./.env`. See `./server/config.py` for options.

```sh
# .env
HOMEASSISTANT_HOST=http://homeassistant:8123/api
HOMEASSISTANT_TOKEN=
VITE_PROXY_HOST=http://localhost:8089
VITE_LOCALE=nb
```

```yml
# config.yml
dashboard:
  components:
    - type: vertical-stack
      style:
        gap: 2
      components:
        - type: weather-forecast
          entity: weather.forecast_oslo
          style:
            height: auto
          show:
            state: true
            forecast: true
          dateFormat: HH:mm

        - type: weather-forecast
          entity: weather.forecast_oslo
          show:
            state: false
```

```sh
make run      # Run server and frontend app
make run-ha   # Home Assistant test instance
```

### Server

```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r server/requirements.txt

$ playwright install # Download new browsers

$ python -m server # Start uvicorn server
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
