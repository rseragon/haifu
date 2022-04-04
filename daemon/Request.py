from daemon.Types import RequestType

"""
Reqeust json skelton
{
    "Type": "NUMBER",
    "Payload": {
        "Package Name": "NAME",
        "Peer Name": "NAME",
        "PUID": "Peer Unique ID"
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

        self.peer_name: str = ""
        self.peerid: str = ""
        self.package_name: str = ""


        if self.payload is not None:
            self.peer_name: str = self.payload.get("Peer Name", "")
            self.peerid: str = self.payload.get("PUID", "")
            self.package_name: str = self.payload.get("Package Name", "")

    def isInvalid(self) -> bool:
        return (self.type == RequestType.INVALID) \
                or (self.type > RequestType.REQ_MAX_NUM) \
                or  (self.type < RequestType.REQ_MIN_NUM)

    def hasData(self) -> bool:
        return (self.payload is not None)

    def getType(self) -> int:
        return self.type

    def getPeerName(self) -> str:
        return self.peer_name

    def getPeerId(self) -> str:
        return self.peerid

    def getPackageName(self) -> str:
        return self.package_name
