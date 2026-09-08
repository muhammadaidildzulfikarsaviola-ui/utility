import os
import platform
import time

try:
    import psutil
except ImportError:
    psutil = None


class SystemMonitor:
    """Small cross-platform system information service."""

    @staticmethod
    def cpu_percent():
        if psutil is None:
            return None
        return psutil.cpu_percent(interval=None)

    @staticmethod
    def memory_percent():
        if psutil is None:
            return None
        return psutil.virtual_memory().percent

    @staticmethod
    def disk_percent(path=None):
        if psutil is None:
            return None
        path = path or os.path.abspath(os.sep)
        return psutil.disk_usage(path).percent

    @staticmethod
    def uptime_seconds():
        if psutil is None:
            return None
        return max(0, time.time() - psutil.boot_time())

    @staticmethod
    def platform_name():
        return platform.system()
