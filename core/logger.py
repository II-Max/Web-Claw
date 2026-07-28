import logging
import sys

from rich.logging import RichHandler

from core.config import LOG_DIR

# ===== LOG FILE =====

log_file = LOG_DIR / "datamine.log"

# ===== CONFIGURE ROOT LOGGER =====

logger = logging.getLogger("DataMine")
logger.setLevel(logging.DEBUG)

# ===== FILE HANDLER (detailed) =====

file_handler = logging.FileHandler(
    log_file,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
)

# ===== RICH CONSOLE HANDLER =====

console_handler = RichHandler(
    level=logging.INFO,
    show_time=False,
    show_path=False,
    markup=True,
    rich_tracebacks=True,
)

# ===== ADD HANDLERS =====

logger.addHandler(file_handler)
logger.addHandler(console_handler)