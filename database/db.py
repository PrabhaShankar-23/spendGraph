import sqlite3
from datetime import date, timedelta
from pathlib import Path

from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = date.today()
    offsets = [18, 15, 12, 10, 7, 5, 3, 1]
    dates = [(today - timedelta(days=o)).isoformat() for o in offsets]

    sample_expenses = [
        (user_id, 12.50, "Food",          dates[0], "Groceries"),
        (user_id, 8.00,  "Transport",     dates[1], "Bus pass top-up"),
        (user_id, 45.00, "Bills",         dates[2], "Electricity bill"),
        (user_id, 60.00, "Health",        dates[3], "Pharmacy"),
        (user_id, 15.00, "Entertainment", dates[4], "Movie tickets"),
        (user_id, 32.75, "Shopping",      dates[5], "New shoes"),
        (user_id, 9.99,  "Other",         dates[6], "Miscellaneous"),
        (user_id, 20.00, "Food",          dates[7], "Dinner out"),
    ]
    conn.executemany(
        """INSERT INTO expenses (user_id, amount, category, date, description)
           VALUES (?, ?, ?, ?, ?)""",
        sample_expenses,
    )
    conn.commit()
    conn.close()
