from daemon.peer_functions import get_peer_list
import utils.Debug as Debug


def test_get_peer_list():
    peers = get_peer_list()

    for peer in peers:
        Debug.debug(f"[Peer] {peer}")

test_get_peer_list()
