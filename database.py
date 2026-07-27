import sqlite3
from config import DATABASE


def connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_name TEXT UNIQUE,
        home REAL,
        draw REAL,
        away REAL,
        updated_at TEXT
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


def add_match(match_name, home, draw, away):
    conn = connect()

    conn.execute("""
    INSERT OR REPLACE INTO matches(
        match_name,
        home,
        draw,
        away,
        updated_at
    )
    VALUES(?,?,?,?,datetime('now'))
    """, (
        match_name,
        home,
        draw,
        away
    ))

    conn.commit()
    conn.close()


def get_matches():
    conn = connect()

    rows = conn.execute(
        "SELECT * FROM matches ORDER BY id"
    ).fetchall()

    conn.close()

    return rows


def update_match(match_id, home, draw, away):
    conn = connect()

    conn.execute("""
    UPDATE matches
    SET
        home=?,
        draw=?,
        away=?,
        updated_at=datetime('now')
    WHERE id=?
    """, (
        home,
        draw,
        away,
        match_id
    ))

    conn.commit()
    conn.close()


def remove_match(match_name):
    conn = connect()

    conn.execute(
        "DELETE FROM matches WHERE match_name=?",
        (match_name,)
    )

    conn.commit()
    conn.close()


def clear_matches():
    conn = connect()

    conn.execute("DELETE FROM matches")

    conn.commit()
    conn.close()