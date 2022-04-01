import sys
import utils.Debug as Debug

if sys.platform == 'linux':
    from daemon.linux_daemon import start
else:
    Debug.error(1, "Only works on Linux for now")


def main() -> None:
    """
    Starts the daemon which controls the connections
    and the communication
    """
    start()
