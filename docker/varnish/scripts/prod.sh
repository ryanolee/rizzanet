#! /usr/bin/env bash
echo "Starting rizzanet varnish in prod mode..."

echo "Building config file..."

(envsubst < /scripts/default-template.vcl) > /scripts/default.vcl

#Checking syntax
echo "Checking syntax ..."

varnishd -C -f /scripts/default.vcl > /dev/null

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "Looks good! loading..."
    cp /scripts/default.vcl /etc/varnish/rizzanet.vcl 
    varnishd -f /etc/varnish/rizzanet.vcl -a :${VARNISH_PORT}
    varnishncsa
else
  echo "Error loading the varnish file failed."
fi
