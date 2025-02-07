from netrc import netrc

from fastapi import APIRouter

from app.common.check_format import check_tc_params
from app.model.models import TC
from app.utils.TrafficControl import TrafficControl
from app.utils.logger import logger

router = APIRouter()

network_interface = "eth0"

@router.get("/hello")
def index():
    return {"message": "Hello World"}

@router.post("/tc")
async def tc(tc_data:TC):
    res_msg = {}
    result, message = check_tc_params(tc_data)
    if result:
        logger.info(message)
        logger.info(f"带宽为 {tc_data.rate}")
        logger.info(f"延迟为 {tc_data.delay}")
        logger.info(f"丢包率为 {tc_data.loss}")
        res_msg["result"] = True
        res_msg["message"] = "切换成功"

        tc = TrafficControl(network_interface)
        tc.setup_tc(tc_data.rate, tc_data.delay, tc_data.loss )


    else:
        res_msg["result"] = False
        res_msg["message"] = message

    return res_msg