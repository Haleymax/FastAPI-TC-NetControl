import subprocess

from app.utils.format_conversion import str_to_dict
from app.utils.logger import logger


class TrafficControl:
    def __init__(self, interface):
        self.interface = interface

    def clear_tc(self, device):
        try:
            if device is None:
                command = ["tcdel", self.interface, "--all"]
                process_result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )
                output = process_result.stdout
                logger.info(f"Cleared tc configuration on interface {self.interface}, result is {output}")
            else:
                command = ["tcdel", self.interface, "--dst-network", device]
                process_result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )
                output = process_result.stdout
                logger.info(f"Cleared tc configuration on device {device}, result is {output}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clear tc configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise
        finally:
            return self.show_tc_config()

    def set_network(self, rate="512Kbit", loss=0, ipaddr="127.0.0.1"):
        output = None
        try:
            command = [
                "tcset", self.interface,
                "--rate", rate,
                "--loss", str(loss),
                "--network", ipaddr,
                "--add"
            ]
            process_result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Network configured: {command}")
            logger.info(process_result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {e.cmd}\nError: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
        finally:
            return self.show_tc_config()

    def show_tc_config(self):
        try:
            command = ["tcshow", self.interface]
            process_result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            output = process_result.stdout
            logger.info(f"TC configuration on interface {self.interface} result is {output}")
            return str_to_dict(output)
        except subprocess.CalledProcessError as e:
            logger.info(f"faild show tc config on interface {self.interface} as {e}")
            return str_to_dict(e.output)