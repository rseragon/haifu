from daemon.Types import ResultType

"""
Result data skeleton
{
    "Result": "NUMBER",
    "Payload": {
        "Data": "stuff",
        "Error": "NONE/ERROR"
    }
}
"""

class Result:
    """
    For JSON responses of results
    """

    def __init__(self, res: dict):
        self.type = res.get("Result", -1)

        self.payload: dict = res.get("Payload", None)

        self.data: str = ""
        if self.payload is not None:
            self.data: str = self.payload.get("Data", "")

    def isInvalid(self) -> bool:
        return (self.type == ResultType.INVALID) \
                or (self.type > ResultType.RES_MAX_NUM) \
                or (self.type < ResultType.RES_MIN_NUM)

    def getData(self) -> str:
        return self.data

    def getType(self) -> int:
        return self.type
