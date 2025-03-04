import json
import re

import requests

from app.utils.logger import logger

def extract_ip_address(input_string):
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    result = re.search(pattern, input_string)
    if result:
        return result.group(0)
    return None


class Sender:
    def __init__(self):
        self.session = requests.Session()
        self.response = None
        self.result = None

    def get(self, url, params=None, headers=None):
        try:
            self.response = self.session.get(url, params=params, headers=headers)
            logger.info(f"successful send get request to : {url}")
        except Exception as e:
            logger.info(f"request failed : {e}")

    def post(self, url, params=None, data=None, headers=None):
        try:
            self.response = self.session.post(url, params=params, json=data, headers=headers)
            logger.info(f"successful send post request to : {url}")
        except Exception as e:
            logger.info(f"request failed : {e}")

    def check_status(self):
        """
        检查修改是否成功
        :return:
        """
        if self.response.status_code == 200:
            if not self.result:
                return False
            else:
                return True
        else:
            return False

    def check_parameters(self, rate:str, loss:int, ipaddress:str):
        """
        检查参数是否符合要求
        :param rate:
        :param loss:
        :param ipaddress:
        :return:
        """
        if not isinstance(rate, str):
            raise TypeError("rate must be a string")
        if not isinstance(loss, int):
            raise TypeError("loss must be an integer")
        if not isinstance(ipaddress, str):
            raise TypeError("ipaddress must be a string")

        data = self.response['message'][self.response['interface']]['outgoing']
        result = False
        for key, value in data.items():
            ipaddr = extract_ip_address(key)
            if ipaddr == ipaddress:
                if 'loss' in value and 'rate' in value:
                    value['loss'] = loss
                    value['rate'] = rate
                    result = True
        return result