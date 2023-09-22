import pyalpm

import os
import sys
import glob # for searching file
from pathlib import Path # For getting sync db packages

pacman_dir = '/var/lib/pacman'
cache_dir = '/var/cache/pacman/pkg'

if not os.access(pacman_dir, os.R_OK):
    sys.exit("[ERROR] Don't have access to: " + pacman_dir)

HANDLE = pyalpm.Handle(".", pacman_dir)

LOCALDB_HANDLE = HANDLE.get_localdb()
#SYNCDB_HANDLE  = HANDLE.get_syncdbs("core", pyalpm.SIG_DATABASE_OPTIONAL)


# TODO: Check for all db's
SYNC_DB_PATH = pacman_dir + "/sync"
SYNC_PATH = Path(SYNC_DB_PATH)
SYNC_DB_LIST = [ db.stem for db in SYNC_PATH.iterdir() if db.suffix == '.db' ] # Get's all the files ending with .db in /var/lib/pacman/sync/

# Core syncdb Handle
#SYNCDB_HANDLE  = HANDLE.register_syncdb("core", pyalpm.SIG_DATABASE_OPTIONAL)
SYNCDBS_HANDLE = [HANDLE.register_syncdb(db, pyalpm.SIG_DATABASE_OPTIONAL) for db in SYNC_DB_LIST]
SYNCDB_HANDLE  = [db for db in SYNCDBS_HANDLE if db.name == 'core'][0]



# TODO: Delete this
def pkg_details(pkg: pyalpm.Package) -> None:
    if not pkg:
        return

    name = pkg.name
    md5  = pkg.md5sum
    sha  = pkg.sha256sum
    deps = pkg.depends
    ver  = pkg.version
    arch = pkg.arch


    if not pkg.md5sum:
        core_pkg = SYNCDB_HANDLE.get_pkg(pkg.name)
        if not core_pkg:
            sys.exit("Not found in core pkg")
        md5 = core_pkg.md5sum
        sha = core_pkg.sha256sum

    #file_name = f"{name}-{ver}-{arch}.pkg.tar.zst"
    file_name = get_file_name(pkg)
    print(f"Package Name: {name}\n\
            File   : {file_name}\n\
            Arch   : {arch}\n\
            Version: {ver}\n\
            MD5Hash: {md5}\n\
            SHA256 : {sha}\n\
            Depends: {str(deps)}")

    for package in SYNCDB_HANDLE.pkgcache:
        if pkg.name == package:
            print("{pkg.name} is present in cache")


def pkg_details_dict(pkg: pyalpm.Package) -> dict:
    """
    An internal function which takes in pyalpm object and returns
    dict information about that package
    """
    if not pkg:
        return {}

    name = pkg.name
    md5  = pkg.md5sum
    sha  = pkg.sha256sum
    deps = pkg.depends
    ver  = pkg.version
    arch = pkg.arch
    file_name = get_file_name(pkg)

    pkg_dict = {"Name": name,
                "File": file_name,
                "Arch": arch,
                "Version": ver,
                "MD5": md5,
                "SHA256": sha,
                "Depends": deps}

    return pkg_dict

def get_file_name(pkg: pyalpm.Package) -> str:
    """
    Gets the file name for the package so send/search 
    in local cache
    name"""
    if not pkg:
        return ""

    name = pkg.name
    ver  = pkg.version
    arch = pkg.arch
    
    if name == "" or ver == "" or arch == "":
        return ""

    return f"{name}-{ver}-{arch}.pkg.tar.zst"

def search_pkg(pkg_name: str) -> list[pyalpm.Package]:
    '''
    Searches for packages in the sync db handles
    '''
    pkg_list = []

    for db in SYNCDBS_HANDLE:
        pkgs = db.search(pkg_name)
        pkg_list.extend(pkgs)

    return pkg_list

def get_pkg(pkg_name: str) -> pyalpm.Package:
    '''
    Gets package from the sync db(cuz local db doesn't give MD5)
    returns None or a single package, similar to search_pkg but
    only returns first pacakge
    '''
    pkg: pyalpm.Package = LOCALDB_HANDLE.get_pkg(pkg_name)

    if pkg is None:
        print(f"{pkg_name} not found in local db")
        pkg = SYNCDB_HANDLE.search(pkg_name)

    '''
    if pkg is None:
        sys.exit(f"{pkg_name} is not found in sync db")
    '''

    return pkg


def check_installed(pkg_name: str) -> bool:
    '''
    Checks if a package is satisfied or not
    '''
    return pyalpm.find_satisfier(LOCALDB_HANDLE.pkgcache, pkg_name) != None


def check_depends(pkg_name: str) -> tuple[list[str], bool]:
    '''
    Returns list of dependencies to install, and bool to
    check if pkg_name was found
    '''
    pkg = SYNCDB_HANDLE.search(pkg_name)

    # TODO: search returns too many pacakges, need to
    # search for the apporiate one
    
    if len(pkg) == 0:
        return [], False

    missing = [package for package in pkg[0].depends if not check_installed(package)]

    return missing, True


#def cache_search(pkg_name: str) -> tuple[bool, str]:
# TODO: check them manually than using localdb
def cache_search(pkg_name: str):
    """
    Checks if the file exists in cache
    """
    found = False
    for package in LOCALDB_HANDLE.pkgcache:
        if pkg_name == package.name:
            found = True
            break

    if not found:
        return False
    return True


def get_file(pkg_name: str, file_name: str) -> str:
    '''
    Returns file path
    '''
    if not cache_search(pkg_name):
        print("[Debug] not found in localdb")
        return ""

    paths = glob.glob(cache_dir + "/" + file_name)

    if len(paths) == 0:
        print("[Debug] path not found")
        return ""

    return paths[0]


def pacman_search(pkg_name: str):
    '''
    A debug function to print the packages found
    '''
    pkg = search_pkg(pkg_name)
    pkg_details(pkg)
