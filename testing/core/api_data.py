
from app.utils.logger import logger
from testing.core.mongo import mongo


def convert_game_info_json_to_list(datas):
    """
    将json格式转换为列表,如果数据为空抛出异常，中止程序
    """
    if not datas:
        raise ValueError("the data read is empty")
    game_info_list = []
    for data in datas:
        try:
            one_game_record = [data['rate'], data['loss'], data['ipaddress'], data['result']]
            game_info_list.append(one_game_record)
        except Exception as e:
            logger.warning(f"game data is incorrect: {e}")
    return game_info_list

class ApiData:
    def __init__(self, collection = "tc"):
        self.data = None
        self.collection = collection

    def create_game_list(self, case_num):
        pipe_sample = {}
        pipe_line = []
        session = mongo.get()
        if case_num == "all":
            case_num = session.find_count(self.collection, query={})
        pipe_sample["$sample"] = {"size": case_num}
        pipe_line.append(pipe_sample)
        result = list(session.pipe(self.collection, pipe_line))
        result = convert_game_info_json_to_list(result)
        return result




