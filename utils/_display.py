import os
import math

colors = {
    "BLACK": 30,
    "RED": 31,
    "GREEN": 32,
    "YELLOW": 33,
    "BLUE": 34,
    "MAGENTA": 35,
    "CYAN": 36,
    "WHITE": 37
}

RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[4m"

def get_color(color: str = "WHITE", background: bool = False, bright: bool = False) -> str:
    n = colors[color.upper()]
    if background:
        n += 10
    if bright:
        n += 60
    
    return f"\33[0;{n}m"

def update_terminal(message: str = None) -> None:
    os.system("clear")
    
    if (message != None):
        print(message)

def loading_bar(text: str, numerator: int, denominator: int):
    ratio = round(numerator / denominator * 100) / 100
    ratio_bar = math.floor(ratio * 10)  

    update_terminal(
        f"{colors["MAGENTA"]}{text}{round(ratio * 100)}%\n -[ {"■" * ratio_bar}{"□" * (10 - ratio_bar)} ]-"
    )