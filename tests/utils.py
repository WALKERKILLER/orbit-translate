"""Shared test utilities: environment isolation under a temporary HOME.

Design principle: tests must NEVER touch the real ~/.config, ~/.local, or ~/.cache.
"""

import os
import tempfile
from pathlib import Path

_KEYS = ("HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME", "WAYLAND_DISPLAY")


class TempEnv:
    """Context manager that points HOME and the XDG base dirs at a temp tree."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        self._old_env = {}

    def __enter__(self):
        home = self.home
        for relative in (".config", ".cache", ".local/state", ".local/share"):
            (home / relative).mkdir(parents=True, exist_ok=True)
        self._old_env = {key: os.environ.get(key) for key in _KEYS}
        os.environ.pop("WAYLAND_DISPLAY", None)
        os.environ["HOME"] = str(home)
        os.environ["XDG_CONFIG_HOME"] = str(home / ".config")
        os.environ["XDG_CACHE_HOME"] = str(home / ".cache")
        os.environ["XDG_STATE_HOME"] = str(home / ".local" / "state")
        os.environ["XDG_DATA_HOME"] = str(home / ".local" / "share")
        return self

    def __exit__(self, *exc):
        for key, value in self._old_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self._tmp.cleanup()
        return False


PRESENTATION_TIMEOUT_SCALE = 1.0


def presentation_timeout_scale():
    """Multiplier for presentation budgets, for hardware slower than CI."""
    raw = os.environ.get("ORBIT_PRESENTATION_TIMEOUT_SCALE", "").strip()
    try:
        value = float(raw) if raw else 0.0
    except ValueError:
        value = 0.0
    return value if value >= 1 else PRESENTATION_TIMEOUT_SCALE


def presentation_budget(seconds):
    return seconds * presentation_timeout_scale()
