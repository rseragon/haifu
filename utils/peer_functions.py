from typing import Optional
from utils.Peer import Peer
from db.DBInterface import DatabaseInterface
import os
import socket
import platform

from asyncio import StreamReader, StreamWriter
from utils.Request import Request
from utils.Result import Result
from utils.Types import ResultType

from utils.helper_functions import async_read_data, async_write_data, make_response_strjson, dict_from_str


def add_to_db(peer: Peer):
    """
    Queries the peer for more info and
    Adds the peer to the database
    """
    db = DatabaseInterface()

    # TODO: Query for morei info?
    db.insert_peer(peer)


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


async def get_peer_with_package(peers: list[Peer], pkg_name: str) -> Optional[Peer]:
    """
    A greedy approach which returns the 
    reader and writer and index of package with 
    the least latency and 
    cached package
    """
    peers_with_pkg: list[Peer] = [peer for peer in peers if await has_package(peer, pkg_name) != -1]
    if len(peers_with_pkg) < 1:
        return None
    peer = nearest_peer(peers_with_pkg)
    
    return peer


async def has_package(peer: Peer, pkg_name: str) -> int:
    """
    Returns index if the packge exists
    or else it's -1
    """
    await peer.connect()  # TODO: error check

    reader, writer = peer.get_reader_writer()
    req = Request({})
    req.package_name = pkg_name

    await async_write_data(req.toJson(), writer)

    res = Result(dict_from_str(await async_read_data(reader)))

    if res.getType() == ResultType.ERROR:
        return -1
    
    peer._pkg_index = res.getData()
    return peer._pkg_index


async def nearest_peer(peers: list[Peer]):
    """
    Returns the index of peer with the lowest latency
    """
    return peers[0]
