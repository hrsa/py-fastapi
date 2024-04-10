#!/bin/bash
set -e

echo "DOMAIN is $DOMAIN"
echo "EMAIL is $EMAIL"

# Obtain the certificate if it does not exist
if [ ! -e "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
  echo "No certificates found! Creating ..."
  certbot certonly --webroot --webroot-path=/var/lib/letsencrypt --email $EMAIL --agree-tos --no-eff-email -d $DOMAIN -d www.$DOMAIN
fi

# Run a background job that tries to renew the certificate daily
while true
do
  echo "Time to renew certificates!"
  certbot renew
  sleep 1d
done