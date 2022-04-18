from typing import Optional
from utils.Peer import Peer
from db.DBInterface import DatabaseInterface
import socket
import platform
import utils.Debug as Debug
from utils.Request import Request
from utils.Result import Result
from utils.Types import RequestType, ResultType
from utils.helper_functions import async_read_data, make_response_strjson, async_write_data, dict_from_str
import json


def add_to_db(peer: Peer):
    """
    Queries the peer for more info and
    Adds the peer to the database
    """
    db = DatabaseInterface()
    Debug.info(f"[USELESS] peer {peer}")

    db.insert_peer(peer)


def get_peer_list():
    """
    Queries the db and get's all the peer list
    TODO
    """
    db = DatabaseInterface()
    peers: list[Peer] = []
    for peer in db.get_peers():
        peers.append(peer)

    return peers

def current_daemon_info() -> dict:
    name = socket.gethostname() 
    arch = platform.architecture()[0]
    os_id = ""
    distro = platform.freedesktop_os_release().get("NAME", "")

    platform_id = platform.freedesktop_os_release().get("ID", "").lower()
    platform_id_like = platform.freedesktop_os_release().get("ID_LIKE", "").lower()

    if platform_id_like == "":
        os_id = platform_id
    else:
        os_id = platform_id_like

    return {"name": name,
            "arch": arch,
            "os": os_id,
            "distro": distro}


async def get_peer_with_package(pkg_name: str, peers: list[Peer]) -> Optional[Peer]:
    """
    Returns a list of peers which have the package
    """
    alive_peers = [peer for peer in peers if await peer.async_is_alive()]

    Debug.info(f"[USELESS] alive_peers: {alive_peers}")

    if len(alive_peers) < 1:
        Debug.debug("[Peer] No peers alive")
        return None

    peers_with_pkg  = [peer for peer in alive_peers if await has_package(pkg_name, peer)]

    Debug.info(f"[USELESS] peers_with_pkg: {peers_with_pkg}")

    if len(peers_with_pkg) < 0:
        Debug.debug("[Peer] No peer with package")
        return None


async def has_package(pkg_name: str, peer: Peer) -> bool:
    """
    Asks the peer if he has the package
    """

    reader, writer = await peer.connect()

    req = make_response_strjson(RequestType.SEND_PKG, {"Package Name": pkg_name})
    await async_write_data(req, writer)

    res = Result(dict_from_str(await async_read_data(reader)))

    if res.getType() == ResultType.FAILED:
        return False

    data: list[dict] = res.getData()

    if len(data) < 1:  # No packages found in peer
        return False

    Debug.info(f"[USELESS] data: {data[0]}")
