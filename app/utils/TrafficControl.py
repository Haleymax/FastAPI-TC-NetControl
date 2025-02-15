import subprocess
import logging

logger = logging.getLogger(__name__)

class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def clear_tc(self):
        try:
            subprocess.run(
                ["sudo", "tcdel", self.interface, "--all"],
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
        self.clear_tc()
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