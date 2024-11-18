import sys


# stole it from https://medium.com/ai-does-it-better/print-colored-text-in-python-enhance-terminal-output-b90aede058c8
def print_colored(text, color, end="\n"):
    colors = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
    }
    reset = "\x1b[0m"
    sys.stdout.write(colors.get(color, "") + text + reset + end)


def colored_string(text: str, color: str) -> str:
    colors = {
        "BLACK": "\033[30m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",  # orange on some systems,
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "LIGHT_GRAY": "\033[37m",
        "DARK_GRAY": "\033[90m",
        "BRIGHT_RED": "\033[91m",
        "BRIGHT_GREEN": "\033[92m",
        "BRIGHT_YELLOW": "\033[93m",
        "BRIGHT_BLUE": "\033[94m",
        "BRIGHT_MAGENTA": "\033[95m",
        "BRIGHT_CYAN": "\033[96m",
        "WHITE": "\033[97m",
    }
    RESET = "\033[0m"
    return f"{colors[color]}{text}{RESET}"
