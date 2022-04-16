from utils.Types import ResultType
import json
from typing import Any

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

        self.data: Any
        self.error: str = ""
        if self.payload is not None:
            self.data: Any = self.payload.get("Data", "")
            self.error: str = self.payload.get("Error", "")

    def isInvalid(self) -> bool:
        return (
            (self.type == ResultType.INVALID)
            or (self.type > ResultType.RES_MAX_NUM)
            or (self.type < ResultType.RES_MIN_NUM)
        )

    def getData(self) -> Any:
        return self.data

    def getType(self) -> int:
        return self.type

    def to_json(self) -> str:
        return json.dumps(
            {"Result": self.type, "Payload": {"Data": self.data, "Error": self.error}}
        )

    def __repr__(self) -> str:
        return f'["Result": {self.type}, "Payload": ["Data": {self.data}, "Error": {self.error}]]'
