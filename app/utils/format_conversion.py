import ast

from app.utils.logger import logger


def str_to_dict(input_str):
    try:
        return ast.literal_eval(input_str)
    except(SyntaxError, ValueError):
        logger.info(f"the input string {input_str} is invalid")
        return None