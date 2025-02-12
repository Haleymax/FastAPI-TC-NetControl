import subprocess
import logging

logger = logging.getLogger(__name__)

class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def clear_tc(self):
        try:
            subprocess.run(
                ["tcdel", self.interface, "--all"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Cleared tc on {self.interface}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Clear tc failed: {e.stderr}"
            if "No such device" in error_msg:
                logger.error(f"Invalid interface: {self.interface}")
            elif "No qdisc" in error_msg:
                logger.warning("No existing configuration")
            else:
                logger.error(error_msg)
            raise  # 重新抛出异常让上层处理
        except FileNotFoundError:
            logger.error("tc command not found! Install iproute2")
            raise

    def clear_tc(self):
        try:
            # 清除现有的 tc 配置
            subprocess.run(
                ["tcdel", self.interface, "--all"],
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

    def set_network(self, rate="512Kbit", loss=0, ipaddr="127.0.0.1"):
        # 合并为一个命令同时设置 rate 和 loss
        command = [
            "tcset", self.interface,
            "--rate", rate,
            "--loss", str(loss),
            "--network", ipaddr
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Network configured: {command}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd}\nError: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

        # 查看配置
        try:
            result = subprocess.run(
                ["tcshow", self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to verify config: {e.stderr}")
            return ""   