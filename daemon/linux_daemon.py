import asyncio
from utils.Debug import Debug
from utils.Config import Config
from utils.Types import RequestType
from daemon.Server import Server
from utils.helper_functions import read_data, dict_from_str
from daemon.request_handler import process_request

# Typing
from typing import Callable, Any
from asyncio import CancelledError, StreamReader, StreamWriter


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
    data = await read_data(reader) 

    dict_data = dict_from_str(data)

    if dict_data.get("Type", RequestType.INVALID) == RequestType.QUIT:
        await server.aclose()

    await process_request(dict_data, reader, writer)

    await writer.drain()
    writer.close()
    Debug.debug(f"[Connection] Closing: {sockname} <- {peername}")
    await writer.wait_closed()
    Debug.debug(f"[Connection] Closed: {sockname} <- {peername}")


async def async_start() -> None:
    """
    Starts the async server
    """
    [host, port] = Config.get_hostport()
    host = str(host)
    port = int(port)

    try:
        async with Server(host, port, handle_request) as server:
            async with server:
                await server.serve_forever()
    except CancelledError:
        Debug.debug("Closing server")
        Config.remove_pidfile()
    """
    except Exception as ex:
        Debug.error(0, "Exception occured: " + str(ex))
    """


def start() -> None:
    """
    Starts the linux daemon
    """
    try:
        asyncio.run(async_start())
    except KeyboardInterrupt:
        Debug.info("Keyboard interrupt occured, closing server...")
    Debug.info("Server closed")
