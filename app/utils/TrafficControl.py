import subprocess
import logging

logger = logging.getLogger(__name__)

class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def setup_tc(self, rate, loss):
        try:
            # 清除现有的 tc 配置
            self.clear_tc()

            # 设置新的 tc 配置
            self.set_network(rate=rate, loss=loss)

        except Exception as e:
            logger.error(f"Failed to setup traffic control: {e}")
            raise

    def clear_tc(self):
        try:
            # 清除现有的 tc 配置
            subprocess.run(
                ["sudo", "tc", "qdisc", "del", "dev", self.interface, "root"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Cleared tc configuration on interface {self.interface}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clear tc configuration: {e}")
            # raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            # raise

    def set_network(self, rate="512Kbit", loss=0):
        results = []
        commands = [
            f"sudo tc qdisc add dev {self.interface} root handle 1: htb default 10",
            f"sudo tc class add dev {self.interface} parent 1: classid 1:1 htb rate {rate}",
            f"sudo tc class add dev {self.interface} parent 1:1 classid 1:10 htb rate {rate}",
            f"sudo tc qdisc add dev {self.interface} parent 1:10 handle 10: netem loss {loss}%"
        ]
        for command in commands:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
                results.append(result.stdout)
                logger.info(f"Command executed successfully: {command}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Command failed: {command}, Error: {e.stderr}")
                raise
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                raise

        return results