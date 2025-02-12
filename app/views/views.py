from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.common.check_format import check_tc_params
from app.utils.TrafficControl import TrafficControl
from app.utils.logger import logger

router = APIRouter()

network_interface = "eth0"

class TC(BaseModel):
    rate: Optional[str] = None
    delay: Optional[int] = None
    loss: Optional[float] = None
    ip_address: str  # 新增 IP 地址字段

@router.get("/hello")
def index():
    return {"message": "Hello World"}

@router.post("/tc")
async def tc(tc_data: TC):
    res_msg = {}
    result, message = check_tc_params(tc_data)
    if result:
        logger.info(message)
        logger.info(f"带宽为 {tc_data.rate}")
        logger.info(f"延迟为 {tc_data.delay}")
        logger.info(f"丢包率为 {tc_data.loss}")
        logger.info(f"IP 地址为 {tc_data.ip_address}")

        try:
            tc = TrafficControl(network_interface)
            tc.setup_tc(tc_data.rate, tc_data.delay, tc_data.loss, tc_data.ip_address)  # 传递 IP 地址
            res_msg["result"] = True
            res_msg["message"] = "切换成功"
        except Exception as e:
            logger.error(f"Traffic control setup failed: {e}")
            raise HTTPException(status_code=500, detail=f"Traffic control setup failed: {e}")

    else:
        res_msg["result"] = False
        res_msg["message"] = message

    return res_msg
