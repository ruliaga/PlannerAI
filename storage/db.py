from __future__ import annotations
import json, os, sqlite3
from datetime import datetime
from pathlib import Path

APP_DIR = Path(os.getenv("APPDATA") or Path.home() / ".planner") / "Planner"
APP_DIR.mkdir(parents=True, exist_ok=True)
DB = APP_DIR / "planner.db"


def _conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS chat(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL, content TEXT NOT NULL, ts TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS snapshots(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, payload TEXT NOT NULL, ts TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS settings(k TEXT PRIMARY KEY, v TEXT);
        """)


def add_msg(role: str, content: str):
    with _conn() as c:
        c.execute("INSERT INTO chat(role, content, ts) VALUES (?,?,?)",
                  (role, content, datetime.utcnow().isoformat()))


def history(limit: int = 40) -> list[dict]:
    with _conn() as c:
        rows = c.execute("SELECT role, content FROM chat ORDER BY id DESC LIMIT ?",
                         (limit,)).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


def save_snapshot(name: str, payload: dict):
    with _conn() as c:
        c.execute("INSERT INTO snapshots(name, payload, ts) VALUES (?,?,?)",
                  (name, json.dumps(payload, ensure_ascii=False, default=str),
                   datetime.utcnow().isoformat()))


def last_snapshot(name: str) -> dict | None:
    with _conn() as c:
        r = c.execute("SELECT payload FROM snapshots WHERE name=? ORDER BY id DESC LIMIT 1",
                      (name,)).fetchone()
    return json.loads(r["payload"]) if r else None