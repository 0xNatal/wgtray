"""Logging configuration for wgtray."""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

LOG_DIR = Path.home() / ".local" / "share" / "wgtray"
LOG_FILE = LOG_DIR / "wgtray.log"
MAX_LOG_SIZE = 1 * 1024 * 1024  # 1 MB
BACKUP_COUNT = 3

logger = logging.getLogger("wgtray")


def setup_logging(debug: bool = False):
    """Setup logging configuration.
    
    Args:
        debug: Enable debug level logging
    """
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    if debug:
        import sys
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_log_path() -> Path:
    """Return the log file path."""
    return LOG_FILE