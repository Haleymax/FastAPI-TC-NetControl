import subprocess
from app.utils.logger import logger

class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def setup_tc(self, rate, delay, loss, ip_address):
        try:
            # 清除现有的 tc 配置
            self.clear_tc()

            self.set_network(rate=rate, loss=loss)

            

        except Exception as e:
            logger.error(f"Failed to setup traffic control: {e}")
            raise

    def clear_tc(self):
        try:
            # 检查当前的 qdisc 配置
            result = subprocess.run(
                ["sudo", "tc", "-s", "qdisc", "show", "dev", self.interface],
                capture_output=True,
                text=True
            )
            logger.info(f"execute result : {result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clear tc configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise
 
    def set_network(self, rate="512Kbit", loss = 0):
        result = []
        commands = [
            f"sudo tc qdisc add dev {self.interface} root handle 1: htb default 10",
            f"sudo tc class add dev {self.interface} parent 1: classid 1:1 htb rate {rate}",
            f"sudo tc class add dev {self.interface} parent 1:1 classid 1:10 htb rate {rate}"
            f"sudo tc class add dev {self.interface} parent 1:10 handle 10: netem loss {loss}%"
        ]
        for command in commands:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
                print(f"命令 {command} 执行成功，输出：{result.stdout}")
                result.append(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"命令 {command} 执行失败，错误信息：{e.stderr}")
                result.append(result.stderr)
        
        return result
    

