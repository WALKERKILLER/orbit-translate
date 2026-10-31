"""Shared harness for the Orbit Translate tests.

The tool ships as plain files (entry orbit-translate.py + package
orbit_translate/), not as an installed distribution, so the repository root
goes on sys.path. Test modules re-export setUpModule/tearDownModule from here:
each module runs inside one TempEnv, so XDG config/cache lookups never reach
the real ~/.config or ~/.cache.
"""

import sys
from pathlib import Path

from tests.utils import TempEnv

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "orbit-translate.py"
TEMPLATE = ROOT / "config" / "orbit-translate__custom__.toml"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# Tests import the source tree directly; keep it free of __pycache__ residue.
sys.dont_write_bytecode = True

_env = None


def setUpModule():
    global _env
    _env = TempEnv()
    _env.__enter__()


def tearDownModule():
    global _env
    if _env is not None:
        _env.__exit__()
        _env = None
