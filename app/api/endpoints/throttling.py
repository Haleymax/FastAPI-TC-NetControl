from fastapi import APIRouter, HTTPException, Query

from app.core.settings import NETWORK_INTERFACE
from app.utils.validation import check_tc_params
from app.utils.TrafficControl import TrafficControl
from app.utils.logger import logger
from app.model.models import Base, TC

tc_router = APIRouter()

@tc_router.post("/tc/add")
async def add(tc_data: TC):
    res_msg = {}
    return res_msg

@tc_router.get("/tc/remove")
async def remove(device: str = Query(None, description="device ip address")) :
    res_msg = {}
    logger.info(f"start cleaning operation")
    try:
        tc_client = TrafficControl(NETWORK_INTERFACE)
        result = tc_client.clear_tc(device)
        res_msg["success"] = True
        res_msg["interface"] = tc_client.interface
        res_msg["message"] = result
        return res_msg
    except Exception as e:
        logger.error(f"Traffic control setup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Traffic control setup failed: {e}")


@tc_router.post("/tc")
async def base_api(tc_data: Base):
    res_msg = {}
    result, message = check_tc_params(tc_data)
    if result:
        logger.info(message)
        logger.info(f"带宽为 {tc_data.rate}")
        logger.info(f"丢包率为 {tc_data.loss}")
        try:
            tc_client = TrafficControl(NETWORK_INTERFACE)
            result = tc_client.set_network(tc_data.rate, tc_data.loss, tc_data.ipaddr)
            res_msg["result"] = True
            res_msg["interface"] = tc_client.interface
            res_msg["message"] = result
        except Exception as e:
            logger.error(f"Traffic control setup failed: {e}")
            raise HTTPException(status_code=500, detail=f"Traffic control setup failed: {e}")
    else:
        res_msg["result"] = False
        res_msg["message"] = message
    return res_msg