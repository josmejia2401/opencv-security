import sqlite3

class ManageDB:

    connection: sqlite3.Connection

    def __init__(self) -> None:
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect("open_security.db", check_same_thread=False, timeout=10, isolation_level=None)
        print("total_changes", self.connection.total_changes)
    
    def create_all(self):
        self.create_table_users()
        self.create_user_defaults()

    def create_table_users(self):
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE if not exists users (username TEXT, full_name TEXT, email TEXT, password TEXT)")

    def create_user_defaults(self):
        if len(self.find_user('esterc')) == 0:
            cursor: sqlite3.Cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users VALUES ('esterc', 'Ester Cordoba', 'estercordoba1928@gmail.com', 'esterc')")
            cursor.execute("INSERT INTO users VALUES ('josem', 'Jose Mejia', 'josmejia.2401@gmail.com', 'josem')")

    def create_user(self, username, full_name, email, password):
        if len(self.find_user(username)) == 0:
            cursor: sqlite3.Cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                                (username, full_name, email, password,))

    def find_user(self, username) -> list[any]:
        cursor: sqlite3.Cursor = self.connection.cursor()
        rows = cursor.execute(
            "SELECT username, full_name, email, password FROM users WHERE username = ?",
            (username,),
        ).fetchall()
        # [('Jamie', 'cuttlefish', 7)]
        return rows
    
    def find_user_and_pass(self, username, password) -> list[any]:
        cursor: sqlite3.Cursor = self.connection.cursor()
        rows = cursor.execute(
            "SELECT username, full_name, email, password FROM users WHERE username = ? AND password = ?",
            (username, password,),
        ).fetchall()
        # [('Jamie', 'cuttlefish', 7)]
        return rows
    
    def update_user_full_name(self, username, full_name):
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET full_name = ? WHERE username = ?",
            (full_name, username))
    
    def delete_user(self, username):
        cursor: sqlite3.Cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM users WHERE username = ?",
            (username,)
        )
    
    def close_connection(self):
        self.connection.close()
