import utils.Config as Config
import utils.Debug as Debug
from utils.Types import RequestType, ResultType
from utils.colors import print_yellow
from utils.helper_functions import send_data
from utils.Result import Result
from utils.helper_functions import dict_from_str
from utils.helper_functions import make_response_strjson

import pkg_resources


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


def print_version() -> None:
    version = pkg_resources.get_distribution('haifu').version
    print_yellow(f"Haifu (v{version}) - daemon (v{version})")

def print_usage() -> None:
    print_version()
