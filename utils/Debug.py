import sys
from collections.abc import Callable
from utils.colors import print_red, print_yellow, print_cyan
from pprint import pprint
from utils.Config import get_logfile as LOG_FILE  # Fix cirular import
from typing import Any


DEBUG = True
INFO = True


def set_level(level: int) -> None:
    """
    Sets the level for the debugging
    0 -> Nothing
    1 -> info
    2 -> debug
    TODO: Standardise
    """
    pass


def error(error_code: int, msg: Any, atexit: Callable[[], None] = None) -> None:
    """
    prints message
    error_code:
        0 -> print message(Don't exit)
        1  -> print message and exit
       -1  -> call a function before quit
    """
    error_msg = "[ERROR] " + str(msg)
    LOG_FILE().writelines(error_msg + "\n")
    LOG_FILE().flush()
    print_red(error_msg)
    if error_code == 1:
        sys.exit()
    elif error_code == -1:
        if atexit is not None:
            atexit()
        sys.exit()


def debug(msg: Any) -> None:

    global DEBUG

    debug_msg = "[DEBUG] " + str(msg)
    LOG_FILE().writelines(debug_msg + "\n")
    LOG_FILE().flush()
    if DEBUG:
        print_yellow(debug_msg)


def info(msg: Any) -> None:
    global INFO

    info_msg = "[INFO] " + str(msg)
    LOG_FILE().writelines(info_msg + "\n")
    LOG_FILE().flush()
    if INFO:
        print_cyan(info_msg)


def wpprint(data: str) -> None:
    """
    A wrapper for pprint
    """
    global DEBUG
    if DEBUG:
        pprint(data)
