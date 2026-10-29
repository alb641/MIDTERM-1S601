
import math

from app.exceptions import OperationError


class Operation:
    """Base class for calculator operations."""

    def execute(self, a, b):
        """Perform the operation using two numerical inputs."""
        raise NotImplementedError(
            "Subclasses must implement execute()."
        )


class Add(Operation):
    """Add two numbers."""

    def execute(self, a, b):
        return a + b


class Subtract(Operation):
    """Subtract the second number from the first."""

    def execute(self, a, b):
        return a - b


class Multiply(Operation):
    """Multiply two numbers."""

    def execute(self, a, b):
        return a * b


class Divide(Operation):
    """Divide the first number by the second."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    """Raise the first number to the power of the second."""

    def execute(self, a, b):
        try:
            result = a ** b
        except (ValueError, OverflowError) as error:
            raise OperationError(
                "Invalid power operation."
            ) from error

        if isinstance(result, complex):
            raise OperationError(
                "Power operation produced a complex number."
            )

        if not math.isfinite(result):
            raise OperationError(
                "Power operation produced an invalid result."
            )

        return result


class NthRoot(Operation):
    """Calculate the nth root of the first number."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError(
                "The root degree cannot be zero."
            )

        if a < 0 and b % 2 == 0:
            raise OperationError(
                "Cannot calculate an even root of a negative number."
            )

        try:
            if a < 0:
                result = -((-a) ** (1 / b))
            else:
                result = a ** (1 / b)
        except (ValueError, OverflowError, ZeroDivisionError) as error:
            raise OperationError(
                "Invalid root operation."
            ) from error

        if not math.isfinite(result):
            raise OperationError(
                "Root operation produced an invalid result."
            )

        return result


class Modulus(Operation):
    """Calculate the remainder after division."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError(
                "Cannot calculate modulus with zero."
            )
        return a % b


class IntegerDivide(Operation):
    """Perform integer division."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError(
                "Cannot divide by zero."
            )
        return a // b


class Percentage(Operation):
    """Calculate the first number as a percentage of the second."""

    def execute(self, a, b):
        if b == 0:
            raise OperationError(
                "Cannot calculate percentage with zero."
            )
        return (a / b) * 100


class AbsoluteDifference(Operation):
    """Calculate the absolute difference between two numbers."""

    def execute(self, a, b):
        return abs(a - b)
