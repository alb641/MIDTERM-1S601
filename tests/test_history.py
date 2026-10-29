
import pandas as pd
import pytest

from app.history import History
from app.exceptions import HistoryError


@pytest.fixture
def sample_calculation():
    return {
        "operation": "add",
        "a": 2,
        "b": 3,
        "result": 5,
        "timestamp": "2026-10-28T10:00:00",
    }


def test_history_add(sample_calculation):
    history = History()
    history.add(sample_calculation)

    assert len(history.get_history()) == 1


def test_history_max_limit(sample_calculation):
    history = History(max_history=2)

    history.add(sample_calculation)
    history.add(sample_calculation)
    history.add(sample_calculation)

    assert len(history.get_history()) == 2


def test_undo_empty_history():
    history = History()

    assert history.undo() is None


def test_redo_empty_history():
    history = History()

    assert history.redo() is None


def test_undo_and_redo(sample_calculation):
    history = History()

    history.add(sample_calculation)
    history.undo()

    assert history.get_history() == []

    history.redo()

    assert len(history.get_history()) == 1


def test_undo_clears_redo_after_new_calculation(sample_calculation):
    history = History()

    history.add(sample_calculation)
    history.undo()
    history.add(sample_calculation)

    assert history.redo() is None


def test_clear_history(sample_calculation):
    history = History()

    history.add(sample_calculation)
    history.clear()

    assert history.get_history() == []
    assert history.undo() is None
    assert history.redo() is None


def test_save_history_to_csv(tmp_path, sample_calculation):
    history = History()
    history.add(sample_calculation)

    file_path = tmp_path / "history.csv"

    history.save_to_csv(file_path)

    dataframe = pd.read_csv(file_path)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["result"] == 5


def test_save_empty_history_to_csv(tmp_path):
    history = History()

    file_path = tmp_path / "history.csv"

    history.save_to_csv(file_path)

    dataframe = pd.read_csv(file_path)

    assert dataframe.empty


def test_load_history_from_csv(tmp_path, sample_calculation):
    history = History()

    file_path = tmp_path / "history.csv"

    pd.DataFrame([sample_calculation]).to_csv(
        file_path,
        index=False,
    )

    history.load_from_csv(file_path)

    assert len(history.get_history()) == 1
    assert history.get_history()[0]["result"] == 5


def test_load_missing_file(tmp_path):
    history = History()

    file_path = tmp_path / "missing.csv"

    with pytest.raises(HistoryError):
        history.load_from_csv(file_path)


def test_load_invalid_csv(tmp_path):
    history = History()

    file_path = tmp_path / "invalid.csv"

    pd.DataFrame({"wrong_column": [1]}).to_csv(
        file_path,
        index=False,
    )

    with pytest.raises(HistoryError):
        history.load_from_csv(file_path)


def test_load_respects_max_history(tmp_path, sample_calculation):
    history = History(max_history=2)

    file_path = tmp_path / "history.csv"

    pd.DataFrame(
        [sample_calculation] * 3
    ).to_csv(file_path, index=False)

    history.load_from_csv(file_path)

    assert len(history.get_history()) == 2


def test_get_history_returns_copy(sample_calculation):
    history = History()

    history.add(sample_calculation)

    returned_history = history.get_history()
    returned_history.clear()

    assert len(history.get_history()) == 1
