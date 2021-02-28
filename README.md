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
