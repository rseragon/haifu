import sys
from collections.abc import Callable
from utils.colors import print_red, print_yellow, print_cyan
from pprint import pprint


class Debug:

    DEBUG = True
    INFO = True


    @staticmethod
    def set_level(level: int) -> None:
        """
        Sets the level for the debugging
        0 -> Nothing
        1 -> info
        2 -> debug
        TODO: Standardise
        """
        pass


    @staticmethod
    def error(error_code: int, msg: str, atexit: Callable[[], None] = None) -> None:
        """
        prints message
        error_code:
            0 -> print message(Don't exit)
            1  -> print message and exit
           -1  -> call a function before quit
        """
        import utils.Config as Conf  # To fix circular import
        error_msg = "[ERROR] " + msg
        Conf.get_logfile().writelines(error_msg + "\n")
        Conf.get_logfile().flush()
        print_red(error_msg)
        if error_code == 1:
            sys.exit()
        elif error_code == -1:
            if atexit is not None:
                atexit()
            sys.exit()

    @staticmethod
    def debug(msg: str) -> None:
        import utils.Config as Conf  # To fix circular import
        debug_msg = "[DEBUG] " + msg
        Conf.get_logfile().writelines(debug_msg + "\n")
        Conf.get_logfile().flush()
        if Debug.DEBUG:
            print_yellow(debug_msg)

    @staticmethod
    def info(msg: str) -> None:
        import utils.Config as Conf  # To fix circular import
        info_msg = "[INFO] " + msg
        Conf.get_logfile().writelines(info_msg + "\n")
        Conf.get_logfile().flush()
        if Debug.INFO:
            print_cyan(info_msg)

    @staticmethod
    def wpprint(data: str) -> None:
        """
        A wrapper for pprint
        """
        if Debug.DEBUG:
            pprint(data)
