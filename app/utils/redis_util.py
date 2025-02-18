import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """
        初始化 Redis 客户端
        :param host: Redis 服务器地址
        :param port: Redis 服务器端口
        :param db: 要使用的数据库编号
        :param password: Redis 服务器密码
        """
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True  # 自动解码响应数据
            )
            # 测试连接
            self.client.ping()
            print("成功连接到 Redis 服务器")
        except redis.exceptions.ConnectionError as e:
            print(f"无法连接到 Redis 服务器: {e}")
        except redis.exceptions.AuthenticationError as e:
            print(f"Redis 认证失败: {e}")

    def set_key(self, key, value, ex=None, px=None, nx=False, xx=False):
        """
        设置键值对
        :param key: 键
        :param value: 值
        :param ex: 过期时间（秒）
        :param px: 过期时间（毫秒）
        :param nx: 如果键不存在则设置
        :param xx: 如果键已存在则设置
        :return: 设置成功返回 True，否则返回 False
        """
        return self.client.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get_key(self, key):
        """
        获取键对应的值
        :param key: 键
        :return: 键对应的值，如果键不存在则返回 None
        """
        return self.client.get(key)

    def delete_key(self, key):
        """
        删除键
        :param key: 键
        :return: 删除成功返回删除的键的数量，否则返回 0
        """
        return self.client.delete(key)

    def hset(self, name, key, value):
        """
        在哈希表中设置字段和值
        :param name: 哈希表名称
        :param key: 字段名
        :param value: 字段值
        :return: 设置成功返回 1，字段已存在并更新则返回 0
        """
        return self.client.hset(name, key, value)

    def hget(self, name, key):
        """
        从哈希表中获取字段的值
        :param name: 哈希表名称
        :param key: 字段名
        :return: 字段的值，如果字段不存在则返回 None
        """
        return self.client.hget(name, key)

    def hdel(self, name, *keys):
        """
        从哈希表中删除指定的字段
        :param name: 哈希表名称
        :param keys: 要删除的字段名列表
        :return: 删除成功的字段数量
        """
        return self.client.hdel(name, *keys)

    def lpush(self, name, *values):
        """
        将一个或多个值插入到列表的头部
        :param name: 列表名称
        :param values: 要插入的值列表
        :return: 插入后列表的长度
        """
        return self.client.lpush(name, *values)

    def rpop(self, name):
        """
        移除并返回列表的最后一个元素
        :param name: 列表名称
        :return: 列表的最后一个元素，如果列表为空则返回 None
        """
        return self.client.rpop(name)

    def sadd(self, name, *values):
        """
        向集合中添加一个或多个成员
        :param name: 集合名称
        :param values: 要添加的成员列表
        :return: 添加成功的成员数量
        """
        return self.client.sadd(name, *values)

    def smembers(self, name):
        """
        获取集合中的所有成员
        :param name: 集合名称
        :return: 集合中的所有成员集合
        """
        return self.client.smembers(name)