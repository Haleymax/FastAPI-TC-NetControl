import pytest
import requests

from app.utils.logger import logger
from testing.testcases.test_tc.conftest import post_data, URL


class TestRunApiTC:
    @pytest.mark.parametrize(post_data)
    def test_01_run_tc(self):
        logger.info("run api test")
        url = URL
        data = {

        }
        response = requests.post(url, json=data)
        assert response.status_code == 200
