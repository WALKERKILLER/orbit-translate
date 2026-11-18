"""Clipboard capture (--clipboard): argv shapes, secret skipping, and entry routing."""

from __future__ import annotations

from tests.support import ENTRY, setUpModule, tearDownModule  # noqa: F401

import importlib.util
import subprocess
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from orbit_translate.capture import SECRET_HINT_TYPE, CaptureError, capture_clipboard
from orbit_translate.config import parse_config


def _runner(*responses):
    """Fake subprocess.run answering successive calls; records argv and timeout."""
    calls = []
    queue = list(responses)

    def run(args, **kwargs):
        calls.append((args, kwargs))
        returncode, stdout = queue.pop(0)
        return SimpleNamespace(returncode=returncode, stdout=stdout)

    return run, calls


class ClipboardCaptureTests(unittest.TestCase):
    def test_lists_types_then_reads_plain_text_by_type(self) -> None:
        run, calls = _runner((0, b"text/html\ntext/plain;charset=utf-8\ntext/plain\n"), (0, b"  PDF paragraph \n"))
        self.assertEqual(capture_clipboard(350, 400, runner=run), "PDF paragraph")
        self.assertEqual([args for args, _ in calls], [
            ["wl-paste", "--list-types"],
            ["wl-paste", "--no-newline", "--type", "text/plain;charset=utf-8"],
        ])
        for _, kwargs in calls:
            self.assertEqual((kwargs["capture_output"], kwargs["check"]), (True, False))
            self.assertGreater(kwargs["timeout"], 0)
            self.assertLessEqual(kwargs["timeout"], 0.35)

    def test_legacy_text_type_is_accepted(self) -> None:
        run, calls = _runner((0, b"UTF8_STRING\nSTRING\n"), (0, b"hello"))
        self.assertEqual(capture_clipboard(350, 400, runner=run), "hello")
        self.assertEqual(calls[1][0][-1], "UTF8_STRING")

    def test_password_manager_hint_is_skipped_without_reading_the_secret(self) -> None:
        run, calls = _runner((0, f"text/plain\n{SECRET_HINT_TYPE}\n".encode()))
        with self.assertRaises(CaptureError) as raised:
            capture_clipboard(350, 400, runner=run)
        self.assertEqual(raised.exception.category, "secret")
        self.assertEqual(len(calls), 1)

    def test_non_text_clipboard_is_not_translated(self) -> None:
        for listing in (b"image/png\n", b"text/html\ntext/uri-list\n"):
            with self.subTest(listing=listing):
                run, calls = _runner((0, listing))
                with self.assertRaises(CaptureError) as raised:
                    capture_clipboard(350, 400, runner=run)
                self.assertEqual((raised.exception.category, raised.exception.message), ("empty", "剪贴板里没有文本"))
                self.assertEqual(len(calls), 1)

    def test_empty_clipboard(self) -> None:
        run, _ = _runner((1, b""))
        with self.assertRaises(CaptureError) as raised:
            capture_clipboard(350, 400, runner=run)
        self.assertEqual((raised.exception.category, raised.exception.message), ("empty", "剪贴板为空"))
        run, _ = _runner((0, b"text/plain\n"), (0, b" \n"))
        with self.assertRaises(CaptureError) as raised:
            capture_clipboard(350, 400, runner=run)
        self.assertEqual(raised.exception.category, "empty")

    def test_one_deadline_covers_both_calls(self) -> None:
        run, calls = _runner((0, b"text/plain\n"))
        with patch("orbit_translate.capture.time.monotonic", side_effect=[0.0, 0.0, 1.0]), \
                self.assertRaises(CaptureError) as raised:
            capture_clipboard(350, 400, runner=run)
        self.assertEqual((raised.exception.category, raised.exception.message), ("timeout", "读取剪贴板超时"))
        self.assertEqual(len(calls), 1)

    def test_wl_paste_timeout_and_missing_binary(self) -> None:
        def slow(args, **kwargs):
            raise subprocess.TimeoutExpired(args, kwargs["timeout"])

        def missing(args, **kwargs):
            raise FileNotFoundError(args[0])

        with self.assertRaises(CaptureError) as raised:
            capture_clipboard(350, 400, runner=slow)
        self.assertEqual((raised.exception.category, raised.exception.message), ("timeout", "读取剪贴板超时"))
        with self.assertRaises(CaptureError) as raised:
            capture_clipboard(350, 400, runner=missing)
        self.assertEqual(raised.exception.category, "missing_dependency")


class ClipboardEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("orbit_translate_entry_clipboard", ENTRY)
        assert spec and spec.loader
        cls.cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.cli)

    def run_main(self, argv, *, capture_primary=True):
        config = parse_config({"capture_primary": capture_primary, "providers": []})
        ui = ModuleType("orbit_translate.ui")
        ui.show_message = MagicMock()
        error = CaptureError("empty", "fixture stop")
        with patch.dict(sys.modules, {"orbit_translate.ui": ui}), \
                patch.object(self.cli, "load_config", return_value=config), \
                patch.object(self.cli, "capture_clipboard", side_effect=error) as clipboard, \
                patch.object(self.cli, "capture_primary", side_effect=error) as primary:
            code = self.cli.main(argv)
        return code, clipboard, primary, ui.show_message

    def test_clipboard_flag_reads_the_clipboard_only(self) -> None:
        code, clipboard, primary, show = self.run_main(["--clipboard"])
        self.assertEqual(code, 1)
        clipboard.assert_called_once()
        primary.assert_not_called()
        self.assertEqual(show.call_args.args[1], "fixture stop")

    def test_clipboard_flag_is_not_blocked_by_capture_primary_false(self) -> None:
        _, clipboard, _, show = self.run_main(["--clipboard"], capture_primary=False)
        clipboard.assert_called_once()
        self.assertNotEqual(show.call_args.args[1], "已关闭 Primary Selection 捕获")

    def test_default_still_reads_primary(self) -> None:
        _, clipboard, primary, _ = self.run_main([])
        primary.assert_called_once()
        clipboard.assert_not_called()
        _, _, primary, show = self.run_main([], capture_primary=False)
        primary.assert_not_called()
        self.assertEqual(show.call_args.args[1], "已关闭 Primary Selection 捕获")


if __name__ == "__main__":
    unittest.main()
