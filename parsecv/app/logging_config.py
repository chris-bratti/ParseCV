import logging
import sys
from colorama import Fore, Style, init

init(autoreset=True)

LOG_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelno, Fore.WHITE)
        levelname = f"{log_color}[{record.levelname}]{Style.RESET_ALL}"
        formatted_message = super().format(record).replace(f"[{record.levelname}]", levelname)
        return formatted_message


logger  = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = ColoredFormatter("[%(levelname)s]: %(asctime)s - %(message)s")
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(console_handler)