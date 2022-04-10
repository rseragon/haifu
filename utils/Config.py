import appdirs
import os
from pathlib import Path
import configparser
from datetime import datetime
import sys
from utils.Debug import Debug


class Config:
    """
    The main config class
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

    HOST: str = ""
    PORT: int = -1  

    @staticmethod
    def populate_dirs() -> None:

        config_dir = appdirs.user_config_dir(Config.PROJECT_NAME)
        log_dir = appdirs.user_log_dir(Config.PROJECT_NAME)
        cache_dir = appdirs.user_cache_dir(Config.PROJECT_NAME)
        
        Config.CONFIG_DIR = config_dir
        Config.LOG_DIR = log_dir
        Config.CACHE_DIR = cache_dir

        """
        Debug.debug("Config dir: " + config_dir)
        Debug.debug("log dir: " + log_dir)
        Debug.debug("cache dir: " + cache_dir)
        """

        if not Path(config_dir).exists():
            os.makedirs(config_dir)

        if not Path(log_dir).exists():
            os.makedirs(log_dir)

        if not Path(cache_dir).exists():
            os.makedirs(cache_dir)

        Config.DIR_POPULATED = True
        config_name: str = str((Path(Config.CONFIG_DIR)/"config.ini").absolute())
        Config.CONFIG_NAME = config_name


    @staticmethod
    def get_logfile():  # TODO: Type annotation
        """
        Returns the file object for the log file
        """
        if not Config.DIR_POPULATED:
            Config.populate_dirs()

        Config.populate_dirs()  # TODO: Call it not matter what

        if Config.LOG_FILE is not None:
            return Config.LOG_FILE

        file_name = Config.PROJECT_NAME + "_" + datetime.now().strftime("%d%m%Y_%H%M") + ".log"

        log_file: str = str((Path(Config.LOG_DIR)/file_name).absolute())

        Config.LOG_FILE = open(log_file, "w")

        return Config.LOG_FILE


    @staticmethod
    def _basic_config() -> None:
        """
        Adds basic config
        TODO: Get config from github repo
        """
        Debug.debug("Config file not found, Populating with default config")
        config_name: str = str((Path(Config.CONFIG_DIR)/"config.ini").absolute())
        Config.CONFIG_NAME = config_name

 
        with open(config_name, "w+") as conf_file:
            conf = "[daemon]\nhost=0.0.0.0\nport=42069\n"
            conf_file.write(conf)


    @staticmethod
    def get_hostport() -> tuple[str, int]:
        """
        Reads the config and returns the host and port
        for the daemon
        """
        if not Config.DIR_POPULATED:
            Config.populate_dirs()

        Config.populate_dirs()  # TODO: Call it
        
        if Config.CONFIG_NAME == "":
            config_name: str = str((Path(Config.CONFIG_DIR)/"config.ini").absolute())

            Config.CONFIG_NAME = config_name
            Config.CONFIG_FILE = open(config_name, "w+")

        if Config.HOST != "":
            return (Config.HOST, Config.PORT)

        if Path(Config.CONFIG_NAME).exists() is False:
            Config._basic_config()

        Debug.debug("config file name: " + Config.CONFIG_NAME)
        
        parser = configparser.ConfigParser()
        parser.read_file(open(Config.CONFIG_NAME, "r"))
        
        if parser.has_section('daemon'):
            Config.HOST = parser['daemon']['host']
            Config.PORT = int(parser['daemon']['port'])
        else:
            Debug.debug("'daemon' section not found in config file")
            Config._basic_config()
            parser.read_file(open(Config.CONFIG_NAME, "r"))
            Config.HOST = parser['daemon']['host'].strip()
            Config.PORT = int(parser['daemon']['port'].strip())
        
        return Config.HOST, Config.PORT
