# py-schedule-compose

A better way to implement Python [schedule](https://schedule.readthedocs.io/en/stable/) module.

## Features

* Handle unexpected exceptions.
* Support parallel execution.
* Run pip install automatically.
* Stop container gracefully.
* Telegram bot integrated.

## Get started

### Create .env file.

```
cp .env.default .env
```

### Run container.

```
# Create and run
docker-compose up -d

# Remove container
# -v is required, so that the volume for temp file would be removed also.
docker-compose down -v
```

## Make your own job

TODO
