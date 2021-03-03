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
