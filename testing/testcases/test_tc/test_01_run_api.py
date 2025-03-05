import allure
import pytest


from app.utils.logger import logger
from testing.core.sender import Sender
from testing.testcases.test_tc.conftest import post_data, URL


class TestRunApiTC:
    @allure.story("api test")
    @allure.description("weak net server api test")
    @allure.title("api 测试")
    @pytest.mark.api
    @pytest.mark.parametrize("rate, loss, ip, status",post_data)
    def test_01_run_tc(self, rate, loss, ip, status):
        logger.info("run api test")
        url = URL
        logger.info(f"rate: {rate}, loss: {loss} ipaddr: {ip}")
        post_data = {
            "rate": rate,
            "loss": loss,
            "ipaddr": ip,
        }
        sender = Sender()
        sender.post(url, post_data)
        allure.attach(sender.result, name="返回结果", attachment_type=allure.attachment_type.TEXT)
        assert sender.check_status(), f"与服务器连接失败"
        assert sender.check_parameters(rate=rate, loss=loss, ipaddress=ip), f"所设置的数据{rate}, {loss}, {ip}并没有设置成功"
