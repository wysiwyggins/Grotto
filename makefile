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
node-logs:
	@docker-compose -p grotto logs -f node
superuser:
	@docker-compose -p grotto exec app python manage.py createsuperuser
django-shell:
	@docker-compose -p grotto exec app python manage.py shell
shell:
	@docker-compose -p grotto exec app sh
node-shell:
	@docker-compose -p grotto exec node sh
lint:
	@docker-compose -p grotto exec app python -m pip install black==20.8b1 isort==5.8.0
	@docker-compose -p grotto exec app python -m black .
	@docker-compose -p grotto exec app python -m isort . --profile black