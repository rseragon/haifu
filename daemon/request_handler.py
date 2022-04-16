from asyncio.exceptions import CancelledError
import platform
from daemon.peer_functions import add_to_db, current_daemon_info
from utils.Peer import Peer
import utils.Debug as Debug
from utils.helper_functions import async_error_writer, make_response_strjson, make_result_strjson, async_write_data
from utils.Types import RequestType, ResultType
from utils.Result import Result
from utils.Request import Request
from utils.Package import Package

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
    elif request_type == RequestType.GET_INFO:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            return
        await package_info(package_name, writer)
    elif request_type == RequestType.SEND_PKG:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            return
        await send_package(package_name, reader, writer)
    elif request_type == RequestType.FETCH_PKG:
        package_name = req.getPackageName()
        if package_name == "":
            # TODO: ERROR
            return
        await fetch_package(package_name, reader, writer)
    elif request_type == RequestType.ADD_PEER:
        host, port = req.getHostPort()
        
        if host == "" or int(port) == -1:
            # Error
            return
        Debug.info(f"[USELESS] ({host}, {port})")
        await add_peer((host, int(port)), writer)
    elif request_type == RequestType.PEER_INFO:
        # Write current daemon info to writer
        await send_info(writer)

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
    pass


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
    pass


async def add_peer(peer_info: tuple[str, int], writer: StreamWriter):
    """
    Connect to peer verify arch and add to peer list
    """
    peer = Peer(peer_info[0], peer_info[1])
    if not await peer.async_is_alive():
        # TODO: Error
        Debug.debug(f"Host Down: {peer}")
        return
    # TODO: Doesn't work
    await peer.async_populate_info()
    add_to_db(peer)
    Debug.debug(f"[Peer] added new peer: {peer_info}")


async def send_info(writer: StreamWriter):
    """
    Sends the current daemon info to asker
    """
    info = current_daemon_info()
    res = make_result_strjson(ResultType.SUCCESSFUL, info)

    await async_write_data(res, writer)
