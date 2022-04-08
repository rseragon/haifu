import appdirs
import configparser
import os
from pathlib import Path
"""
parse .config files and return appropriate
stuff
"""

CONFIG_POPULATED = False


def populate_configs() -> None:
    """
    Populates the config, cache directories
    with placeholders
    """
    global CONFIG_POPULATED

    if CONFIG_POPULATED:
        return

    project_name = "haifu"  # TODO: any way to remove this hardcode?

    config_dir = appdirs.user_config_dir(project_name)
    log_dir = appdirs.user_log_dir(project_name)
    cache_dir = appdirs.user_cache_dir(project_name)

    if not Path(config_dir).exists():
        os.makedirs(config_dir)

    if not Path(log_dir).exists():
        os.makedirs(log_dir)

    if not Path(cache_dir).exists():
        os.makedirs(cache_dir)

    CONFIG_POPULATED = True


def get_hostport() -> tuple[str, int]:
    return "0.0.0.0", 42069


def get_daemon_hostport() -> tuple[str, int]:
    return "0.0.0.0", 42069


def peer_list() -> list[list]:
    """
    parsese the .config file
    and returns the list
    of known peers daemons from the config
    or the sqlite database
    """
    return [["127.0.0.1", 42069]]
