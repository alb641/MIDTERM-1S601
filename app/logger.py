
import logging
from pathlib import Path


class Logger:
    """Configure and manage calculator logging."""

    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        log_file = self.log_dir / "calculator.log"

        self.logger = logging.getLogger("CalculatorLogger")
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate log messages.
        if not self.logger.handlers:
            file_handler = logging.FileHandler(
                log_file,
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message):
        """Log an informational message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
