from colorama import Fore, Style, init
init(autoreset=True)

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import CalculatorError


def show_help():
    """Display available calculator commands."""
    print("\nAvailable operations:")
    print("add         - Addition")
    print("subtract    - Subtraction")
    print("multiply    - Multiplication")
    print("divide      - Division")
    print("power       - Exponentiation")
    print("root        - Nth root")
    print("modulus     - Modulus")
    print("int_divide  - Integer division")
    print("percent     - Percentage")
    print("abs_diff    - Absolute difference")

    print("\nCommands:")
    print("history     - View calculation history")
    print("clear      - Clear history")
    print("undo        - Undo last calculation")
    print("redo        - Redo last calculation")
    print("save       - Save history to CSV")
    print("load       - Load history from CSV")
    print("help       - Show this help message")
    print("exit       - Exit calculator")


def main():
    """Run the calculator command-line interface."""
    try:
        config = CalculatorConfig()
        calculator = Calculator(config)

        history_file = (
            f"{config.history_dir}/calculator_history.csv"
        )

        print(Fore.CYAN + "Welcome to the Python Calculator!")
        print(Fore.YELLOW + "Type 'help' to view available commands.")

        while True:
            try:
                command = input("\nEnter command: ").strip().lower()

                if command == "exit":
                    print(Fore.CYAN + "Goodbye!")
                    break

                elif command == "help":
                    show_help()

                elif command == "history":
                    calculations = calculator.history.get_history()

                    if not calculations:
                        print("No calculation history.")
                    else:
                        for calculation in calculations:
                            print(calculation)

                elif command == "clear":
                    calculator.history.clear()
                    print("History cleared.")

                elif command == "undo":
                    result = calculator.history.undo()
                    print("Undo completed." if result else "Nothing to undo.")

                elif command == "redo":
                    result = calculator.history.redo()
                    print("Redo completed." if result else "Nothing to redo.")

                elif command == "save":
                    calculator.history.save_to_csv(history_file)
                    print("History saved.")

                elif command == "load":
                    calculator.history.load_from_csv(history_file)
                    print("History loaded.")

                elif command in (
                    "add",
                    "subtract",
                    "multiply",
                    "divide",
                    "power",
                    "root",
                    "modulus",
                    "int_divide",
                    "percent",
                    "abs_diff",
                ):
                    a = input("Enter first number: ")
                    b = input("Enter second number: ")

                    result = calculator.calculate(command, a, b)

                    print(Fore.GREEN + f"Result: {round(result, config.precision)}")

                else:
                    print("Invalid command. Type 'help' for options.")

            except CalculatorError as error:
                print(Fore.RED + f"Error: {error}")

            except (ValueError, TypeError) as error:
                print(Fore.RED + f"Invalid input: {error}")

    except CalculatorError as error:
        print(f"Calculator startup error: {error}")


if __name__ == "__main__":
    main()