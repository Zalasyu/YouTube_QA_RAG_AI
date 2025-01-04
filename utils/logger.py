import sys
from pathlib import Path

from loguru import logger

# Create logs directory if it doesn't exist
Path("logs").mkdir(parents=True, exist_ok=True)

# Remove existing handlers
logger.remove()


# Configure logger
logger.add(
    sink=sys.stdout,
    level="INFO",
    format="<level>{message}</level>",
    colorize=True,
    enqueue=True,
)


logger.add(
    sink="logs/log_{time}.log",
    rotation="100 MB",
    level="DEBUG",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    colorize=True,
    enqueue=True,
)