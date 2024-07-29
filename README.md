# homeassistant-dashboard-server

A simple, customizable Home Assistant dashboard that can be used as a "backend" for wall-mounted displays like the [Inkplate 10](#inkplate). The server automatically captures screenshots of the dashboard at configured interval, and is an alternative to other similar software like [sibbl/hass-lovelace-kindle-screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver), and at the same time an alternative to dealing with [kiosk-mode](https://github.com/maykar/kiosk-mode), [card-mod](https://github.com/thomasloven/lovelace-card-mod) and [layout-card](https://github.com/thomasloven/lovelace-layout-card) plugins for Home Assistant.

<div align="center">
  <img src="/screenshots/v023_screenshot.png?raw=true" alt="screenshot_1200_825">
</div>

#### Inkplate

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
# configuration.yml
homeassistant:
  url: !secret homeassistant_url
  token: !secret homeassistant_token

timezone: Europe/Oslo

locale:
  default: nb
  fallback: en

dashboard:
  components: !include components.yaml

capture:
  timeout: 10000
  width: 1200
  height: 825
```

```yml
# components.yaml
- type: vertical-stack
  style: gap-12
  components:
    - type: weather-forecast
      entity: weather.oslo_hourly
      show:
        state: true
        forecast: true
      dateFormat: HH:mm
    - type: weather-graph
      entity: weather.oslo_hourly
      attribute: temperature
      show:
        labels: true
      dateFormat: HH
    - type: sun
    - type: weather-forecast
      entity: weather.oslo
      show:
        state: false

# - type: vertical-stack
#   style: gap-12
#   components:
#     ...
```

```yml
# secrets.yaml
homeassistant_url: http://ha.lan
homeassistant_token:
```

### Components

#### Groups

```yaml
- type: horizontal-stack
  components:
    - type: vertical-stack
      style: gap-2
      components:
        - type: ...
```

#### Cards

```yaml
- type: ...
  title: ...
  icon: ...
```

##### Entities

```yaml
- type: entities
  display: list (default) | grid | grouped
  columns: 2 (default, when using `grid`)
  entities:
    - sensor.power_consumption
    - entity: sensor.electricity_price
      precision: 2
      secondaryInfo: last-changed
    - entity: sensor.monthly_electricity_cost
      precision: 0
      unit: kr
      name: Monthly cost
      icon: cash
      secondaryInfo: sensor.electricity_price
    - entity: sun.sun
      secondaryInfo: attribute.next_dawn
  # ...
  groups: # optional
    - id: temp
      title: Temperatures
      icon: thermometer
  entities:
    - entity: climate.heater
      group: temp
      attribute: temperature
      unit: °C
    - entity: sensor.temp2
      group: temp
```

##### Graph

```yaml
- type: graph
  entity: sensor.download_speed
  unit: null (default, uses `unit_of_measurement`)
  xAxis: false | true (default) | { min, max }
  yAxis: false | true (default) | { min, max }
  targetResolution: null (default) | <number>
  labels: [true | false | 'min' + 'max' (default)]
  annotations: [average, <number:yval> ...] (default)
```

##### Sun

```yaml
- type: sun
  entity: sun.sun # optional, default
```

##### Weather Forecasst

```yaml
- type: weather-forecast
  entity: weather.home
  state: true (default) | false 
  forecast: true | 'daily' | 'hourly' (default) | false
```

##### Weather Graph

```yaml
- type: weather-graph
  entity: weather.home
  attribute: temperature (default)
  unit: null (default, uses `{attribute}_unit`)
  includeForecast: true (default) | false 
  includeHistory: true (default) | false
  forecastType: daily | hourly (default) | twice_daily
  annotations: [now, startOfDay, endOfDay] (default)
```

##### Calendar

```yaml
- type: calendar
  limit: 10 (default) # Limit events
  calendars: # Optional list of calendars to include (defaults to all calendar entities)
    - entity: calendar.work
      icon: flag # defaults to card icon
      showDescription: true (default) | false
      showCalendarName: true (default) | false
      filterBegun: false (default) | true # Filter events that have begun
```


##### Todo List

```yaml
- type: todo-list
  entity: todo.shopping
```

##### RSS

```yaml
- type: rss
  url: https://www.nrk.no/toppsaker.rss
  limit: 10 (default)
```

##### Transmission

```yaml
- type: transmission
  entity: sensor.transmission_total_torrents # optional, default
  limit: 15 (default)
  dateFormat: HH:mm (default)
  lineClamp: 3 (default)
  showCategories: true (default)
  showDescription: true (default)
```

##### Petcare

```yaml
- type: petcare
  petEntity: binary_sensor.cat
  hubEntity: binary_sensor.hub
  flapBatteryEntity: sensor.hub_battery_level
  flapConnectivityEntity: binary_sensor.hub_connectivity
```

##### Markdown

```yaml
- type: markdown
  entity: sensor.markdown
  attribute: description
  # or
  content: |
    # Foo
    Bar
```

## Build and run

```sh
$ docker build \
  --tag inkplate-dashboard:latest \
  --tag inkplate-dashboard:<version> \
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
# Setup
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r server/requirements.txt -r server/requirements.dev.txt

$ playwright install [chromium]  # Download new browsers
$ playwright install-deps

# Start development server (uvicorn)
$ python -m server [--data-path <path>]

# Linting
$ black server/
```

### Frontend

```sh
$ cd frontend/
$ npm install

$ npm run dev

$ npm run build
```

### Bump version

```sh
$ bumpversion [major|minor|patch]
$ git push --tags
```

#### Home Assistant test instance

```sh
$ docker-compose -f dev/homeassistant/docker-compose.yml up
```

Username/password: `foobar`/`foobar`.
