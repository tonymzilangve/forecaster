# FORECASTER
    Interactive API service.
    Fetch weather info for your city!

### STACK
`Django (DRF)  | PostgreSQL | Redis | Docker | Telegram Bot` 

## Common docker commands
### Build the images:
```bash
$ docker-compose build
```
### Run the containers:
```bash
$ docker-compose up -d
```

### Create migrations:
```bash
$ docker-compose exec api python manage.py makemigrations
```

### Apply migrations:
```bash
$ docker-compose exec api python manage.py migrate
```

### Run the tests:
```bash
$ docker-compose exec api pytest -p no:warnings
```

### Run the tests with coverage:
```bash
$ docker-compose exec api python -m pytest -p no:warnings --cov=.
```

### Lint:
```bash
$ docker-compose exec api python -m flake8 .
```
