FROM tiangolo/uwsgi-nginx:python3.6

ENV NGINX_MAX_UPLOAD 0
ENV LISTEN_PORT 8080
ENV UWSGI_INI /app/rizzanet/config/uwsgi.ini
ENV STATIC_URL /static
ENV STATIC_PATH /app/static/
ENV STATIC_INDEX 0
ENV FLASK_APP=app.py

EXPOSE 8080

COPY . /app


# Build rizzanet admin app
WORKDIR /app/rizzanet/admin/admin_app/
RUN curl -sL  https://deb.nodesource.com/setup_9.x | bash - && apt-get install -y nodejs && curl -o- -L https://yarnpkg.com/install.sh | bash 
RUN $HOME/.yarn/bin/yarn install --pure-lockfile && $HOME/.yarn/bin/yarn build_rizzanet && $HOME/.yarn/bin/yarn global bin

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt 
ENV PYTHONPATH=/app

COPY docker/rizzanet/scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY docker/rizzanet/scripts/prestart.sh /app/prestart.sh
RUN chmod +x /app/prestart.sh


COPY docker/rizzanet/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]