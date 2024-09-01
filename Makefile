default: help

help:
	@echo "make format"
	@echo "make run"
	@echo "make migrate"
	@echo "make create-migration"
	@echo "make create-superuser"
	@echo "make create-cachetable"
	@echo "make bootstrap"

format:
	isort app translation
	black app translation

run:
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

create-migration:
	python manage.py makemigrations

create-superuser:
	python manage.py createsuperuser

create-cachetable:
	python manage.py createcachetable

bootstrap:
	make migrate translation && make migrate && make create-cachetable