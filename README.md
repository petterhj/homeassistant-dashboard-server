# homeassistant-inkplate-dashboard

...

## Development

### Server

```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt -r requirements.dev.txt

$ playwright install # Download new browsers

$ python -m server # Start uvicorn server
```

### Frontend

```
$ cd frontend/
$ npm install
$ npm run dev
```

#### Home Assistant test instance

```sh
$ docker-compose -f dev/homeassistant/docker-compose.yml up
```

Username/password: `foobar`/`foobar`
