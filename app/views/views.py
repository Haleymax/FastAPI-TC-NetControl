from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from check_tc_params import check_tc_params
from app.utils.TrafficControl import TrafficControl
from app.utils.logger import logger
router = APIRouter()
network_interface = "wlan0"

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
        logger.info(f"丢包率为 {tc_data.loss}")
        try:
            tc = TrafficControl(network_interface)
            result = tc.set_network(tc_data.rate, tc_data.loss, tc_data.ipaddr)
            res_msg["result"] = True
            res_msg["message"] = result
        except Exception as e:
            logger.error(f"Traffic control setup failed: {e}")
            raise HTTPException(status_code=500, detail=f"Traffic control setup failed: {e}")
    else:
        res_msg["result"] = False
        res_msg["message"] = message
    return res_msg