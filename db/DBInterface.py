from db.DBHandler import DatabaseHandler
import utils.Config as Config
import utils.Debug as Debug
from utils.Peer import Peer


class DatabaseInterface:
    """
    The bridge between the sqlite db and the usage
    """

    # DB_NAME = ":memory:"
    DB_NAME = Config.get_db()
    DB_CONN = DatabaseHandler(DB_NAME)

    def __init__(self):
        pass

    def insert_peer(self, peer: Peer):
        self.insert(peer.host, peer.port, peer.name, peer.arch, peer.os, peer.distro, int(peer.was_alive))

    def insert(
        self,
        host: str,
        port: int,
        name: str = "",
        arch: str = "",
        os: str = "",
        distro: str = "",
        was_alive: int = 0,
    ) -> bool:
        """
        returns True if inserted sucessfully
        else false
        """
        with DatabaseInterface.DB_CONN as cursor:
            exists = cursor.execute(
                "SELECT * FROM peers WHERE host==? AND port=?", (host, port)
            )

            if len(exists.fetchall()) != 0:
                print("Entry already exists")
                return False

            cursor.execute(
                """
            INSERT INTO peers(host, port, name, arch, os, distro, was_alive)
            VALUES (
                 ?, ?, ?, ?, ?, ?, ?
            )""",
                (host, port, name, arch, os, distro, was_alive),
            )
        return True

    def display_all(self):
        with DatabaseInterface.DB_CONN as cursor:
            peers = cursor.execute("""SELECT * FROM peers""").fetchall()
            Debug.info(peers)
