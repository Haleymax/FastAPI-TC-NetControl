import redis

from app.core.settings import get_redis_config


def get_redis_client():
    host, port, db = get_redis_config()
    client = redis.Redis(host=host, port=port, db=db)
    try:
        yield client
    finally:
        client.close()