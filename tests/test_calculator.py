import pytest

from app.calculator import Calculator
from app.calculation import OperationFactory
from app.exceptions import OperationError, ValidationError
from app.history import History
from app.input_validators import validate_number, validate_operation


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 5, 3, 8),
        ("subtract", 5, 3, 2),
        ("multiply", 5, 3, 15),
        ("divide", 10, 2, 5),
        ("power", 2, 3, 8),
        ("root", 27, 3, 3),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 5, 10, 5),
    ],
)
def test_operations(operation, a, b, expected):
    calculator = Calculator()
    assert calculator.calculate(operation, a, b) == pytest.approx(expected)


def test_divide_by_zero():
    calculator = Calculator()
    with pytest.raises(OperationError):
        calculator.calculate("divide", 10, 0)


def test_invalid_operation():
    factory = OperationFactory()
    with pytest.raises(OperationError):
        factory.create_operation("invalid")


def test_invalid_number():
    with pytest.raises(ValidationError):
        validate_number("hello")


def test_invalid_operation_name():
    with pytest.raises(ValidationError):
        validate_operation("")


def test_calculation_added_to_history():
    calculator = Calculator()
    calculator.calculate("add", 2, 3)

    history = calculator.history.get_history()

    assert len(history) == 1
    assert history[0]["result"] == 5


def test_history_undo_redo():
    history = History()

    history.add({"operation": "add", "a": 2, "b": 3, "result": 5})
    history.undo()

    assert history.get_history() == []

    history.redo()

    assert len(history.get_history()) == 1


def test_history_clear():
    history = History()
    history.add({"operation": "add", "a": 2, "b": 3, "result": 5})

    history.clear()

    assert history.get_history() == []


from app.calculator import LoggingObserver, AutoSaveObserver
from app.logger import Logger


def test_calculator_with_no_config():
    calculator = Calculator()

    assert calculator.config is None
    assert calculator.history.max_history == 100


def test_calculator_observer_attach_detach():
    calculator = Calculator()
    observer = LoggingObserver()

    calculator.attach(observer)
    assert observer in calculator.observers

    calculator.detach(observer)
    assert observer not in calculator.observers


def test_calculator_detach_missing_observer():
    calculator = Calculator()

    observer = LoggingObserver()

    calculator.detach(observer)

    assert observer not in calculator.observers


def test_logging_observer_update(tmp_path):
    observer = LoggingObserver(str(tmp_path))

    calculation = {
        "operation": "add",
        "a": 2,
        "b": 3,
        "result": 5,
    }

    observer.update(calculation)


def test_autosave_observer_update(tmp_path):
    history = History()

    calculation = {
        "operation": "add",
        "a": 2,
        "b": 3,
        "result": 5,
    }

    history.add(calculation)

    file_path = tmp_path / "history.csv"

    observer = AutoSaveObserver(history, file_path)
    observer.update(calculation)

    assert file_path.exists()


def test_calculator_observer_notifies(tmp_path):
    calculator = Calculator()

    observer = AutoSaveObserver(
        calculator.history,
        tmp_path / "history.csv",
    )

    calculator.attach(observer)

    calculator.calculate("add", 2, 3)

    assert (tmp_path / "history.csv").exists()
