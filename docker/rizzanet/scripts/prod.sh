#! /usr/bin/env bash
echo '##################################'
echo '#            RIZZANET            #'
echo '#      Starting in prod mode     #'
echo '##################################'

touch /var/log/rizzanet-prod.log
touch /var/log/rizzanet-prod.log.old

#Copy and clean old log files
cat /var/log/rizzanet-prod.log >> /var/log/rizzanet-prod.log.old
> /var/log/rizzanet-prod.log

# Start Supervisor, with Nginx and uWSGI in dameon
touch /var/log/rizzanet-prod.log
exec nohup /usr/bin/supervisord >> /var/log/rizzanet-prod.log &
tail -f /var/log/rizzanet-prod.log