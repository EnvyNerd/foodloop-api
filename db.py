import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "foodloop.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_conn()
    with open(os.path.join(os.path.dirname(__file__), "..", "schema_sqlite.sql"), "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def dict_from_row(row):
    if row is None:
        return None
    return dict(row)
