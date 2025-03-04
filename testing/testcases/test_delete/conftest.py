import pytest

from testing.core.api_data import ApiData
from testing.core.sender import Sender
from testing.testcases.conftest import get_case_num
tc_api =  "http://127.0.0.1:8000/tc"
delete_api = "http://127.0.0.1:8000/tc/remove"

def generate_tests(case_num):
    api = ApiData(collection="tc")
    datas = api.create_game_list(case_num)
    return datas

post_data = generate_tests(get_case_num)
sender = Sender()

@pytest.fixture(scope="function", autouse=True)
def add_weak_environment(post_data):
    for data in post_data:
        post_dict = {
            "rate": data["rate"],
            "loss": data["loss"],
            "ipaddr": data["ipaddr"],
        }
        sender.post(tc_api, post_dict)
        sender.check_status()
        if sender.response.status_code != 200 or not sender.result['result']:
            post_data = [d for d in post_data if d.get('ipaddr') != data["ipaddr"]]
    return post_data