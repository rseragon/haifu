from typing import Any
from utils.Package import Package

def search_pkg(pkg_name: str) -> list[str]:
    """
    Returns a list of packages info which match
    the given package name
    """
    return []

def get_info(pkg_name: str) -> list[Package]:
    """
    Similar to search_pkg but returns
    info about the package like MD5, depnds,
    arch etc.
    """
    return []

def check_installed(pkg_name: str) -> bool:
    """
    Checks if the given package is installed
    """
    return False



def get_file_location() -> str:
    """
    Returns the location of the file in cache
    """
    return ""


def in_cache(pkg_name: str) -> bool:
    """
    Checks if the given package is in cache
    """
    pass


def install_package(pkg_loc: str) -> bool:
    """
    Install the package from the locations
    """
    pass
