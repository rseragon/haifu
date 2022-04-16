import sqlite3 as sqlite


class DatabaseHandler:
    def __init__(self, dbname: str):
        self.conn = sqlite.connect(dbname)

        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS peers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host TEXT NOT NULL,
            port INTEGER NOT NULL,
            name TEXT,
            arch TEXT,
            os   TEXT,
            distro TEXT,
            was_alive INT)"""
        )

    def __enter__(self) -> sqlite.Cursor:
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is not None:
            raise exception_type(exception_value)

        if self.cursor is not None:
            self.cursor.close()
        self.conn.commit()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        self.conn.commit()
        self.conn.close()
