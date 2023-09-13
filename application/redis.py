import redis
from application.config import parseConfig

redisLocal = parseConfig("redis_local", "/etc/anrari.conf", "=", "redis")

redis_conn = redis.StrictRedis(host=redisLocal.host, port=redisLocal.port, password=redisLocal.password)