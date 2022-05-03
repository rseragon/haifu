from enum import IntEnum


class RequestType(IntEnum):
    """
    0. Quit daemon[local] (Handled by `handle_request` in linux_daemon)
    1. Search[Local]
    2. Get pkg info[Local]
    3. send package to the requester[External]
    4. fetch package[Local -> External]
    5. Add peer[local -> external]
    6. Peer info[writes the current daemon info to writer]
    Local = cli <-> daemon
    External = daemon <-> daemon

    """

    INVALID = -1
    QUIT = 0  # this is dummy, Will be handled by signals
    PING = 0  # If 0 is sent to another daemon, then it acts a ping
    SEARCH = 1
    PKG_INFO = 2
    SEND_PKG = 3
    PKG_INDEX = 4  # Used when getting index of packge from the received list of packages
    FETCH_PKG = 5
    ADD_PEER = 6
    PEER_INFO = 7
    FILE_INFO = 8  # Gets the file file info like name and size

    REQ_MIN_NUM = 0
    REQ_MAX_NUM = 8


class ResultType(IntEnum):
    """
    Result type specification
    """

    SUCCESSFUL = 1
    FAILED = 0
    ERROR = -1
    INVALID = -2

    RES_MIN_NUM = -1
    RES_MAX_NUM = 1
