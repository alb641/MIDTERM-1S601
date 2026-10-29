from datetime import datetime

from app.calculation import OperationFactory
from app.history import History
from app.input_validators import validate_number, validate_operation
from app.logger import Logger


class LoggingObserver:
    """Log each successful calculation."""

    def __init__(self, log_dir="logs"):
        self.logger = Logger(log_dir)

    def update(self, calculation):
        """Log calculation details."""
        message = (
            f"{calculation['operation']} "
            f"({calculation['a']}, {calculation['b']}) "
            f"= {calculation['result']}"
        )

        self.logger.info(message)


class AutoSaveObserver:
    """Automatically save calculation history to CSV."""

    def __init__(self, history, history_file):
        self.history = history
        self.history_file = history_file

    def update(self, calculation):
        """Save history when a calculation is added."""
        self.history.save_to_csv(self.history_file)


class Calculator:
    """Main calculator class."""

    def __init__(self, config=None):
        self.config = config

        self.history = History(
            max_history=config.max_history if config else 100
        )

        self.factory = OperationFactory()
        self.observers = []

        log_dir = config.log_dir if config else "logs"
        self.attach(LoggingObserver(log_dir))

        if config and config.autosave:
            history_file = (
                f"{config.history_dir}/calculator_history.csv"
            )

            self.attach(
                AutoSaveObserver(self.history, history_file)
            )

    def attach(self, observer):
        """Register an observer."""
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        """Remove an observer."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, calculation):
        """Notify observers of a new calculation."""
        for observer in self.observers:
            observer.update(calculation)

    def calculate(self, operation_name, a, b):
        """Perform a calculation and save it to history."""

        operation_name = validate_operation(operation_name)

        a = validate_number(
            a,
            self.config.max_input if self.config else 1000000
        )

        b = validate_number(
            b,
            self.config.max_input if self.config else 1000000
        )

        operation = self.factory.create_operation(operation_name)
        result = operation.execute(a, b)

        calculation = {
            "operation": operation_name,
            "a": a,
            "b": b,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }

        self.history.add(calculation)

        self.notify(calculation)

        return result