from asyncio.exceptions import CancelledError
import platform
from daemon.peer_functions import add_to_db, current_daemon_info, get_peer_with_package
from db.DBInterface import DatabaseInterface
from pkgman.Skel import get_info
from utils.Peer import Peer
import utils.Debug as Debug
from utils.helper_functions import (
    async_error_writer,
    async_read_data,
    make_response_strjson,
    make_result_strjson,
    async_write_data,
    dict_from_str,
    recv_file,
    send_file,
)
from utils.Types import RequestType, ResultType
from utils.Result import Result
from utils.Request import Request
from utils.Package import Package
import asyncio

from typing import Any
from asyncio import StreamReader, StreamWriter

if (platform.freedesktop_os_release().get("ID", "") == "arch") or (
    platform.freedesktop_os_release().get("ID_LIKE", "") == "arch"
):
    from pkgman import pacman as PackageManager

    Debug.debug(f"[OS] ID: {platform.freedesktop_os_release().get('ID', '')}")
else:
    Debug.error(1, "Supports only Arch as of now")


async def process_request(
    request: dict, reader: StreamReader, writer: StreamWriter
) -> None:
    """
    Process the json for further actions described in the
    RequestType class
    """
    peername = writer.get_extra_info("peername")
    # sockname = writer.get_extra_info("sockname")

    Debug.info(f"[USELESS] {request}")
    req = Request(request)

    if req.isInvalid():
        await async_error_writer(f"Invalid request type {req.getType()}", writer)
        return

    Debug.debug(f"[Connection {peername}] Request Type: {req.getType()}")

    request_type = req.getType()

    # Check if it is a normal ping
    if request_type == RequestType.PING:
        ping_resp = make_result_strjson(ResultType.SUCCESSFUL, "Pong")
        await async_write_data(ping_resp, writer)

    # Check if payload data is provided
    if not req.hasPayload():
        await async_error_writer(f"No data provided {peername}", writer)
        return

    # The real request handler
    if request_type == RequestType.SEARCH:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            return
        await search_package(package_name, writer)
    elif request_type == RequestType.PKG_INFO:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            return
        await package_info(package_name, writer)
    elif request_type == RequestType.SEND_PKG:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            Debug.error(0, f"No package name found {peername}")
            return
        await send_package(package_name, reader, writer)
    elif request_type == RequestType.FETCH_PKG:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            return
        await fetch_package(package_name, reader, writer)
    elif request_type == RequestType.ADD_PEER:
        # TODO: Add the requesting peer if it is not the cli
        host, port = req.getHostPort()

        if host == "" or int(port) == -1:
            # Error
            return
        Debug.info(f"[USELESS] ({host}, {port})")
        await add_peer((host, int(port)), writer)
    elif request_type == RequestType.PEER_INFO:
        # Write current daemon info
        await send_info(req, writer)

    await writer.drain()


async def search_package(pkg_name: str, writer: StreamWriter) -> None:
    """
    Handles the search request
    """
    pkg_list: list[str] = PackageManager.search_pkg(pkg_name)
    Debug.debug(f"[Package Names] {pkg_list}")

    res_json = make_result_strjson(ResultType.SUCCESSFUL, pkg_list)

    await async_write_data(res_json, writer)


async def package_info(pkg_name: str, writer: StreamWriter) -> None:
    """
    Handles getting package information
    """
    pkg_info: list[Package] = PackageManager.get_info(pkg_name)
    Debug.debug(f"[Package Info] {pkg_info}")

    res_json = make_result_strjson(ResultType.SUCCESSFUL, pkg_info)
    await async_write_data(res_json, writer)


async def send_package(pkg_name: str, reader: StreamReader, writer: StreamWriter):
    """
    Search the package in the cache, and send the package
    to the connected peer via the socket
    """
    package_list = PackageManager.search_pkg(pkg_name)

    # No packages found with that name
    if len(package_list) < 1:
        res = make_result_strjson(ResultType.FAILED, {}, f"No packages named {pkg_name}")
        Debug.debug(f"[PacakgeManager] Package {pkg_name} not found")
        await async_write_data(res, writer)
        return
    
    cached_pkgs: list[Package] = []
    for pkg in package_list:
        if PackageManager.in_cache(pkg):
            cached_pkgs.extend(PackageManager.get_info(pkg))

    # pacakage not found int cache
    if len(cached_pkgs) < 1:
        res = make_result_strjson(ResultType.FAILED, {}, f"Package {pkg_name} not in cache")
        Debug.debug(f"[PacakgeManager] Package {pkg_name} not found in cache")
        await async_write_data(res, writer)
        return
    
    pkg_info = [pkg.toJson() for pkg in cached_pkgs]

    res = make_result_strjson(ResultType.SUCCESSFUL, pkg_info)
    Debug.info(f"[USELESS] result: {res}")

    # Send data about available packages
    await async_write_data(res, writer)

    # Wait for peer to ask for which package he wants
    Debug.info("[USELESS] waiting from index")
    resp = await async_read_data(reader)

    req_obj = Request(dict_from_str(resp))

    if req_obj.getIndex() == -1 or req_obj.getIndex() > len(pkg_info):  # When peer doesn't want any package
        Debug.debug(f"[Peer] Index invalid {writer.get_extra_info('peername')}")
        # TODO: Error
        return

    # Send asker info about the file
    file_name = cached_pkgs[req_obj.getIndex()].filename()

    file_info = make_result_strjson(ResultType.SUCCESSFUL, file_name)
    Debug.info(f"[File] file_info result: {file_info}")

    await async_write_data(file_info, writer)
    Debug.info("[USELESS] after writing file_info send_package")

    # Send peer the required package
    # await send_file(cached_pkgs[req_obj.getIndex()].get_file_location(), writer)
    Debug.info(f"[Package] package index: {req_obj.getIndex()}")
    await send_file(cached_pkgs[req_obj.getIndex()].get_pkg_location(), writer)


async def fetch_package(
    pkg_name: str, reader: StreamReader, writer: StreamWriter
) -> None:
    """
    Asks the peers for the package and if it is present
    downloads it and saves it to a temp file and gives the
    location to the cli handler
    TODO:
        + Get peers list and ping each one of 'em for package
        + verify peer and package architecture
        + assert package checksum
    """
    # Get the peer list
    db = DatabaseInterface()
    #peers: list[Peer] = [peer for peer in db.get_peers() if await peer.async_is_alive()]
    peers: list[Peer] = [peer for peer in db.get_peers()]
    Debug.debug(f"[Peer] Peers in DB: {peers}")

    if len(peers) < 1:
        await async_write_data(make_result_strjson(ResultType.FAILED, {}, "No peers in the list"), writer)
        Debug.error(0, "[Peers] Not peers found in the PeerDB")
        return

    peer_with_pkg = await get_peer_with_package(pkg_name, peers)

    if peer_with_pkg is None:
        await async_write_data(make_result_strjson(ResultType.FAILED, {}, "No peers alive"), writer)
        Debug.error(0, "[Peers] All peers are down")
        return

    # TODO: ask peer to send the required package
    pkgIdx_str = make_response_strjson(RequestType.PKG_INDEX, peer_with_pkg._pkg_index)

    Debug.info("[USELESS] before sending index")
    await async_write_data(pkgIdx_str, peer_with_pkg._writer)

    # Get info about the file
    file_info = dict_from_str(await async_read_data(peer_with_pkg.get_reader_writer()[0]))
    Debug.info(f"[USELESS] after file_info: {file_info}")

    if file_info is None:
        # TODO: Error
        Debug.debug("[Daemon] Didn't receive file info")
        return

    file_info_res = Result(file_info)
    file_name = file_info_res.getData()

    Debug.info("[USELESS] before recv_file")
    file_loc  = await recv_file(file_name, peer_with_pkg._reader)

    Debug.debug(f"[File] file stored in: {file_loc}")

    found = make_result_strjson(ResultType.SUCCESSFUL, file_loc)
    await async_write_data(found, writer)


async def add_peer(peer_info: tuple[str, int], writer: StreamWriter):
    """
    Connect to peer verify arch and add to peer list
    """
    peer = Peer(peer_info[0], peer_info[1])
    if not await peer.async_is_alive():
        # TODO: Error
        Debug.debug(f"Host Down: {peer}")
        return
    await peer.async_populate_info()  
    add_to_db(peer)
    Debug.debug(f"[Peer] added new peer: {peer_info}")


async def send_info(req_obj: Request, writer: StreamWriter):
    """
    Sends the current daemon info to asker
    and adds the asker if it a deamon
    TODO: Write to writer about success
    """
    info = current_daemon_info()
    res = make_result_strjson(ResultType.SUCCESSFUL, info)

    # Send info
    await async_write_data(res, writer)

    if req_obj.host == "":
        return

    # The requester is probably a daemon 
    host = req_obj.host
    port = req_obj.port
    Debug.debug(f"[Peer] Checking if ({host}, {port}) is a daemon")
    check_daemon = make_response_strjson(RequestType.PING, {})

    peer = Peer(host, port)

    if await peer.connect() is False:
        Debug.debug(f"Failed to check if peer was daemon: ({host}, {port})")
        return

    r, w = peer.get_reader_writer()

    await async_write_data(check_daemon, w)
    resp = Result(dict_from_str(await async_read_data(r)))

    if resp.getType() == 1:  # Daemon!!
        Debug.debug(f"[Peer] ({host}, {port}) is a Daemon!")
        # await peer.async_populate_info() # TODO: This is leading to complications
        add_to_db(peer)
    else:
        Debug.debug(f"[Peer] ({host}, {port}) is not a daemon")
