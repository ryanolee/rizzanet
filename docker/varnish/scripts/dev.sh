#! /usr/bin/env bash
echo "Starting rizzanet varnish in dev mode..."

echo "Building config file..."

load_in_vcl()
{
    echo "Building config file..."

    (envsubst < /scripts/default-template.vcl) > /scripts/default.vcl

    #Checking syntax
    echo "Checking syntax ..."

    varnishd -C -f /scripts/default.vcl > /scripts/varnish_compile_error.log

    RESULT=$?

    if [ $RESULT -eq 0 ]; then
        echo "Looks good! loading..."
        cp /scripts/default.vcl /etc/varnish/rizzanet.vcl 
        start_varnish >> /var/log/varnish/rizzanet-dev.log
    else
        echo "Error loading the varnish file failed."
        cat /scripts/varnish_compile_error.log >> /var/log/varnish/rizzanet-dev.log
    fi
    echo 'Reload end.'
}

watcher(){
    varnishd -f /etc/varnish/default.vcl -a :${VARNISH_PORT} >> /var/log/varnish/rizzanet-dev.log
    load_in_vcl >> /var/log/varnish/rizzanet-dev.log
    LTIME=`stat -c %Z /scripts/default-template.vcl`

    while true    
    do
        ATIME=`stat -c %Z /scripts/default-template.vcl`

        if [[ "$ATIME" != "$LTIME" ]]
        then    
            load_in_vcl >> /var/log/varnish/rizzanet-dev.log
            
            LTIME=$ATIME
        fi
        sleep 5
    done

    
    #inotifywait -q -m -e close_write --format %e /scripts/default-template.vcl |
    #while read events; do
    #     echo "Changes!" 
    #done
}

start_varnish(){
    TIME=$(date +%s)
    varnishadm vcl.load rizzanet_dev_vcl_$TIME /etc/varnish/rizzanet.vcl
    varnishadm vcl.use rizzanet_dev_vcl_$TIME
}


touch /var/log/varnish/rizzanet-dev.log
> /var/log/varnish/rizzanet-dev.log

watcher &

varnishlog >> /var/log/varnish/rizzanet-dev.log &

tail -f /var/log/varnish/rizzanet-dev.log

