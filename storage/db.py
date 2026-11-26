# storage/db.py
import json
import os
import sqlite3
from pathlib import Path

APP_DIR = Path(os.getenv("APPDATA") or Path.home() / ".planner") / "Planner"
DB = APP_DIR / "planner.db"


def _conn():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB)


def init():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT);
        CREATE TABLE IF NOT EXISTS snapshots (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, payload TEXT);
        CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
        """)


def add_msg(role: str, content: str):
    with _conn() as c:
        c.execute("INSERT INTO chat(role, content) VALUES (?,?)", (role, content))


def history(limit: int = 40) -> list[dict]:
    """Последние `limit` сообщений в хронологическом порядке (было: задом наперёд)."""
    with _conn() as c:
        rows = c.execute("SELECT role, content FROM chat ORDER BY id DESC LIMIT ?",
                         (limit,)).fetchall()
    return [{"role": r, "content": t} for r, t in reversed(rows)]


def get_setting(key: str, default=None):
    with _conn() as c:
        r = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return r[0] if r else default


def set_setting(key: str, value):
    with _conn() as c:
        c.execute("INSERT INTO settings(key, value) VALUES (?,?) "
                  "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))


def del_setting(key: str):
    with _conn() as c:
        c.execute("DELETE FROM settings WHERE key=?", (key,))


def save_snapshot(name: str, payload: dict):
    with _conn() as c:
        c.execute("INSERT INTO snapshots(name, payload) VALUES (?,?)",
                  (name, json.dumps(payload, ensure_ascii=False, default=str)))


def last_snapshot(name: str) -> dict | None:
    with _conn() as c:
        r = c.execute("SELECT payload FROM snapshots WHERE name=? ORDER BY id DESC LIMIT 1",
                      (name,)).fetchone()
    return json.loads(r[0]) if r else None
