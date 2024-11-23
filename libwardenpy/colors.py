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


# funtion i wrote
### this append reset code and prepend the color code on to a string
def colored_string(text: str, color: str) -> str:
    colors = {
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "BLUE": "\033[34m",
    }
    RESET = "\033[0m"
    return f"{colors[color]}{text}{RESET}"
