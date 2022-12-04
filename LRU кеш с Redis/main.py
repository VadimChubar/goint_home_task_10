import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client, default_ttl=10, max_size=100)


@cache
def f(x):
    print(f"LRU кеш с Redis f({x})")
    result = x * 1000
    return result


f(30)
f(3000)