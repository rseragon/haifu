import asyncio
import socket
from typing import Callable, Any, Coroutine
from asyncio import StreamReader, StreamWriter
from utils.Debug import Debug


class Server:
    """
    The Sever which handles async clients
    """

    # TODO: Any should be Server in handle_request
    def __init__(
        self,
        host: str,
        port: int,
        handle_request: Callable[
            [
                StreamReader,
                StreamWriter,
                Any,
            ],
            Coroutine[Any, Any, None],  # TODO: Is this right?
        ],
    ):
        self.host = host
        self.port = port
        self.handle_request = handle_request
        self.server: Any  # TODO: Type this

    async def __aenter__(self):
        self.server = await asyncio.start_server(
            self._handle_request_placeholder,
            self.host,
            self.port,
            family=socket.AF_INET,
        )

        server_address = ", ".join(
            str(sock.getsockname()) for sock in self.server.sockets
        )
        Debug.debug(f"Serving on {server_address}")
        return self.server

    async def __aexit__(self, exc_type, exc, tb):
        self.server.close()
        await self.server.wait_closed()

    async def _handle_request_placeholder(self, reader, writer):
        """
        A place holder which will call the real request handler
        """
        await self.handle_request(reader, writer, self)

    async def aclose(self):
        """
        Signals the server shutdown with asyncio.CancelledException
        which should be handled by the called and close it gracefully
        """
        self.server.close()
        await self.server.wait_closed()
