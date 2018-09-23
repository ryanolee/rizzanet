#! /usr/bin/env bash


if [[ $VARNISH_ENV == 'dev' ]] ; then 
  source /scripts/dev.sh
else
  source /scripts/prod.sh
fi

