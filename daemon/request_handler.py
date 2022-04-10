from asyncio.exceptions import CancelledError
import platform
import json
from utils.Debug import Debug
import asyncio
from utils.helper_functions import error_writer, make_response_strjson, make_result_strjson, write_data
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

    req = Request(request)

    if req.isInvalid():
        await error_writer(f"Invalid request type {req.getType()}", writer)
        return

    Debug.debug(f"[Connection {peername}] Request Type: {req.getType()}")

    if not req.hasData():
        await error_writer(f"No data provided {peername}", writer)
        return

    request_type = req.getType()

    if request_type == RequestType.QUIT:
        raise CancelledError("Closing server")
    elif request_type == RequestType.SEARCH:
        package_name = req.getPackageName()
        if package_name == "":
            return
        await search_package(package_name, writer)
    elif request_type == RequestType.GET_INFO:
        package_name = req.getPackageName()
        if package_name == "":
            return
        await package_info(package_name, writer)
    elif request_type == RequestType.SEND_PKG:
        package_name = req.getPackageName()
        if package_name == "":
            return
        await send_package(package_name, reader, writer)
    elif request_type == RequestType.FETCH_PKG:
        package_name = req.getPackageName()
        if package_name == "":
            return
        await fetch_package(package_name, reader, writer)
    elif request_type == RequestType.ADD_PEER:
        pass

    await writer.drain()


async def search_package(pkg_name: str, writer: StreamWriter) -> None:
    """
    Handles the search request
    """
    pkg_list: list[str] = PackageManager.search_pkg(pkg_name)
    Debug.debug(f"[Package Names] {pkg_list}")

    res_json = make_result_strjson(ResultType.SUCCESSFUL, pkg_list)

    await write_data(res_json, writer)


async def package_info(pkg_name: str, writer: StreamWriter) -> None:
    """
    Handles getting package information
    """
    pkg_info: list[Package] = PackageManager.get_info(pkg_name)
    Debug.debug(f"[Package Info] {pkg_info}")

    res_json = make_result_strjson(ResultType.SUCCESSFUL, pkg_info)
    await write_data(res_json, writer)


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


async def add_peer(peer_info: Any, writer: StreamWriter):
    """
    Connect to peer verify arch and add to peer list
    TODO:
        + sqlite?
    """
    pass
