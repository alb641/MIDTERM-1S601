import pandas as pd
from pathlib import Path
from datetime import datetime

from app.calculator_memento import CalculatorMemento
from app.exceptions import HistoryError


class History:
    """Manage calculation history, undo, redo, and CSV persistence."""

    def __init__(self, max_history=100):
        self.max_history = max_history
        self.calculations = []
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

        previous_state = self.undo_stack.pop()
        self.calculations = previous_state.get_state()

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

        next_state = self.redo_stack.pop()
        self.calculations = next_state.get_state()

        if self.calculations:
            return self.calculations[-1]

        return None

    def clear(self):
        """Clear calculation history and undo/redo stacks."""
        self.calculations.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history(self):
        """Return a copy of calculation history."""
        return self.calculations.copy()

    def save_to_csv(self, file_path):
        """Save calculation history to a CSV file using pandas."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            records = []

            for calculation in self.calculations:
                record = calculation.copy()

                if "timestamp" not in record:
                    record["timestamp"] = datetime.now().isoformat()

                records.append(record)

            columns = [
                "operation",
                "a",
                "b",
                "result",
                "timestamp",
            ]

            dataframe = pd.DataFrame(records, columns=columns)

            dataframe.to_csv(
                path,
                index=False,
                encoding="utf-8",
            )

        except (OSError, ValueError, TypeError) as error:
            raise HistoryError(
                f"Could not save history: {error}"
            ) from error

    def load_from_csv(self, file_path):
        """Load calculation history from a CSV file using pandas."""
        try:
            path = Path(file_path)

            if not path.exists():
                raise HistoryError(
                    f"History file does not exist: {path}"
                )

            dataframe = pd.read_csv(path)

            required_columns = {
                "operation",
                "a",
                "b",
                "result",
                "timestamp",
            }

            if not required_columns.issubset(dataframe.columns):
                raise HistoryError(
                    "CSV file is missing required columns."
                )

            loaded_calculations = dataframe.to_dict(
                orient="records"
            )

            self.calculations = loaded_calculations[
                -self.max_history:
            ]

            self.undo_stack.clear()
            self.redo_stack.clear()

        except HistoryError:
            raise

        except (
            OSError,
            ValueError,
            pd.errors.ParserError,
            KeyError,
        ) as error:
            raise HistoryError(
                f"Could not load history: {error}"
            ) from error