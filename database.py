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
        league_key TEXT UNIQUE NOT NULL,
        league_name TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS odds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT UNIQUE NOT NULL,
        league_key TEXT NOT NULL,
        home_team TEXT NOT NULL,
        away_team TEXT NOT NULL,
        home REAL NOT NULL,
        draw REAL NOT NULL,
        away REAL NOT NULL,
        kickoff TEXT NOT NULL,
        last_update TEXT
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


def add_league(league_key, league_name):
    conn = connect()

    conn.execute(
        """
        INSERT OR IGNORE INTO leagues(league_key, league_name)
        VALUES(?, ?)
        """,
        (league_key, league_name)
    )

    conn.commit()
    conn.close()


def remove_league(league_key):
    conn = connect()

    conn.execute(
        "DELETE FROM leagues WHERE league_key=?",
        (league_key,)
    )

    conn.commit()
    conn.close()


def get_leagues():
    conn = connect()

    rows = conn.execute(
        """
        SELECT *
        FROM leagues
        ORDER BY league_name
        """
    ).fetchall()

    conn.close()

    return rows


def save_odds(
    match_id,
    league_key,
    home_team,
    away_team,
    home,
    draw,
    away,
    kickoff,
    last_update
):
    conn = connect()

    conn.execute(
        """
        INSERT OR REPLACE INTO odds(
            match_id,
            league_key,
            home_team,
            away_team,
            home,
            draw,
            away,
            kickoff,
            last_update
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            match_id,
            league_key,
            home_team,
            away_team,
            home,
            draw,
            away,
            kickoff,
            last_update
        )
    )

    conn.commit()
    conn.close()


def get_saved_odds():
    conn = connect()

    rows = conn.execute(
        """
        SELECT *
        FROM odds
        """
    ).fetchall()

    conn.close()

    return rows


def delete_match(match_id):
    conn = connect()

    conn.execute(
        "DELETE FROM odds WHERE match_id=?",
        (match_id,)
    )

    conn.commit()
    conn.close()