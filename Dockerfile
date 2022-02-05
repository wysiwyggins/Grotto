FROM registry.gitlab.com/grotto/grotto-deps:latest-main

RUN apk add --no-cache libffi-dev build-base

RUN mkdir -p /app/src
RUN mkdir -p /app/svelte
WORKDIR /app/src

COPY requirements.txt /app/src/

RUN python -m pip install -r requirements.txt

RUN rm /app/src/requirements.txt

COPY entrypoint.sh /app/
RUN chmod -x /app/entrypoint.sh

COPY src /app/src
COPY svelte /app/svelte

RUN adduser -D worker -u 1000
RUN chown worker:worker -R /app/src
RUN chown worker:worker -R /app/svelte
USER worker

## setting debug triggers certain build behavior
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE=Grotto.settings.base
## https://stackoverflow.com/q/58712195/2754587
RUN python manage.py collectstatic --no-input
RUN python manage.py compress --force
RUN python manage.py collectstatic --no-input
RUN rm -rf static/

EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
