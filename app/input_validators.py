
from app.exceptions import ValidationError


def validate_number(value, max_input=1000000):
    """Validate that an input is a number within the allowed range."""
    try:
        number = float(value)
    except (ValueError, TypeError) as error:
        raise ValidationError(
            "Input must be a valid number."
        ) from error

    if number != number or number in (float("inf"), float("-inf")):
        raise ValidationError(
            "Input must be a finite number."
        )

    if abs(number) > max_input:
        raise ValidationError(
            f"Input cannot exceed {max_input}."
        )

    return number


def validate_operation(operation):
    """Validate that an operation name is not empty."""
    if not isinstance(operation, str) or not operation.strip():
        raise ValidationError(
            "Operation name cannot be empty."
        )

    return operation.strip().lower()
