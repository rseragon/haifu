import platform
import asyncio
import utils.Debug as Debug
import utils.config as config
from daemon.Server import Server

# Typing
from typing import Callable, Any
from asyncio import CancelledError, StreamReader, StreamWriter

if (platform.freedesktop_os_release().get("ID", "") == "arch") or (
    platform.freedesktop_os_release().get("ID_LIKE", "") == "arch"
):
    Debug.debug(f"[OS] ID: {platform.freedesktop_os_release().get('ID', '')}")
else:
    Debug.error(1, "Supports only Arch as of now")


async def handle_request(
    reader: StreamReader,
    writer: StreamWriter,
    server: Server,
) -> None:

    """
    Handles request given by the server
    """
    peername = writer.get_extra_info("peername")
    sockname = writer.get_extra_info("sockname")
    Debug.debug(f"[Connection] New: {sockname} <- {peername}")

    # TODO: Main stuff goes here

    await writer.drain()
    writer.close()
    Debug.debug(f"[Connection] Closing: {sockname} <- {peername}")
    await writer.wait_closed()
    Debug.debug(f"[Connection] Closed: {sockname} <- {peername}")


async def async_start() -> None:
    """
    Starts the async server
    """
    [host, port] = config.get_hostport()

    try:
        async with Server(host, port, handle_request) as server:
            async with server:
                await server.serve_forever()
    except CancelledError:
        Debug.debug("Closing server")
        await server.aclose()
    except Exception as ex:
        Debug.error(0, "Exception occured: " + str(ex))

    Debug.info("Server closed")


def start() -> None:
    """
    Starts the linux daemon
    """
    asyncio.run(async_start())
