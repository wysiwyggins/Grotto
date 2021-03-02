# Grotto

## Dev setup

You're welcome to run your dev environment if you like, but here is the suggested pattern.

Be sure you have `docker` and `make` installed. Then `cd` into this directory. Use

* `make build` to build your dev docker image
* `make run` to run your dev instance (navigate browser to `localhost:8000` to interact)
* `make migrations` when you've changed the models (requires running instance)
* `make stop` to bring the instance down
* `make stop && make run` will apply any migrations
* `make logs` to follow the app logs
* `make superuser` to create a superuser for yourself

See `makefile` for complete list of command targets.

## Deployment

### Environment Variables

| Variable | Description |
|----------|-------------|
| APP_ENV  | Expresses which environment the app is running "dev" or "prod" |
| SECRET_KEY | Django secret key |
| DEBUG | Django debug setting (set to "False" in prod) |

### Droplet setup

Install docker and docker compose

```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Install nginx

```sh
apt install -y nginx
```

Set up nginx with ???


Set up docker compose by creating `/root/prod/docker-compose.yml` with contents like:
```
version: '3'

services:
  app:
    image: thismatters/grotto:latest
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=prod
      - DEBUG=False
    volumes:
      - ./db.sqlite:/app/src/db.sqlite3
    restart: always
```

Start grotto with (from `/root/prod/`)

```
docker-compose up -d
```
