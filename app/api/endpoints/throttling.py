import redis
from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends

from app.api.middleware import is_ip_exist, is_list_empty, clear_all_values
from app.core.settings import NETWORK_INTERFACE, REDIS_HOST_KEY
from app.utils.generate_template import Template
from fastapi.responses import HTMLResponse

from app.utils.redis_util import get_redis_client
from app.utils.validation import check_tc_params, check_ip_address
from app.utils.TrafficControl import TrafficControl
from app.utils.logger import logger
from app.model.models import Base, TC

tc_router = APIRouter()

@tc_router.post("/tc/add")
async def add(tc_data: TC):
    res_msg = {}
    return res_msg

@tc_router.get("/tc/remove")
async def remove(device: str = Query(None, description="device ip address"), redis_client: redis.Redis= Depends(get_redis_client)) :
    """
    移除弱网配置，若传递了device参数就移除指定设备的弱网配置信息，没有就移除全局的配置信息
    :param redis_client: redis client
    :param device: 设备的ip地址
    :return: 将处理结果返回给前端以及现有的弱网信息也返回给前端
    """
    res_msg = {}
    logger.info(f"start cleaning operation")

    try:
        tc_client = TrafficControl(NETWORK_INTERFACE)
        if device and not check_ip_address(device):
                res_msg['result'] = False
                res_msg['interface'] = tc_client.interface
                res_msg['message'] = "invalid ip address"
                return res_msg
        if is_list_empty(redis_client, REDIS_HOST_KEY):
            res_msg['result'] = False
            res_msg['interface'] = tc_client.interface
            res_msg['message'] = "no device is set up"
            return res_msg

        if device and not is_ip_exist(redis_client, REDIS_HOST_KEY, device):
            res_msg['result'] = False
            res_msg['interface'] = tc_client.interface
            res_msg['message'] = "device not set up"
            return res_msg

        result = tc_client.clear_tc(device)
        res_msg["result"] = True
        res_msg["interface"] = tc_client.interface
        res_msg["message"] = result
        if device :
            redis_client.lpop(REDIS_HOST_KEY)
        else:
            clear_all_values(redis_client, REDIS_HOST_KEY)
        return res_msg
    except Exception as e:
        logger.error(f"Traffic control setup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Traffic control setup failed: {e}")


@tc_router.post("/tc")
async def base_api(tc_data: Base, redis_client: redis.Redis= Depends(get_redis_client)):
    """
    添加弱网配置
    :param tc_data: fastapi接收的数据模型
    :param redis_client: redis客户端
    :return: 将服务器处理后的数据返回给前端
    """
    res_msg = {}
    result, message = check_tc_params(tc_data)
    is_exist = is_ip_exist(redis_client, REDIS_HOST_KEY, tc_data.ipaddr)
    if result and not is_exist:
        logger.info(f"带宽为 {tc_data.rate}")
        logger.info(f"丢包率为 {tc_data.loss}")
        try:
            tc_client = TrafficControl(NETWORK_INTERFACE)
            result = tc_client.set_network(tc_data.rate, tc_data.loss, tc_data.ipaddr)
            res_msg["result"] = True
            res_msg["interface"] = tc_client.interface
            res_msg["message"] = result
            redis_client.lpush(REDIS_HOST_KEY, tc_data.ipaddr)
        except Exception as e:
            logger.error(f"Traffic control setup failed: {e}")
            raise HTTPException(status_code=500, detail=f"Traffic control setup failed: {e}")
    else:
        res_msg["result"] = False
        res_msg["message"] = message
        if is_exist:
            logger.info(f"ip address {tc_data.ipaddr} exist")
            res_msg["message"] = f"unable to set weak network configuration for ip {tc_data.ipaddr}, because the ip address already exists"
    return res_msg

@tc_router.get("/tc/show", response_class=HTMLResponse)
async def show():
    """
    该接口将现有的弱网配置信息展示到web页面上
    :return:将生成的页面返回给浏览器
    """
    tc_client = TrafficControl(NETWORK_INTERFACE)
    data = tc_client.show_tc_config()
    page = Template(data=data)
    return page.generate()