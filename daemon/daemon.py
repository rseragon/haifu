import sys
import utils.Debug as Debug
import utils.Config as Config
import signal
import os

from daemoniker import Daemonizer, SIGINT, SignalHandler1, send

if sys.platform == 'linux':
    from daemon.linux_daemon import start
else:
    Debug.error(1, "Only works on Linux for now")

def handle_sigint(signum: int, fram) -> None:
    Debug.debug("Signal detected, closing server")
    clean_up()
    os._exit(0)

def main(daemon: bool=False, DebugLevel: int=2) -> None:
    """
    Starts the daemon which controls the connections
    and the communication
    """
    Debug.set_level(DebugLevel)
    if daemon:
        with Daemonizer() as (is_setup, daemonizer):
            if is_setup:
                # TODO: do setups
                pass

            is_parent = daemonizer(Config.get_pidfile())

            if is_parent:
                Debug.debug("PID: " + str(os.getpid()))
                # TODO: Is this required?
                pass

        # Setting up signal handlers
        sighandler = SignalHandler1(Config.get_pidfile())
        sighandler.start()
        sighandler.sigint = handle_sigint

        Debug.debug("PID: " + str(os.getpid()))
        start()
            
    else:
        with open(Config.get_pidfile(), "w") as f:
            Debug.debug("PID: " + str(os.getpid()))
            f.write(str(os.getpid()))
        signal.signal(signal.SIGINT, handle_sigint)
        start()


def clean_up() -> None:
    """
    Clean ups the daemon and the files
    """
    if Config.LOG_FILE is not None:
        Config.LOG_FILE.close()

    Config.remove_pidfile()
