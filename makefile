build:
	@docker-compose -p grotto build
run:
	@docker-compose -p grotto up -d
stop:
	@docker-compose -p grotto down
migrations:
	@docker-compose -p grotto exec python manage.py makemigrations
logs:
	@docker-compose -p grotto logs app -f
superuser:
	@docker-compose -p grotto exec python manage.py createsuperuser
django-shell:
	@docker-compose -p grotto exec python manage.py shell
shell:
	@docker-compose -p grotto exec sh
