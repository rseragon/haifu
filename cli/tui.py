from typing import Any
import utils.Debug as Debug
from utils import colors
from utils.Package import Package


def display_table(data: list[Any], take_input: bool = False):
    """
    Takes in the data and display a cute table
    TODO: This is general form
    """
    if len(data) == 0:
        Debug.info("[CLI] Nothing to display")
        return

    return display_pkg_list(data, take_input)


def display_pkg_info(data: list[Any], take_input: bool = False) -> int:
    """
    Display Package info
    """
    if len(data) == 0:
        Debug.info("[CLI] No info to display")
        return -1

    colors.print_cyan("Data Length: " + str(len(data)))

    colors.print_green("\tPackage Name\tVersion\t\tArchitecture")
    for idx in range(len(data)):
        name = data[idx].get('name', '')
        if name == "":
            Debug.info(f"[CLI] Unkown info found: {data[idx]}")
            continue

        if len(name) > 14:
            name = name[:10]
            name += "..."
        else:
            req = 14 - len(name)
            name += " " * req

        version = data[idx].get('ver', '')
        arch = data[idx].get('arch', '')
        colors.print_yellow(f"{idx}\t{name} {version}\t\t{arch}")

    if take_input:
        return _take_input()
    return -1


def display_pkg_list(data: list[str], take_input: bool = False) -> int:
    """
    This is to display package list
    """

    # TODO: Check if __str__ or __repr__ exists
    """
    if "__repr__" not in data.__dir__ or "__str__" not in data.__dir__:
        Debug.error(0, "Cannot display data(no __repr__ or __str__)")
        return -1
    """
    if len(data) == 0:
        Debug.info("[CLI] Nothing to display")
        return -1

    colors.print_cyan("Data Length: " + str(len(data)))

    for idx in range(len(data)):
        colors.print_yellow(f"  {idx} {data[idx]}")

    if take_input:
        return _take_input()
    return -1


def _take_input():
    # Take the index input if requried
    while True:
        ret = -1
        try:
            colors.print_cyan("Enter index: ", end="")
            ret = input()
        except ValueError:
            Debug.error(0, f"Enter a number not {ret}")
            ret = -1
            continue
        return int(ret)
