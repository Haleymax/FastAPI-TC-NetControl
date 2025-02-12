import subprocess
from app.utils.logger import logger

class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def setup_tc(self, rate, delay, loss, ip_address):
        try:
            # 清除现有的 tc 配置
            self.clear_tc()

            # 设置延迟
            if delay:
                self.set_delay(delay)

            # 设置丢包率
            if loss:
                self.set_loss(loss)

            # 设置带宽限制
            if rate:
                self.set_rate(rate)

            # 设置 IP 地址的过滤器
            if ip_address:
                self.set_ip_filter(ip_address)

        except Exception as e:
            logger.error(f"Failed to setup traffic control: {e}")
            raise

    def clear_tc(self):
        try:
            subprocess.run(["sudo", "tc", "qdisc", "del", "dev", self.interface, "root"], check=True)
            logger.info(f"Cleared existing tc configuration on {self.interface}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clear tc configuration: {e}")
            raise

    def set_delay(self, delay):
        try:
            subprocess.run(["sudo", "tc", "qdisc", "add", "dev", self.interface, "root", "netem", "delay", f"{delay}ms"], check=True)
            logger.info(f"Set delay to {delay}ms on {self.interface}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set delay: {e}")
            raise

    def set_loss(self, loss):
        try:
            subprocess.run(["sudo", "tc", "qdisc", "change", "dev", self.interface, "root", "netem", "loss", f"{loss}%"], check=True)
            logger.info(f"Set loss to {loss}% on {self.interface}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set loss: {e}")
            raise

    def set_rate(self, rate):
        try:
            subprocess.run(["sudo", "tc", "qdisc", "add", "dev", self.interface, "root", "tbf", "rate", rate, "burst", "32kbit", "latency", "400ms"], check=True)
            logger.info(f"Set rate to {rate} on {self.interface}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set rate: {e}")
            raise

    def set_ip_filter(self, ip_address):
        try:
            # 添加过滤器以限制特定 IP 地址的流量
            subprocess.run(["sudo", "tc", "filter", "add", "dev", self.interface, "protocol", "ip", "parent", "1:", "prio", "1",
                            "u32", f"match ip dst {ip_address} flowid 1:1"], check=True)
            logger.info(f"Set IP filter for {ip_address} on {self.interface}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set IP filter: {e}")
            raise
