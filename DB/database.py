import sqlite3

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()
            self.connection = None
