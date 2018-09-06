#! /usr/bin/env bash
echo '##################################'
echo '#            RIZZANET            #'
echo '#      Starting in dev mode      #'
echo '##################################'

#Fetch dev dependencies
python -m pip install -r /app/requirements-dev.txt &

#Make sure log files exsist
touch /var/log/rizzanet-dev.log
touch /var/log/rizzanet-dev.log.old

#Copy and clean old log files
cat /var/log/rizzanet-dev.log >> /var/log/rizzanet-dev.log.old
> /var/log/rizzanet-dev.log

#Start dev server and watch for css changes
bash /scripts/devserver.sh &
python -m flask assets watch >> /var/log/rizzanet-dev.log &

#Hang on tail -f (ing log file)
tail -f /var/log/rizzanet-dev.log