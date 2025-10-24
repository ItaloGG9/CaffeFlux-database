import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', '/tmp/local_database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
