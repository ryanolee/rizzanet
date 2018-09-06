#! /usr/bin/env bash
while `true`
do
  python app.py >> /var/log/rizzanet-dev.log
  echo "Error: rizzanet dev server unexpectedly quit. Restarting in 5 seconds!" 
  sleep 5
done