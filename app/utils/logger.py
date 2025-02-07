import logging
import os
import time
from logging.handlers import RotatingFileHandler

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 定义日志文件路径
LOG_PATH = os.path.join(BASE_PATH, "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger:
    def __init__(self):
        # 修正日志文件名格式
        self.logname = os.path.join(LOG_PATH, f"logfile_{time.strftime('%Y%m%d')}.log")
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        self.formater = logging.Formatter(
            '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')

        # 创建 RotatingFileHandler 时指定编码为 utf-8
        self.filelogger = RotatingFileHandler(self.logname, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')
        # 创建 StreamHandler 时指定编码为 utf-8
        self.console = logging.StreamHandler()
        self.console.encoding = 'utf-8'

        self.console.setLevel(logging.DEBUG)
        self.filelogger.setLevel(logging.DEBUG)
        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)


logger = Logger().logger

if __name__ == '__main__':
    logger.info("---测试开始---")
    logger.debug("---测试结束---")