# Python CLI Calculator

## Project Overview

This project supports multiple mathematical operations, calculation history, undo and redo functionality, automatic logging, and CSV history persistence.

The calculator uses design patterns to organize its functionality and improve maintainability. It also includes input validation, custom exceptions, automated tests, and continuous integration through GitHub Actions.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Exponentiation
- Nth root
- Modulus
- Integer division
- Percentage calculation
- Absolute difference
- Calculation history
- Undo and redo
- CSV history saving and loading using pandas
- Automatic logging of calculations
- Automatic saving of calculation history
- Configuration through environment variables
- Input validation and error handling
- NEW for extra credit: Color-coded terminal output using Colorama for results, errors, and calculator messages

## Design Patterns

### Factory Pattern

The Factory Pattern is used to create operation objects based on the operation selected by the user. The `OperationFactory` class determines which operation class to instantiate.

### Memento Pattern

The Memento Pattern is used to save and restore calculation history states. This allows users to undo and redo calculations.

### Observer Pattern

The Observer Pattern allows the calculator to notify registered observers when a calculation is completed.

Two observers are implemented:

- `LoggingObserver`: Logs calculation details.
- `AutoSaveObserver`: Automatically saves calculation history to a CSV file.

## Project Structure

```text
IS601-MIDTERM/
│
├── app/
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   └── operations.py
│
├── tests/
│   ├── __init__.py
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculator_config.py
│   ├── test_history.py
│   └── test_operations.py
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

### Requirements

- Python 3.12 or later
- pip

### Clone the repository

```bash
git clone https://github.com/alb641/MIDTERM-1S601.git
```

Navigate to the project directory:

```bash
cd MIDTERM-1S601
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Configuration

The calculator uses environment variables stored in a `.env` file.

Example configuration:

```text
LOG_DIR=logs
HISTORY_DIR=history
MAX_HISTORY=100
AUTOSAVE=true
PRECISION=2
MAX_INPUT=1000000
DEFAULT_ENCODING=utf-8
```

| Setting | Description |
|---|---|
| `LOG_DIR` | Directory used to store log files |
| `HISTORY_DIR` | Directory used to store calculation history |
| `MAX_HISTORY` | Maximum number of calculations stored |
| `AUTOSAVE` | Enables or disables automatic history saving |
| `PRECISION` | Number of decimal places displayed |
| `MAX_INPUT` | Maximum allowed numerical input |
| `DEFAULT_ENCODING` | Default file encoding |

## Running the Calculator

Start the calculator from the project directory:

```bash
python main.py
```

The calculator will display a welcome message and prompt you to enter a command.

### Example

```
Welcome to the Python Calculator!
Type 'help' to view available commands.

Enter command: add
Enter first number: 5
Enter second number: 3
Result: 8.0
```

## Available Commands

| Command | Description |
|---|---|
| `add` | Addition |
| `subtract` | Subtraction |
| `multiply` | Multiplication |
| `divide` | Division |
| `power` | Exponentiation |
| `root` | Nth root |
| `modulus` | Modulus |
| `int_divide` | Integer division |
| `percent` | Percentage calculation |
| `abs_diff` | Absolute difference |
| `history` | View calculation history |
| `clear` | Clear calculation history |
| `undo` | Undo the last calculation |
| `redo` | Redo the last undone calculation |
| `save` | Save history to CSV |
| `load` | Load history from CSV |
| `help` | Display available commands |
| `exit` | Exit the calculator |

## Testing

The project uses pytest to run automated tests and pytest-cov to measure test coverage.

Run all tests:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

The project currently achieves **91% total test coverage**, exceeding the assignment requirement of 90%.

## Continuous Integration

GitHub Actions is configured to automatically run the project's tests and check test coverage when changes are pushed to the repository or a pull request is opened.

The workflow verifies that:

- The application tests pass.
- Test coverage meets the minimum required threshold of 90%.

## Technologies Used

- Python
- pandas
- python-dotenv
- Colorama
- pytest
- pytest-cov
- GitHub Actions


## Repository

[GitHub Repository](https://github.com/alb641/MIDTERM-1S601)
