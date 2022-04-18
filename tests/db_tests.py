from db.DBInterface import DatabaseInterface
import utils.Debug as Debug


def test_get_peers():
    db = DatabaseInterface()

    for peer in db.get_peers():
        Debug.info(f"[Peer] {peer}")


test_get_peers()
