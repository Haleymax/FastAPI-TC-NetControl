from testing.core.api_data import ApiData

URL = "http://127.0.0.1:8000/tc"


def generate_tests():
    api = ApiData()
    datas = api.create_game_list("all")
    return datas

post_data = generate_tests()