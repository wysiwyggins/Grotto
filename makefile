build:
	@docker-compose -p grotto build
run:
	@docker-compose -p grotto up -d
stop:
	@docker-compose -p grotto down
migrations:
	@docker-compose -p grotto exec app python manage.py makemigrations
logs:
	@docker-compose -p grotto logs -f app
superuser:
	@docker-compose -p grotto exec app python manage.py createsuperuser
django-shell:
	@docker-compose -p grotto exec app python manage.py shell
shell:
	@docker-compose -p grotto exec app sh
lint:
	@docker-compose -p grotto exec app python -m pip install black==20.8b1 isort==5.8.0
	@docker-compose -p grotto exec app python -m black .
	@docker-compose -p grotto exec app python -m isort .