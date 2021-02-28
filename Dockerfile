FROM python:3.7-alpine

RUN apk add --no-cache libffi-dev build-base

RUN mkdir -p /app/src
WORKDIR /app/src

COPY requirements.txt /app/src/

RUN python -m pip install -r requirements.txt

RUN rm /app/src/requirements.txt

COPY src /app/src

COPY entrypoint.sh /app/
RUN chmod -x /app/entrypoint.sh

RUN adduser -D worker -u 1000
USER worker

EXPOSE 8000
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
