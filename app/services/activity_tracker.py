import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path

try:
    import ctypes
    import psutil
except ImportError:
    ctypes = None
    psutil = None


class ActivityTracker:
    """Track foreground Windows applications and active computer time."""

    def __init__(self, db_path="data/utility.db", idle_threshold=60):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.idle_threshold = idle_threshold
        self.current_session_id = None
        self.current_app = None
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

    @staticmethod
    def is_supported():
        return os.name == "nt" and ctypes is not None and psutil is not None

    @staticmethod
    def get_idle_seconds():
        if not ActivityTracker.is_supported():
            return 0
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

        info = LASTINPUTINFO()
        info.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(info)):
            return 0
        tick = ctypes.windll.kernel32.GetTickCount64()
        return max(0, (tick - info.dwTime) / 1000.0)

    @staticmethod
    def get_foreground_app():
        if not ActivityTracker.is_supported():
            return None
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if not hwnd:
            return None
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        try:
            process = psutil.Process(pid.value)
            name = process.name()
            return Path(name).stem or name
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None

    def start_session(self, app_name):
        if not app_name:
            return None
        started_at = datetime.now().isoformat(timespec="seconds")
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO activity_sessions (app_name, started_at) VALUES (?, ?)",
                (app_name, started_at),
            )
            connection.commit()
            self.current_session_id = cursor.lastrowid
            self.current_app = app_name
            return self.current_session_id

    def end_session(self, session_id=None):
        session_id = session_id or self.current_session_id
        if session_id is None:
            return False

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
                "UPDATE activity_sessions SET ended_at = ?, duration_seconds = ? WHERE id = ?",
                (ended_at.isoformat(timespec="seconds"), duration, session_id),
            )
            connection.commit()

        if session_id == self.current_session_id:
            self.current_session_id = None
            self.current_app = None
        return True

    def poll(self):
        """Update the current session. Returns the active app name, or None while idle."""
        if not self.is_supported():
            return None

        idle = self.get_idle_seconds()
        app_name = None if idle >= self.idle_threshold else self.get_foreground_app()

        if app_name != self.current_app:
            if self.current_session_id is not None:
                self.end_session()
            if app_name:
                self.start_session(app_name)
        return app_name

    def get_today_total_seconds(self):
        today = datetime.now().date().isoformat()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COALESCE(SUM(duration_seconds), 0) FROM activity_sessions "
                "WHERE date(started_at) = ?",
                (today,),
            ).fetchone()
        total = int(row[0] or 0)
        if self.current_session_id:
            with self._connect() as connection:
                row = connection.execute(
                    "SELECT started_at FROM activity_sessions WHERE id = ?",
                    (self.current_session_id,),
                ).fetchone()
            if row:
                total += max(0, int(time.time() - datetime.fromisoformat(row[0]).timestamp()))
        return total

    def get_today_session_count(self):
        today = datetime.now().date().isoformat()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) FROM activity_sessions WHERE date(started_at) = ?",
                (today,),
            ).fetchone()
        return int(row[0] or 0)

    def get_top_app(self):
        today = datetime.now().date().isoformat()
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT app_name, SUM(duration_seconds) AS seconds "
                "FROM activity_sessions WHERE date(started_at) = ? "
                "GROUP BY app_name ORDER BY seconds DESC LIMIT 1",
                (today,),
            ).fetchone()
        return (rows[0], int(rows[1])) if rows else (None, 0)

    def get_recent_apps(self, limit=5):
        with self._connect() as connection:
            return connection.execute(
                "SELECT app_name, SUM(duration_seconds) AS seconds "
                "FROM activity_sessions GROUP BY app_name ORDER BY seconds DESC LIMIT ?",
                (limit,),
            ).fetchall()

    @staticmethod
    def format_duration(seconds):
        seconds = max(0, int(seconds or 0))
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
