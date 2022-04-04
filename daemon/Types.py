from enum import IntEnum


class RequestType(IntEnum):
    """
    0. Quit daemon[local] (Handled by `handle_request` in linux_daemon)
    1. Search[Local]
    2. Get pkg info[Local]
    3. send package to the requester[External]
    4. fetch package[Local -> External]
    Local = cli <-> daemon
    External = daemon <-> daemon

    """
    INVALID   = -1
    QUIT      = 0
    SEARCH    = 1
    GET_INFO  = 2
    SEND_PKG  = 3
    FETCH_PKG = 4
    ADD_PEER  = 5

    REQ_MIN_NUM = 0
    REQ_MAX_NUM = 5


class ResultType(IntEnum):
    """
    Result type specification
    """
    SUCCESSFUL = 1
    FAILED = 0
    INVALID = -1

    RES_MIN_NUM = -1
    RES_MAX_NUM = 1
