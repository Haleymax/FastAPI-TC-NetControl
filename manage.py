import argparse

from app.core.settings import get_config
from app.main import start
from app.utils.logger import logger


def parse_arguments():
    parser = argparse.ArgumentParser(description='Start webserver')
    parser.add_argument('--host', help="Bingding IP address", default="0.0.0.0", type=str)
    parser.add_argument('--port', help="Bingding port", default=8008, type=int)
    return parser.parse_args()

def main():
    args = parse_arguments()
    start_host, start_port = get_config()

    host =args.host or start_host
    port =args.port or start_port

    if not host or not port :
        logger.error("Host or port and interface must be provided via args or config file")
        return
    try:
        start(host=host, port=port)
        logger.info(f"Webserver started on {host}:{port}")
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()