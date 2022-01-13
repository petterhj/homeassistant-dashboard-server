# homeassistant-inkplate-dashboard

Simple app for capturing and hosting screenshots of a specified Home Assistant dashboard. Based on [itobey/hass-lovelace-screenshotter](https://github.com/itobey/hass-lovelace-screenshotter) (fork of [sibbl/hass-lovelace-kindle-screensaver](https://github.com/sibbl/hass-lovelace-kindle-screensaver)), rewritten using Python and [Playwright](https://playwright.dev/).

## Config

To configure, update the necessary environment variables specified below in a `.env` file (or see `hashotter/config.py`).

| Variable | Default |
| --- | --- |
| DEBUG | `False` |
| HA_BASE_URL | `http://homeassistant.local:8123` |
| HA_DASHBOARD_URL | `/lovelace/default_view` |
| HA_ACCESS_TOKEN | `xxxx` |
| SERVER_HOST | `0.0.0.0` |
| SERVER_PORT | `80` |
| SERVER_OUTPUT_PATH | `/dashboard.png` |
| SCREENSHOT_HEIGHT | `825` |
| SCREENSHOT_WIDTH | `1200` |
| SCREENSHOT_SCALING | `1` |
| SCREENSHOT_TIMEOUT | `10000` |
| SCREENSHOT_DELAY | `15` |
| SCREENSHOT_OUTPUT_PATH | `output/ha.png` |
| SCREENSHOT_INTERVAL | `600` |

## Development

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

playwright install # Download new browsers

DEBUG=true python app.py
```

## Build and run

```sh
docker build -t hashot .
docker run \
    --env-file .env \
    -p 8081:80 \
    --name hasshot \
    --detach \
    hashot
```
