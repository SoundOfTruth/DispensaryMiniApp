FROM redis:latest

COPY redis.conf /usr/local/etc/redis/redis.conf

CMD ["sh", "-c", "redis-server --requirepass $REDIS_PASSWORD"]