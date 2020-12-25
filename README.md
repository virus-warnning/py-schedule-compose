# py-schedule-compose

A better way to implement Python [schedule](https://schedule.readthedocs.io/en/stable/) module.

I'd just like to run several spiders on my NAS, so create this repository to test.

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
```

### What's happened?

There are two default jobs in the project:

* good_job(): run per 3 seconds.
* bad_job(): run per 10 seconds and throw an unhandled exception.

### Screenshot

![screenshot](https://imgur.com/effu4di)

### Remove container
```
# Remove container
# -v is required, so that the volume for temp file would be removed also.
# Without -v option, pip install would not run next time. 
docker-compose down -v
```

## Make your own job

### Add a job.

### Add a job which using 3rd party package.

### Add a job to generate some data.

### Set Telegram bot to received unexpected exception.

### Set timezone.
