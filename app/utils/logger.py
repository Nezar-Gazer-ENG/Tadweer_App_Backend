import logging
from logging.handlers import RotatingFileHandler
import os
from app.utils.config_loader import get_config

LOG_DIRECTORY = get_config("LOG_DIRECTORY", default="./logs")
LOG_LEVEL = get_config("LOG_LEVEL", default="INFO").upper()

# Ensure log directory exists
os.makedirs(LOG_DIRECTORY, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with rotating file handling.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Log file path
    log_file = os.path.join(LOG_DIRECTORY, f"{name}.log")

    # Rotating file handler: 5MB per file, keep last 5 logs
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Console handler for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Log format
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Avoid duplicate logs
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Standard loggers for different parts of the app
app_logger = get_logger("application")
db_logger = get_logger("database")
auth_logger = get_logger("authentication")
route_logger = get_logger("routing")

def log_info(message: str, logger=app_logger):
    logger.info(message)

def log_warning(message: str, logger=app_logger):
    logger.warning(message)

def log_error(message: str, logger=app_logger):
    logger.error(message)

def log_critical(message: str, logger=app_logger):
    logger.critical(message)

def log_debug(message: str, logger=app_logger):
    logger.debug(message)
