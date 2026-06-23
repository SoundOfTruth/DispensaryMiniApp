#!/bin/bash

if [ -f .env.certbot ]; then
    export $(grep -v '^#' .env.certbot | xargs)
else
    echo "Ошибка: файл .env.certbot не найден!"
    exit 1
fi


if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    echo "Ошибка: переменные DOMAIN и EMAIL должны быть определены в .env.certbot файле"
    exit 1
fi


docker run -it --rm \
  -v $(pwd)/certbot/conf:/etc/letsencrypt \
  -v $(pwd)/certbot/www:/var/www/certbot \
  -p 80:80 \
  certbot/certbot certonly \
  --standalone \
  -d $DOMAIN \
  -d www.$DOMAIN \
  --email $EMAIL \
  --agree-tos \
  --no-eff-email