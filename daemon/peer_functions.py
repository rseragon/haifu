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
    # Get all the alive peers, this also makes readers and writers with them
    alive_peers = [peer for peer in peers if await peer.async_is_alive()]

    Debug.info(f"[USELESS] alive_peers: {alive_peers}")

    if len(alive_peers) < 1:
        Debug.debug("[Peer] No peers alive")
        return None

    # Get all the peers with the package
    peers_with_pkg  = [peer for peer in alive_peers if await has_package(pkg_name, peer)]

    Debug.info(f"[USELESS] peers_with_pkg: {peers_with_pkg}")

    if len(peers_with_pkg) < 1:
        Debug.debug("[Peer] No peer with package")
        return None

    # Get the least latency peer 
    low_latency_peer = await peer_latency(peers_with_pkg)

    return low_latency_peer


async def has_package(pkg_name: str, peer: Peer) -> bool:
    """
    Asks the peer if it has the package
    """

    if await peer.connect() is False:
        Debug.error(0, f"[Peer] failed to connect to: ({peer.host}, {peer.port})")
        return False

    reader, writer = peer.get_reader_writer()

    req = make_response_strjson(RequestType.SEND_PKG, pkg_name)
    await async_write_data(req, writer)

    res_data = await async_read_data(reader)
    """
    data_len = int(await reader.readline())
    res_data = ""
    while len(res_data) < data_len:
        curr_data = await reader.read(10)
        res_data += curr_data.decode('utf-8')
    """
    Debug.info(f"[USELESS] res_str: {res_data}")

    res = Result(dict_from_str(res_data))

    if res.getType() == ResultType.FAILED:
        Debug.debug(f"[Connection] Failed result: {res.getType()}")
        return False

    data: list[dict] = res.getData()
    Debug.info(f"[USELESS] data: {data}")

    if len(data) < 1:  # No packages found in peer
        return False

    for pkgIdx in range(len(data)):
        pkg_dict: str = data[pkgIdx]
        if json.loads(pkg_dict).get("name", "") == pkg_name:
            peer._pkg_index = pkgIdx
            return True

    return False

async def peer_latency(peers: list[Peer]) -> Optional[Peer]:
    """
    Returns the peer with lowest latency
    TODO
    """
    if len(peers) > 0:
        return peers[0]
    else:
        return None
