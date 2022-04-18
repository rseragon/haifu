from typing import Coroutine, Optional
from utils.Request import Request
from utils.Types import RequestType, ResultType
from utils.helper_functions import (
    async_read_data,
    async_write_data,
    dict_from_str,
    make_response_strjson,
    send_data,
)
from asyncio import StreamWriter
import asyncio
import utils.Debug as Debug
from utils.Result import Result
from asyncio import StreamReader, StreamWriter
from typing import Any
import utils.Config as Config


class Peer:
    def __init__(
        self,
        host: str,
        port: int,
        name: str = "",
        arch: str = "",
        os: str = "",
        distro: str = "",
        was_alive: int = 0,
    ):
        self.host = host
        self.port = port
        self.name = name
        self.arch = arch
        self.os = os
        self.distro = distro
        self.was_alive = was_alive

        # Only used when connection is made
        self._connected = False
        self._reader: StreamReader
        self._writer: StreamWriter
        self._pkg_index = -1  # This is for send_package to store index

    async def async_is_alive(self) -> bool:
        """
        Ping the daemon and check if it alive
        TODO: Update peer info, for discrepency
        """
        resp = make_response_strjson(
            RequestType.PING, {"info": "Ping!!!"}
        )  # The info is useless
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
        except ConnectionRefusedError:
            Debug.error(0, f"[Connection] Failed to connect ({self.host}, {self.port})")
            return False
        await async_write_data(resp, writer)

        result = await async_read_data(reader)

        Debug.info(f"[USELSS] {result}")
        if dict_from_str(result).get("Result", -1) == 1:
            self.was_alive = 1
            return True

        return False

    async def async_populate_info(self) -> bool:
        """
        Asks the peer for the requred info
        TODO: check if already in db, and update info
        """
        host, port = Config.get_hostport()
        Debug.info("[USELESS] Populating info")
        # req = Request({"Type": RequestType.PEER_INFO}).toJson() # TODO: Doesn't work
        req = make_response_strjson(RequestType.PEER_INFO, {"host": host, "port": port})# This acts the 2-way handshake)
        Debug.info(f"[USELESS] req: {req}")

        reader, writer = await self.connect()
        await async_write_data(req, writer)

        result = await async_read_data(reader)

        res = Result(dict_from_str(result))

        info = res.getData()

        self.name = info.get("name", "")
        self.arch = info.get("arch", "")
        self.os = info.get("os", "")
        self.distro = info.get("distro", "")
        self.was_alive = 1

        return True

    #async def _create_conn(self) -> Optional[tuple[StreamReader, StreamWriter]]:
    async def _create_conn(self) -> bool:
        """
        returns connection reader and writer for peer
        """
        if self._connected is not False:
            return True

        try:
            self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port
            )
            self._connected = True
        except ConnectionRefusedError as ce:
            Debug.error(0, f"[Connection] Failed to connect ({self.host}, {self.port}) " + str(e))
            return False

        return True


    async def connect(self) -> tuple[StreamReader, StreamWriter]:
        if self._connected is False:
            await self._create_conn()
        return self._reader, self._writer

    def __repr__(self) -> str:
        return f"({self.host}, {self.port}) [{self.name}, {self.arch}, {self.os}, {self.distro}]"
