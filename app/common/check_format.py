import re
# 验证IP地址格式
import ipaddress

from app.model.models import TC


def check_tc_params(tc: TC):
    # 验证 loss 是否为数字且在 0 到 100 之间
    if not isinstance(tc.loss, (int, float)) or not 0 <= tc.loss <= 100:
        raise ValueError("Loss must be 0-100")
    
    # 验证速率格式
    if not isinstance(tc.rate, str) or not tc.rate.lower().endswith(("bit", "bps")):
        raise ValueError("Invalid rate format (e.g. 10Mbit)")
    
    # 验证 IP 地址格式
    try:
        ipaddress.ip_address(tc.ipaddr)
    except ValueError:
        raise ValueError("Invalid IP address format")


if __name__ == "__main__":
    # 合规的参数
    valid_cases = [
        TC(rate="1kbps", delay=50, loss=10),

    ]

    for case in valid_cases:
        result, message = check_tc_params(case)
        print(f"合规参数 {case} 检查结果: {result}, 消息: {message}")


