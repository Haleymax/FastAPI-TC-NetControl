# 网卡接口
NETWORK_INTERFACE = "wlan0"
# FastAPI Server的服务监听地址
FASTAPI_HOST = "0.0.0.0"
# FastAPI Server的监听端口
FASTAPI_PORT = 8008

# redis相关配置
REDIS_HOST = "10.86.97.89"
REDIS_PORT = 6379
TC_DATABASE = 0

def get_server_config():
    return FASTAPI_HOST, FASTAPI_PORT

def get_redis_config():
    return REDIS_HOST, REDIS_PORT, TC_DATABASE