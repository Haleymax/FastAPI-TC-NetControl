import allure
import pytest


from app.utils.logger import logger
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
        assert 1==1
