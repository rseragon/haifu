from typing import Any
#from utils.Package import Package
from pathlib import Path

import apt
import apt_pkg

import os

import utils.Debug as Debug

CACHE_DIR = '/var/cache/apt/archives'
APT_CACHE = apt.Cache()

def search_pkg(pkg_name: str) -> list[str]:
    """
    Returns a list of packages info which match
    the given package name
    """
    global APT_CACHE

    pkg = APT_CACHE.get(pkg_name, None)

    if pkg is None:
        return []

    return [pkg.name]

#def get_info(pkg_name: str) -> list[Package]:
def get_info(pkg_name: str) -> list[Any]:
    """
    Similar to search_pkg but returns
    info about the package like MD5, depnds,
    arch etc.
    """
    from utils.Package import Package  # Fix circular deps
    global APT_CACHE

    cache_pkg = APT_CACHE.get(pkg_name, None)

    if cache_pkg is None:
        return []

    deps = []

    try:
        for dep in cache_pkg.candidate.dependencies:
            for base_dep in dep:
                deps.append(base_dep.name)
    except Exception:
        pass

    pkg = Package(cache_pkg.name, cache_pkg.candidate.md5, cache_pkg.candidate.sha256, deps, cache_pkg.versions[0].version, cache_pkg.architecture)
    return [pkg]

def check_installed(pkg_name: str) -> bool:
    """
    Checks if the given package is installed
    """
    global APT_CACHE
    pkg = APT_CACHE.get(pkg_name, None)

    if pkg is None:
        return False
    
    return pkg.is_installed


def get_file_location(pkg: Any) -> str:
    """
    Returns the location of the file in cache
    """
    global CACHE_DIR

    # TODO: This is a quick fix
    if isinstance(pkg, str):
        pkg_name = pkg
    else:
        pkg_name = pkg.name

    filename = pkg_file_name(pkg_name)

    cache_path = Path(CACHE_DIR)

    # Checks if file name is present in the cache
    file_path = [pth for pth in cache_path.glob("*.deb") if pth is not None and str(pth).rsplit('/')[-1] == filename]

    if len(file_path) == 0:
        return ""

    Debug.info(f"[USELESS] File found: {file_path[0]}")
    return str(file_path)[0]


def pkg_file_name(pkg: Any) -> str:
    """
    Gets the file name of the package
    """
    from utils.Package import Package

    # TODO: This is a quick fix
    if isinstance(pkg, str):
        pkg_name = pkg
    else:
        pkg_name = pkg.name

    global APT_CACHE

    pkg = APT_CACHE.get(pkg_name, None)

    if pkg is None:
        return ""

    return pkg.candidate.filename.rsplit('/')[-1] 
    # Retuns the package name for eg
    # zsh_5.8-3ubuntu1.1_amd64.deb

def in_cache(pkg_name: str) -> bool:
    """
    Checks if the given package is in cache
    TODO: This is inefficient
    """
    if get_file_location(pkg_name) != "":
        return True
    return False


def install_package(pkg_loc: str) -> bool:
    """
    Install the package from the locations
    """
    if pkg_loc == "":
        return False
    os.system(f'sudo apt-get install {pkg_loc}')
    return True
