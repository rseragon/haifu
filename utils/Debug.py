import sys
from collections.abc import Callable
from utils.colors import print_red, print_yellow, print_cyan
from pprint import pprint

class Debug:

    DEBUG = True
    INFO = True

    @staticmethod
    def error(error_code: int, msg: str, atexit: Callable[[], None] = None) -> None:
        """
        prints message
        error_code:
            0 -> print message(Don't exit)
            1  -> print message and exit
           -1  -> call a function before quit
        """
        print_red("[ERROR] " + msg)
        if error_code == 1:
            sys.exit()
        elif error_code == -1:
            if atexit is not None:
                atexit()
            sys.exit()

    @staticmethod
    def debug(msg: str) -> None:
        if Debug.DEBUG:
            print_yellow("[DEBUG] " + msg)

    @staticmethod
    def info(msg: str) -> None:
        if Debug.INFO:
            print_cyan("[INFO] " + msg)

    @staticmethod
    def wpprint(data: str) -> None:
        """
        A wrapper for pprint
        """
        if Debug.DEBUG:
            pprint(data)
