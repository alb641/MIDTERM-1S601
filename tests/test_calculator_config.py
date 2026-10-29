
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_config_loads_defaults(monkeypatch):
    monkeypatch.delenv("MAX_HISTORY", raising=False)
    monkeypatch.delenv("AUTOSAVE", raising=False)
    monkeypatch.delenv("PRECISION", raising=False)
    monkeypatch.delenv("MAX_INPUT", raising=False)

    config = CalculatorConfig()

    assert config.max_history == 100
    assert config.autosave is True
    assert config.precision == 2
    assert config.max_input == 1000000


def test_config_loads_environment_values(monkeypatch):
    monkeypatch.setenv("MAX_HISTORY", "50")
    monkeypatch.setenv("AUTOSAVE", "false")
    monkeypatch.setenv("PRECISION", "4")
    monkeypatch.setenv("MAX_INPUT", "5000")

    config = CalculatorConfig()

    assert config.max_history == 50
    assert config.autosave is False
    assert config.precision == 4
    assert config.max_input == 5000


@pytest.mark.parametrize("value", ["invalid", "abc"])
def test_invalid_max_history(monkeypatch, value):
    monkeypatch.setenv("MAX_HISTORY", value)

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


@pytest.mark.parametrize("value", ["invalid", "abc"])
def test_invalid_precision(monkeypatch, value):
    monkeypatch.setenv("PRECISION", value)

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


@pytest.mark.parametrize("value", ["invalid", "abc"])
def test_invalid_max_input(monkeypatch, value):
    monkeypatch.setenv("MAX_INPUT", value)

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


@pytest.mark.parametrize("value", ["invalid", "maybe"])
def test_invalid_autosave(monkeypatch, value):
    monkeypatch.setenv("AUTOSAVE", value)

    with pytest.raises(ConfigurationError):
        CalculatorConfig()


@pytest.mark.parametrize(
    "variable,value",
    [
        ("MAX_HISTORY", "0"),
        ("PRECISION", "-1"),
        ("MAX_INPUT", "0"),
        ("DEFAULT_ENCODING", ""),
    ],
)
def test_invalid_config_values(monkeypatch, variable, value):
    monkeypatch.setenv(variable, value)

    with pytest.raises(ConfigurationError):
        CalculatorConfig()
