import logging
from fastapi.logger import logger


def log(data, level=logging.INFO):
    logger.setLevel(level)
    logger.error(data)
