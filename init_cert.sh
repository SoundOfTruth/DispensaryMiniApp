#!/bin/sh

set -a
source .env
set +a

docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d "$DOMAIN" \
  -d "www.$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email