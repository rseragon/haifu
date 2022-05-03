from glob import glob
import pyalpm
from pathlib import Path
import utils.Debug as Debug
# from utils.Package import Package  # Ciruclar import
from typing import Any
import os

PACMAN_DIR = '/var/lib/pacman'
CACHE_DIR  = '/var/cache/pacman/pkg'
PYALPM_DIR = "."  # TODO: Fix this
SYNC_DB_PATH = Path(PACMAN_DIR + '/sync')

if not Path(PACMAN_DIR).exists():
    Debug.error(1, "Pacman Directory not found, Cannot run package manager")

if not Path(CACHE_DIR).exists():
    Debug.error(1, "Cache Directory not found, Cannot run package manager")

if not SYNC_DB_PATH.exists():
    Debug.error(1, "Sync DB's not found, Cannot run package manager")


PACMAN_HANDLE = pyalpm.Handle(PYALPM_DIR, PACMAN_DIR)

# This is not actually useful
LOCALDB_HANDLE = PACMAN_HANDLE.get_localdb()

SYNC_DB_LIST = [ db.stem for db in SYNC_DB_PATH.iterdir() if db.suffix == '.db' ] # Get's all the files ending with .db in /var/lib/pacman/sync/
SYNCDBS = [PACMAN_HANDLE.register_syncdb(db, pyalpm.SIG_DATABASE_OPTIONAL) for db in SYNC_DB_LIST]



def search_pkg(pkg_name: str) -> list[str]:
    """
    Returns a list of packages info which match
    the given package name
    """
    pkg_list: list[str] = []

    for db in SYNCDBS:
        pkgs = db.search(pkg_name)
        for pkg in pkgs:
            pkg_list.append(pkg.name)

    return pkg_list

def get_info(pkg_name: str) -> list[Any]:
    """
    Similar to search_pkg but returns
    info about the package like MD5, depnds,
    arch etc.
    """
    from utils.Package import Package
    pkg_info: list[Package] = []

    for db in SYNCDBS:
        pkgs = db.search(pkg_name)
        for pkg in pkgs:
            pkg_info.append(Package(pkg.name, pkg.md5sum, pkg.sha256sum, pkg.depends,
                                    pkg.version, pkg.arch))

    return pkg_info

def check_installed(pkg_name: str) -> bool:
    """
    Checks if the given package is installed
    """
    return False


#def pkg_file_name(pkg: Package) -> str:
def pkg_file_name(pkg: Any) -> str:

    if not pkg:
        return ""

    name = pkg.name
    ver = pkg.ver
    arch = pkg.arch

    if name == "" or ver == "" or arch == "":
        return ""

    return f"{name}-{ver}-{arch}.pkg.tar.zst"


def get_file_location(package: Any) -> str:
    """
    Returns the location of the file in cache
    """
    from utils.Package import Package

    if not in_cache(package.name):
        return ""

    paths = glob(CACHE_DIR + "/" + pkg_file_name(package))

    if len(paths) < 1:
        Debug.debug(f"[Package] {package.name} is not found")
        return ""

    return paths[0]



def in_cache(pkg_name: str) -> bool:
    """
    Checks if the given package is in cache
    """
    found = False

    for package in LOCALDB_HANDLE.pkgcache:
        if pkg_name == package.name:
            found = True
            break

    return found



def install_package(pkg_loc: str) -> bool:
    """
    Installs the package from the location
    TODO: Make a better version
    """
    if not Path(pkg_loc).exists():
        Debug.error(0, f"File location invalid: {pkg_loc}")
    os.system(f"sudo pacman -U {pkg_loc}")
    Debug.info(f"[Pacakge] Installed {pkg_loc}") 
