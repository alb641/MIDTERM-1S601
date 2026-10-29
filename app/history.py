import pandas as pd
from pathlib import Path
from datetime import datetime

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import HistoryError


class History:
    """Manage calculation history, including undo, redo, and CSV persistence."""

    def __init__(self, max_history=100):
        self.calculations = []
        self.max_history = max_history
        self.undo_stack = []
        self.redo_stack = []

    def add(self, calculation):
        """Add a calculation to history."""
        self.undo_stack.append(
            CalculatorMemento(self.calculations.copy())
        )

        self.calculations.append(calculation)

        if len(self.calculations) > self.max_history:
            self.calculations.pop(0)

        self.redo_stack.clear()

    def undo(self):
        """Undo the most recent calculation."""
        if not self.undo_stack:
            return None

        self.redo_stack.append(
            CalculatorMemento(self.calculations.copy())
        )

        memento = self.undo_stack.pop()
        self.calculations = memento.get_state()

        if self.calculations:
            return self.calculations[-1]

        return None

    def redo(self):
        """Redo the most recently undone calculation."""
        if not self.redo_stack:
            return None

        self.undo_stack.append(
            CalculatorMemento(self.calculations.copy())
        )

        memento = self.redo_stack.pop()
        self.calculations = memento.get_state()

        if self.calculations:
            return self.calculations[-1]

        return None

    def clear(self):
        """Clear calculation history."""
        self.calculations = []
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history(self):
        """Return a copy of calculation history."""
        return self.calculations.copy()

    def save_to_csv(self, filepath):
        """Save calculation history to a CSV file."""
        try:
            records = []

            for calculation in self.calculations:
                if isinstance(calculation, Calculation):
                    record = calculation.to_dict()
                else:
                    record = calculation.copy()

                if "timestamp" not in record or not record["timestamp"]:
                    record["timestamp"] = datetime.now().isoformat()

                records.append(record)

            dataframe = pd.DataFrame(
                records,
                columns=["operation", "a", "b", "result", "timestamp"]
            )

            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            dataframe.to_csv(filepath, index=False)

        except (OSError, ValueError, TypeError) as error:
            raise HistoryError(
                f"Could not save history: {error}"
            ) from error

    def load_from_csv(self, filepath):
        """Load calculation history from a CSV file."""
        filepath = Path(filepath)

        if not filepath.exists():
            raise HistoryError(
                f"History file not found: {filepath}"
                )

        try:
            dataframe = pd.read_csv(filepath)

            required_columns = [
                "operation",
                "a",
                "b",
                "result",
                "timestamp",
            ]

            if not all(
                column in dataframe.columns
                for column in required_columns
            ):
                raise HistoryError(
                    "CSV file is missing required columns."
                )

            loaded_calculations = []

            for _, row in dataframe.iterrows():
                calculation = Calculation(
                    operation=row["operation"],
                    a=row["a"],
                    b=row["b"],
                    result=row["result"],
                    timestamp=row["timestamp"],
                )

                loaded_calculations.append(calculation)

            self.calculations = loaded_calculations[-self.max_history:]

        except (OSError, ValueError, TypeError, KeyError) as error:
            raise HistoryError(
                f"Could not load history: {error}"
            ) from error