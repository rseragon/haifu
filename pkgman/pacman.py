import pyalpm
from pathlib import Path
import utils.Debug as Debug
from utils.Package import Package

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

def get_info(pkg_name: str) -> list[Package]:
    """
    Similar to search_pkg but returns
    info about the package like MD5, depnds,
    arch etc.
    """
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



def get_file_location(package: Package) -> str:
    """
    Returns the location of the file in cache
    """
    return ""


def in_cache(pkg_name: str) -> bool:
    """
    Checks if the given package is in cache
    """
    return True
