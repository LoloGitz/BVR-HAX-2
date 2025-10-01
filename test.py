import termios
import sys
import tty
import os
import time

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"
RESET = "\033[0m"

from typing import Optional

print(len({"hi": "bye"}))

def get_key() -> Optional[str]:
    if os.name == "nt":  # If the operating system is Windows
        if msvcrt.kbhit():  # Checks if a keypress is available
            return msvcrt.getch().decode("utf-8")  # Reads the keypress
    else:  # If the operating system is macOS or Linux
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            char = sys.stdin.read(1)
        except KeyboardInterrupt:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
    
my_dict = {'apple': 5, 'banana': 2, 'orange': 8, 'grape': 3}

# Sort by value in ascending order
print(my_dict.items())
sorted_items_asc = dict(sorted(my_dict.items(), key=lambda item: item[1]))
print(f"Sorted by value (ascending): {sorted_items_asc}")


# while True:
#     key = get_key()
#     print(f"{key, key == ""}")
#     time.sleep(0.1)