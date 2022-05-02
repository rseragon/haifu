from utils.Types import RequestType
import json
from typing import Any

"""
Reqeust json skelton
{
    "Type": "NUMBER",
    "Payload": {
        "info": "STR"  # Contains some random data

        "host": "STR",
        "port": "NUMBER"

        "Package Name": "NAME",

        "index": "NUMBER"  # Used for send_package

    }
}
"""


class Request(dict):
    def __init__(self, req: dict):
        """
        Takes in the request dict and
        converts into a object
        """
        self.type: int = req.get("Type", -1)

        self.payload: dict = req.get("Payload", None)

        self.host: str = ""
        self.port: int = -1
        self.package_name: str = ""
        self.info: str = ""
        self.index: int = -1

        if self.payload is not None:
            self.host: str = self.payload.get("host", "")
            self.port: int = self.payload.get("port", "")
            self.package_name: str = self.payload.get("Package Name", "")
            self.info: str = self.payload.get("info", "")
            self.index: int = self.payload.get("index", "")

    def isInvalid(self) -> bool:
        return (
            (self.type == RequestType.INVALID)
            or (self.type > RequestType.REQ_MAX_NUM)
            or (self.type < RequestType.REQ_MIN_NUM)
        )

    def hasPayload(self) -> bool:
        return self.payload is not None

    def hasInfo(self) -> bool:
        return self.info != ""

    def getType(self) -> int:
        return self.type

    def getHostPort(self) -> tuple[str, int]:
        return (self.host, self.port)

    def getPackageName(self) -> str:
        return self.package_name

    def getInfo(self) -> str:
        return self.info

    def getIndex(self) -> int:
        return self.index

    def toJson(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)


class MakeRequest:

    def __init__(self, req_type: RequestType, data: Any):
        pass
