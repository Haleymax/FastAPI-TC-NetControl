import re

import ipaddress

from app.model.models import Base


def check_tc_params(tc: Base):
    if not isinstance(tc.loss, (int, float)) or not 0 <= tc.loss <= 100:
        return False, "Loss must be 0-100"

    if not isinstance(tc.rate, str) or not tc.rate.lower().endswith(("bit", "bps")):
        return False, "Invalid rate format (e.g. 10Mbit)"
    try:
        ipaddress.ip_address(tc.ipaddr)
    except ValueError:
        return False, "Invalid IP address format"
    
    return True, "Parameters are valid"


