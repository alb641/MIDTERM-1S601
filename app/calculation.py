
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

class Calculation:
    """Represent a single calculation."""

    def __init__(self, operation, a, b, result, timestamp):
        self.operation = operation
        self.a = a
        self.b = b
        self.result = result
        self.timestamp = timestamp

    def to_dict(self):
        """Convert the calculation into a dictionary."""
        return {
            "operation": self.operation,
            "a": self.a,
            "b": self.b,
            "result": self.result,
            "timestamp": self.timestamp,
        }

    def __getitem__(self, key):
        return self.to_dict()[key]

    def copy(self):
        return self.to_dict().copy()

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
