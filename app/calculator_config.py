
import os
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


# Load environment variables from the project's .env file
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class CalculatorConfig:
    """Load and validate calculator configuration settings."""

    def __init__(self):
        self.log_dir = os.getenv("LOG_DIR", "logs")
        self.history_dir = os.getenv("HISTORY_DIR", "history")
        self.max_history = self._get_int("MAX_HISTORY", 100)
        self.autosave = self._get_bool("AUTOSAVE", True)
        self.precision = self._get_int("PRECISION", 2)
        self.max_input = self._get_float("MAX_INPUT", 1000000)
        self.default_encoding = os.getenv("DEFAULT_ENCODING", "utf-8")

        self.validate()

    def _get_int(self, name, default):
        """Read an integer setting."""
        try:
            return int(os.getenv(name, default))
        except ValueError as error:
            raise ConfigurationError(
                f"{name} must be an integer."
            ) from error

    def _get_float(self, name, default):
        """Read a numeric setting."""
        try:
            return float(os.getenv(name, default))
        except ValueError as error:
            raise ConfigurationError(
                f"{name} must be a number."
            ) from error

    def _get_bool(self, name, default):
        """Read a boolean setting."""
        value = os.getenv(name, str(default)).lower()

        if value in ("true", "1", "yes"):
            return True

        if value in ("false", "0", "no"):
            return False

        raise ConfigurationError(
            f"{name} must be true or false."
        )

    def validate(self):
        """Validate the configuration values."""
        if self.max_history <= 0:
            raise ConfigurationError(
                "MAX_HISTORY must be greater than zero."
            )

        if self.precision < 0:
            raise ConfigurationError(
                "PRECISION cannot be negative."
            )

        if self.max_input <= 0:
            raise ConfigurationError(
                "MAX_INPUT must be greater than zero."
            )

        if not self.default_encoding:
            raise ConfigurationError(
                "DEFAULT_ENCODING cannot be empty."
            )
