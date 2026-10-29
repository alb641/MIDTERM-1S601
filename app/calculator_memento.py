
class CalculatorMemento:
    """Store and restore a snapshot of calculator history."""

    def __init__(self, state):
        self._state = state.copy()

    def get_state(self):
        """Return the saved calculator state."""
        return self._state.copy()