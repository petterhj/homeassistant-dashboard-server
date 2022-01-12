# homeassistant-inkplate-dashboard

## Config

To configure, update the necessary environment variables specified below in a `.env` file (automatically loaded through `config.py`).

| Variable | Default |
| --- | --- |
| DEBUG | `False` |
| HA_BASE_URL | `http://homeassistant.local:8123` |
| HA_DASHBOARD_URL | `/lovelace/default_view` |
| HA_ACCESS_TOKEN | `xxxx` |
| SERVER_PORT | `80` |
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

DEBUG=true python shotter.py
```
