from cli.tui import display_pkg_list
import utils.Config as Config
import utils.Debug as Debug
from utils.Types import RequestType, ResultType
from utils.colors import print_yellow
from utils.helper_functions import send_data
from utils.Result import Result
from utils.helper_functions import dict_from_str
from utils.helper_functions import make_response_strjson
from pkgman import PackageManager

import pkg_resources  # To get the packages version

from typing import Any

def check_alive() -> bool:
    """
    Checks if the daemon is alive or not
    """
    host, port = Config.get_hostport()

    if host == "" or port == -1:
        Debug.error(1, "Failed to connect to daemon port: Config not defined")

    ping = make_response_strjson(RequestType.PING, "PING!!!")

    resp = send_data(ping, host, port)

    if resp == "":
        Debug.debug("[CLI] Failed to connect to daemon port: No response")
        return False

    pong = Result(dict_from_str(resp))

    if pong is None:
        Debug.debug("[CLI] Failed to connect to daemon port: No response")
        return False


    if pong.getType() == ResultType.SUCCESSFUL:
        return True

    return False


def request_daemon(req_type: RequestType, data: Any, info: str = "") -> Any:
    """
    Requests the daemon and returns the response
    """
    dhost, dport = Config.get_hostport()
    req = make_response_strjson(req_type, data, info)

    res = send_data(req, dhost, dport, True)

    if res == "":
        Debug.debug("[CLI] No response from daemon")
        return ""
    
    result = Result(dict_from_str(res))

    return result.getData()


def print_version() -> None:
    # TODO: FIX THIs
    version = pkg_resources.get_distribution('haifu').version
    print_yellow(f"Haifu (v{version}) - daemon (v{version})")

def print_usage() -> None:
    print_version()


def install_pkg(pkg_name: str) -> bool:
    """
    This the the core which connects to daemon asks for package
    and install it if available
    """
    dhost, dport = Config.get_hostport()

    # Get the real package name
    pkgs = request_daemon(RequestType.SEARCH, pkg_name)
    pkg_idx = display_pkg_list(pkgs, True)

    if pkg_idx < 0: # -ve number for cancelling
        Debug.debug(f"[CLI] Package install cancelled by user {pkg_idx}")
        return False
    
    if pkg_idx > len(pkgs):
        Debug.debug(f"[CLI] {pkg_idx} Exceeding given list length")
        return False

    full_pkg_name = pkgs[pkg_idx]  # This gets the real package name, which is used for fetching

    file_loc = request_daemon(RequestType.FETCH_PKG, full_pkg_name)

    if file_loc == "":
        Debug.debug("[CLI] Failed to retrive package")
        return False

    Debug.info("[USELESS] File location: " + str(file_loc))

    PackageManager.install_package(file_loc)

    return True
