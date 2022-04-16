from utils.Request import Request
from utils.Types import RequestType, ResultType
from utils.helper_functions import async_read_data, async_write_data, dict_from_str, make_response_strjson, send_data
from asyncio import StreamWriter
import asyncio
import utils.Debug as Debug
from utils.Result import Result



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


    async def async_is_alive(self) -> bool:
        """
        Ping the daemon and check if it alive
        """
        resp = make_response_strjson(RequestType.PING, {"info": "Ping!!!"})  # The info is useless
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
        """
        Debug.info("[USELESS] Populating info")
        req = Request({"Type": RequestType.PEER_INFO}).to_json()
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
        except ConnectionRefusedError:
            Debug.error(0, f"[Connection] Failed to connect ({self.host}, self.port)")
            return False

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

    def __repr__(self) -> str:
        return f"({self.host}, {self.port}) [{self.name}, {self.arch}, {self.os}, {self.distro}]"


