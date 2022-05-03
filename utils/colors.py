from colorama import Fore, Back, init

init(autoreset=True)

def print_red(msg: str) -> None:
    print(Fore.RED + msg)

def print_yellow(msg: str) -> None:
    print(Fore.YELLOW + msg)

def print_green(msg: str) -> None:
    print(Fore.GREEN + msg)

def print_cyan(msg: str, end: str = '\n') -> None:
    print(Fore.CYAN + msg, end = end)
