import appdirs
import os
from pathlib import Path
import configparser
from datetime import datetime
from utils.Debug import Debug

"""
The main config module
"""

DIR_POPULATED = False
CONFIG_POPULATED = False
PROJECT_NAME = "haifu"  # TODO: remove hardcoding?

CONFIG_DIR: str = ""
LOG_DIR: str = ""
CACHE_DIR: str = ""

CONFIG_NAME: str = ""


LOG_FILE = None  # TODO: Type annotate
CONFIG_FILE = None
PID_FILE: str = ""

PID: int = -1

HOST: str = ""
PORT: int = -1


def populate_dirs() -> None:

    global DIR_POPULATED, CONFIG_DIR, CACHE_DIR, CONFIG_NAME, LOG_DIR, PROJECT_NAME

    config_dir = appdirs.user_config_dir(PROJECT_NAME)
    log_dir = appdirs.user_log_dir(PROJECT_NAME)
    cache_dir = appdirs.user_cache_dir(PROJECT_NAME)

    CONFIG_DIR = config_dir
    LOG_DIR = log_dir
    CACHE_DIR = cache_dir

    """
    Debug.debug("dir: " + config_dir)
    Debug.debug("log dir: " + log_dir)
    Debug.debug("cache dir: " + cache_dir)
    """

    if not Path(config_dir).exists():
        os.makedirs(config_dir)

    if not Path(log_dir).exists():
        os.makedirs(log_dir)

    if not Path(cache_dir).exists():
        os.makedirs(cache_dir)

    DIR_POPULATED = True
    config_name: str = str((Path(CONFIG_DIR) / "config.ini").absolute())
    CONFIG_NAME = config_name
    if not Path(config_name).exists():
        _basic_config()


def get_logfile():  # TODO: Type annotation
    """
    Returns the file object for the log file
    """

    global DIR_POPULATED, LOG_FILE, PROJECT_NAME, LOG_FILE

    if not DIR_POPULATED:
        populate_dirs()

    if LOG_FILE is not None:
        return LOG_FILE

    file_name = PROJECT_NAME + "_" + datetime.now().strftime("%d%m%Y_%H%M") + ".log"

    log_file: str = str((Path(LOG_DIR) / file_name).absolute())

    LOG_FILE = open(log_file, "w")

    return LOG_FILE


def _basic_config() -> None:
    """
    Adds basic config
    TODO: Get config from github repo
    """

    global CONFIG_NAME, CONFIG_DIR

    Debug.debug("file not found, Populating with default config")
    config_name: str = str((Path(CONFIG_DIR) / "config.ini").absolute())
    CONFIG_NAME = config_name

    with open(config_name, "w+") as conf_file:
        conf = "[daemon]\nhost=0.0.0.0\nport=42069\n"
        conf_file.write(conf)


def get_hostport() -> tuple[str, int]:
    """
    Reads the config and returns the host and port
    for the daemon
    """

    global DIR_POPULATED, CONFIG_NAME, CONFIG_DIR, CONFIG_FILE, HOST, PORT

    if not DIR_POPULATED:
        populate_dirs()

    populate_dirs()  # TODO: Call it

    if CONFIG_NAME == "":
        config_name: str = str((Path(CONFIG_DIR) / "config.ini").absolute())

        CONFIG_NAME = config_name
        CONFIG_FILE = open(config_name, "w+")

    if HOST != "":
        return (HOST, PORT)

    Debug.debug("config file name: " + CONFIG_NAME)

    parser = configparser.ConfigParser()
    parser.read_file(open(CONFIG_NAME, "r"))

    if parser.has_section("daemon"):
        HOST = parser["daemon"]["host"]
        PORT = int(parser["daemon"]["port"])
    else:
        Debug.debug("'daemon' section not found in config file")
        _basic_config()
        parser.read_file(open(CONFIG_NAME, "r"))
        HOST = parser["daemon"]["host"].strip()
        PORT = int(parser["daemon"]["port"].strip())

    return HOST, PORT


def get_pidfile() -> str:
    """
    returns the location of the pid file
    """

    global DIR_POPULATED, PID_FILE

    if not DIR_POPULATED:
        populate_dirs()

    if PID_FILE != "":
        return PID_FILE

    file_name = str((Path(CONFIG_DIR) / "pid.txt").absolute())
    PID_FILE = file_name

    return file_name


def get_pid() -> int:
    """
    returns the pid of current daemon if running
    or else returns -1
    """

    global PID

    file_name = get_pidfile()

    if Path(file_name).exists():
        with open(file_name, "r") as f:
            pid = int(f.readline())
            PID = pid
            return pid
    else:
        return -1


def remove_pidfile() -> None:
    try:
        os.remove(get_pidfile())
    finally:  # Don't care if file doesn't exist
        pass
