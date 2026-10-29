
class CalculatorError(Exception):
    """Base exception for calculator errors."""


class OperationError(CalculatorError):
    """Raised when a calculation operation fails."""


class ValidationError(CalculatorError):
    """Raised when input validation fails."""


class ConfigurationError(CalculatorError):
    """Raised when configuration settings are invalid."""


class HistoryError(CalculatorError):
    """Raised when calculator history cannot be saved or loaded."""
