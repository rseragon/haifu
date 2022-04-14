import sys
from utils.Debug import Debug
from utils.Config import Config
import signal
import os

if sys.platform == 'linux':
    from daemon.linux_daemon import start
else:
    Debug.error(1, "Only works on Linux for now")

def handle_sigint(signum: int, fram) -> None:
    Debug.debug("Signal detected, closing server")
    Config.remove_pidfile()
    os._exit(0)

def main(daemon: bool=False, DebugLevel: int=2) -> None:
    """
    Starts the daemon which controls the connections
    and the communication
    """
    Debug.set_level(DebugLevel)
    if daemon:
        pass
        # Setup daemoniker
    else:
        with open(Config.get_pidfile(), "w") as f:
            Debug.debug("PID: " + str(os.getpid()))
            f.write(str(os.getpid()))
        signal.signal(signal.SIGINT, handle_sigint)
        start()
