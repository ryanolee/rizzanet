FROM tiangolo/uwsgi-nginx:python3.6

ENV NGINX_MAX_UPLOAD 0
ENV LISTEN_PORT 8080
ENV UWSGI_INI /app/rizzanet/config/uwsgi.ini
ENV STATIC_URL /static
ENV STATIC_PATH /app/static/
ENV STATIC_INDEX 0
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

EXPOSE 8080

COPY . /app

# Install elastic search
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

RUN export JAVA_HOME

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.0.deb && \
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.0.deb.sha512 && \
shasum -a 512 -c elasticsearch-6.3.0.deb.sha512 && \
dpkg -i elasticsearch-6.3.0.deb

# Build rizzanet admin app
WORKDIR /app/rizzanet/admin/admin_app/
RUN curl -sL  https://deb.nodesource.com/setup_9.x | bash - && apt-get install -y nodejs && curl -o- -L https://yarnpkg.com/install.sh | bash 
RUN $HOME/.yarn/bin/yarn install --pure-lockfile && $HOME/.yarn/bin/yarn build_rizzanet

WORKDIR /app

RUN pip install -r requirements.txt 
ENV PYTHONPATH=/app

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

COPY docker/prestart.sh /app/prestart.sh
RUN chmod +x /app/prestart.sh


COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]