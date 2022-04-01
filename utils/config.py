""" 
parse .config files and return appropriate
stuff
"""
# TODO: read from config


def get_hostport() -> tuple[str, int]:
    return "0.0.0.0", 42069


def peer_list() -> list[list]:
    """
    parsese the .config file
    and returns the list
    of known peers daemons from the config
    or the sqlite database
    """
    return [["127.0.0.1", 42069]]
