from utils.Types import RequestType
import json

"""
Reqeust json skelton
{
    "Type": "NUMBER",
    "Payload": {
        "info": "STR"  # Contains some random data

        "host": "STR",
        "port": "NUMBER"

        "Package Name": "NAME",

    }
}
"""


class Request:
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

        if self.payload is not None:
            self.host: str = self.payload.get("host", "")
            self.port: int = self.payload.get("port", "")
            self.package_name: str = self.payload.get("Package Name", "")
            self.info: str = self.payload.get("info", "")

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

    def to_json(self) -> str:
        return json.dumps({
            "Type": self.type,
            "Payload": {
                "info": self.info,
                "host": self.host,
                "port": self.port,
                "Pacakge Name": self.package_name,
                }
            })
