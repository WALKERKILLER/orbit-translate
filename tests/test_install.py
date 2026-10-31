"""install.sh contract: same target as Nyxuri, user config is never touched."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests.support import ROOT

_INSTALLER = ROOT / "install.sh"
_CONFIG = "orbit-translate__custom__.toml"


@unittest.skipIf(shutil.which("bash") is None or os.geteuid() == 0, "requires bash as a regular user")
class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        self.tools = self.home / ".config" / "noctalia" / "tools"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_installer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(_INSTALLER), *args],
            env={"HOME": str(self.home), "PATH": os.environ.get("PATH", "/usr/bin:/bin")},
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_install_copies_program_files_and_seeds_config_once(self) -> None:
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = self.tools / "orbit-translate.py"
        self.assertTrue(os.access(entry, os.X_OK))
        self.assertTrue((self.tools / "orbit_translate" / "__init__.py").is_file())
        self.assertEqual(
            (self.tools / _CONFIG).read_bytes(),
            (ROOT / "config" / _CONFIG).read_bytes(),
        )
        self.assertFalse(list(self.tools.rglob("__pycache__")))
        self.assertEqual({path.name for path in self.tools.iterdir()},
                         {_CONFIG, "orbit-translate.py", "orbit_translate"})

    def test_reinstall_refreshes_program_but_keeps_user_config(self) -> None:
        self.assertEqual(self.run_installer().returncode, 0)
        (self.tools / _CONFIG).write_text('source = "ja"\n', encoding="utf-8")
        stale = self.tools / "orbit_translate" / "stale.py"
        stale.write_text("", encoding="utf-8")
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.tools / _CONFIG).read_text(encoding="utf-8"), 'source = "ja"\n')
        self.assertFalse(stale.exists())
        self.assertNotIn("Created user config", result.stdout)

    def test_uninstall_removes_program_files_only(self) -> None:
        self.assertEqual(self.run_installer().returncode, 0)
        result = self.run_installer("--uninstall")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([path.name for path in self.tools.iterdir()], [_CONFIG])

    def test_unknown_argument_is_rejected(self) -> None:
        result = self.run_installer("--bogus")
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.tools.exists())


if __name__ == "__main__":
    unittest.main()
