# homeassistant-inkplate-dashboard

...

## Development

```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt -r requirements.dev.txt

$ playwright install # Download new browsers

$ python -m server # Start uvicorn server
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
