import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging():
    # 로거 설정
    logger = logging.getLogger()
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)

    # SQL 로깅 설정
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
