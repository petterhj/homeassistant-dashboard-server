# homeassistant-inkplate-dashboard

## Inkplate

> Inkplate 10 is a powerful, energy-efficient, Wi-Fi enabled ESP32 board with a recycled 9.7 inch e-paper display. It’s open hardware supported by an open-source software library, and it’s easy to program, regardless of whether you prefer MicroPython or the Arduino IDE.

The Inkplate MCU must be programmed to periodically download and display the captured dashboard image. See samples in the `inkplate/` folder for how to do this, either by using the [Arduino](https://github.com/SolderedElectronics/Inkplate-Arduino-library/)-based sketch or the config file for using the Inkplate with [ESPHome](http://esphome.io/). Another excellent alternative, is to use the [PlatformIO](https://platformio.org/)-based solution [lanrat/homeplate](https://github.com/lanrat/homeplate).

* [Inkplate: Get Started Page](https://inkplate.readthedocs.io/en/latest/get-started.html)
* [ESPHome: Inkplate 6, 10 and 6 Plus](https://esphome.io/components/display/inkplate6.html)


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

Other runtime config, including the dashboard itself, is defined in a YAML file called `configuration.yaml` placed at the root of the application data path (`DATA_PATH`).

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

## Build and run

```sh
$ docker build \
  --target rpi \ # Build for Raspberry Pi (armv7l)
  --tag inkplate-dashboard:latest \
  .

$ docker run \
  -p 9090:8000 \
  -v $(pwd)/data:/app/data \
  --name inkplate-dashboard \
  --rm \
  inkplate-dashboard
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
