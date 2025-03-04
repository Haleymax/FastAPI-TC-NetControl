from testing.core.api_data import ApiData
from testing.testcases.conftest import get_case_num

URL = "http://127.0.0.1:8000/tc"


def generate_tests(case_num):
    api = ApiData(collection="tc")
    datas = api.create_game_list(case_num)
    return datas

post_data = generate_tests(get_case_num)