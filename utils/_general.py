import termios
import sys
import tty

from typing import Callable
from typing import Optional

def sort_dict(
    d: dict = {},
    sort: Callable[..., int] = lambda item: item[1],
    reverse_b: bool = False
) -> dict:
    return dict(sorted(d.items(), key=sort, reverse=reverse_b))

def get_index(l: list | dict, v: any) -> Optional[int]:
    try:
        return l.index(v)
    except ValueError:
        return None

def get_key() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char