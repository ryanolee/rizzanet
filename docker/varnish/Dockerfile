FROM debian:stretch-slim

#Install varnish 6.0
RUN apt-get update && \
    apt-get install debian-archive-keyring curl gnupg apt-transport-https gettext -y && \
    curl -L https://packagecloud.io/varnishcache/varnish60/gpgkey | apt-key add - && \
    echo " \
deb https://packagecloud.io/varnishcache/varnish60/debian/ stretch main \
deb-src https://packagecloud.io/varnishcache/varnish60/debian/ stretch main \
    " > /etc/apt/sources.list.d/varnishcache_varnish60.list && \
    apt-get update && \
    apt-get install varnish -y

COPY ./scripts/* /scripts/




ENV VARNISH_BACKEND_HOST localhost
ENV VARNISH_BACKEND_PORT 8080
ENV VARNISH_BACKEND_MAX_CONNECTIONS 300
ENV VARNISH_PORT 81
ENV VARNSIH_BACKEND_BAN 0.0.0.0

EXPOSE ${VARNISH_PORT}

RUN chmod -R 755 /scripts
ENTRYPOINT '/scripts/docker-varnish-entrypoint.sh'