import argparse
import sys
import os  # Signal
import signal

from daemon import daemon
from utils.helper_functions import make_response_strjson, send_data
from utils.Types import RequestType
import utils.Debug as Debug
import utils.Config as Config

from cli.cli_helpers import check_alive, print_usage

def parse_cliargs(args: list) -> None:

    if len(args) < 2:
        print_usage()

    parser = argparse.ArgumentParser(description="A Distributed meta Package Manager")
    parser.add_argument('subcmd', metavar='SUBCOMMAND', help = "daemon, version, search, install, info")
    parser.add_argument('action', metavar='ACTION', nargs="?", help="start, stop, <package-name>, (host, port)")

    cli_args = parser.parse_args()

    [dhost, dport] = Config.get_hostport()

    Debug.debug(f"[CLI] SUBCOMMAND: {cli_args.subcmd}")
    Debug.debug(f"[CLI] ACTION: {cli_args.action}")

    if cli_args.subcmd != 'daemon':
        if check_alive() is False:
            Debug.error(1, "Unable to connect to daemon")
 


    if cli_args.subcmd == 'daemon':
        if cli_args.action is None:
            Debug.error(1, f"Action not provided\nUsage: {sys.argv[0]} daemon start/stop")
            return
        elif cli_args.action == 'start':
            daemon.main()
        elif cli_args.action == 'stop':
            # send_data(make_response_strjson(RequestType.QUIT, {}), dhost, dport)
            # Raise signal
            pid = Config.get_pid()
            if pid != -1:
                os.kill(pid, signal.SIGINT)
            else:
                Debug.error(1, "Unknown pid")
        else:
            Debug.error(1, f"Action not provided\nUsage: {sys.argv[0]} daemon start/stop")
    elif cli_args.subcmd == 'search':
        if cli_args.action is None:
            Debug.error(1, f"Action not provided\nUsage: {sys.argv[0]} search <package_name>")
            return
        else:
            resp = send_data(make_response_strjson(RequestType.SEARCH, cli_args.action), dhost, dport)
            Debug.debug(f"[CLI] {resp}")

    elif cli_args.subcmd == 'install':
        pass

    elif cli_args.subcmd == 'info':
        if cli_args.action is None:
            Debug.error(1, f"Action not provided\nUsage: {sys.argv[0]} info <package_name>")
            return
        else:
            resp = send_data(make_response_strjson(RequestType.GET_INFO, cli_args.action), dhost, dport)
            Debug.debug(f"[CLI] {resp}")

    else:
        Debug.error(1, "Unknown subcommand command")
