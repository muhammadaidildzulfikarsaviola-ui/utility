import sqlite3
from datetime import datetime
from pathlib import Path


class ActivityTracker:
    """SQLite-backed session tracker for future application usage statistics."""

    def __init__(self, db_path="data/utility.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    ended_at TEXT,
                    duration_seconds INTEGER DEFAULT 0
                )
                """
            )
            connection.commit()

    def start_session(self, app_name):
        started_at = datetime.now().isoformat(timespec="seconds")
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO activity_sessions (app_name, started_at) VALUES (?, ?)",
                (app_name, started_at),
            )
            connection.commit()
            return cursor.lastrowid

    def end_session(self, session_id):
        ended_at = datetime.now()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT started_at FROM activity_sessions WHERE id = ?",
                (session_id,),
            ).fetchone()

            if row is None:
                return False

            started_at = datetime.fromisoformat(row[0])
            duration = max(0, int((ended_at - started_at).total_seconds()))

            connection.execute(
                """
                UPDATE activity_sessions
                SET ended_at = ?, duration_seconds = ?
                WHERE id = ?
                """,
                (ended_at.isoformat(timespec="seconds"), duration, session_id),
            )
            connection.commit()
            return True
