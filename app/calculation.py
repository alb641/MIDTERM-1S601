
from app.exceptions import OperationError
from app.operations import (
    Add,
    Subtract,
    Multiply,
    Divide,
    Power,
    NthRoot,
    Modulus,
    IntegerDivide,
    Percentage,
    AbsoluteDifference,
)


class OperationFactory:
    """Create operation objects based on operation names."""

    _operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": NthRoot,
        "modulus": Modulus,
        "int_divide": IntegerDivide,
        "percent": Percentage,
        "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create_operation(cls, operation_name):
        """Return an instance of the requested operation."""
        operation_class = cls._operations.get(
            operation_name.lower()
        )

        if operation_class is None:
            raise OperationError(
                f"Unknown operation: {operation_name}"
            )

        return operation_class()
