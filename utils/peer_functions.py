from utils.Peer import Peer
from db.DBInterface import DatabaseInterface
import os
import socket
import platform


def add_to_db(peer: Peer):
    """
    Queries the peer for more info and
    Adds the peer to the database
    """
    db = DatabaseInterface()


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

