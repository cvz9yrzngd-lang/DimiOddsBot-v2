import sqlite3
from config import DATABASE


def connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        chat_id INTEGER PRIMARY KEY
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS leagues(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        league_key TEXT UNIQUE,
        league_name TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS odds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT UNIQUE,
        home REAL,
        draw REAL,
        away REAL,
        kickoff TEXT,
        league TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(chat_id):
    conn = connect()

    conn.execute(
        "INSERT OR IGNORE INTO users(chat_id) VALUES(?)",
        (chat_id,)
    )

    conn.commit()
    conn.close()


def get_users():
    conn = connect()

    rows = conn.execute(
        "SELECT chat_id FROM users"
    ).fetchall()

    conn.close()

    return [row["chat_id"] for row in rows]


def add_league(key, name):
    conn = connect()

    conn.execute(
        "INSERT OR IGNORE INTO leagues(league_key, league_name) VALUES(?, ?)",
        (key, name)
    )

    conn.commit()
    conn.close()


def remove_league(key):
    conn = connect()

    conn.execute(
        "DELETE FROM leagues WHERE league_key=?",
        (key,)
    )

    conn.commit()
    conn.close()


def get_leagues():
    conn = connect()

    rows = conn.execute(
        "SELECT * FROM leagues ORDER BY league_name"
    ).fetchall()

    conn.close()

    return rows