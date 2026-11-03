"""
Structured logger with rotating file handler.
Import and use:  from app.utils.logger import logger
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
MAX_SIZE = 5 * 1024 * 1024   # 5 MB
BACKUP_COUNT = 3

os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE)

_fmt = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _build_logger(name: str = "app") -> logging.Logger:
    log = logging.getLogger(name)
    if log.handlers:
        return log

    log.setLevel(logging.DEBUG)

    fh = RotatingFileHandler(log_path, maxBytes=MAX_SIZE, backupCount=BACKUP_COUNT)
    fh.setFormatter(_fmt)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(_fmt)
    ch.setLevel(logging.INFO)

    log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = _build_logger("app")
