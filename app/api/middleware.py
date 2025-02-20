import redis

from app.core.settings import get_redis_config


def is_ip_exist(redis_client, key, ip):
    all_ips = redis_client.lrange(key, 0, -1)
    decoded_ips = [ip.decode('utf-8') for ip in all_ips]
    return ip in decoded_ips


def is_list_empty(redis_client, key):
    return redis_client.llen(key)==0