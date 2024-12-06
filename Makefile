build:
	docker-compose build

run:
	docker-compose up

migrations:
	docker-compose exec api python manage.py makemigrations

migrate:
	docker-compose exec api python manage.py migrate

superuser:
	docker-compose exec api python manage.py createsuperuser

shell:
	docker-compose run --rm api shell

test:
	docker-compose run --rm api pytest
