import re

from app.model.models import TC


def check_tc_params(tc: TC):
    # 定义正则表达式来匹配包含常见单位的速率格式
    rate_pattern = re.compile(r'^\d+([bkmgt]bps)?$', re.IGNORECASE)
    if not rate_pattern.match(tc.rate):
        return False, "rate 必须是一个非负数字，可后跟 'bps'、'kbps'、'Mbps'、'Gbps' 或 'Tbps' 单位"

    # 检查 delay 是否为非负整数
    if tc.delay < 0:
        return False, "delay 必须是一个非负整数"

    # 检查 loss 是否在 0 到 100 之间
    if tc.loss < 0 or tc.loss > 100:
        return False, "loss 必须是一个介于 0 到 100 之间的整数"

    return True, "参数合规"

# 示例使用
if __name__ == "__main__":
    # 合规的参数
    valid_cases = [
        TC(rate="1kbps", delay=50, loss=10),

    ]

    for case in valid_cases:
        result, message = check_tc_params(case)
        print(f"合规参数 {case} 检查结果: {result}, 消息: {message}")


