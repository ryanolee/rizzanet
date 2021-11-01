FROM tiangolo/uwsgi-nginx:python3.6

MAINTAINER "ryan<rizza@rizza.net>"

ENV NGINX_MAX_UPLOAD 0
ENV LISTEN_PORT 8080
ENV UWSGI_INI /app/rizzanet/config/uwsgi.ini
ENV STATIC_URL /static
ENV STATIC_PATH /app/static/
ENV STATIC_INDEX 0
ENV FLASK_APP app.py
ENV RIZZANET_ENV prod

EXPOSE 8080

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install --upgrade pip && pip install -r requirements.txt 
ENV PYTHONPATH=/app

COPY docker/rizzanet/scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY docker/rizzanet/scripts/prestart.sh /app/prestart.sh
RUN chmod +x /app/prestart.sh


COPY docker/rizzanet/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY docker/rizzanet/scripts/ /scripts/


RUN chmod -R +x /scripts/*

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]