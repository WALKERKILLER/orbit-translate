"""Wayland PRIMARY Selection and clipboard capture."""

from __future__ import annotations

from dataclasses import dataclass
import subprocess
import time

# Password managers (KeePassXC, wl-copy --sensitive) mark secrets with this
# type. It is checked from the type list, so a secret is never read.
SECRET_HINT_TYPE = "x-kde-passwordManagerHint"
_PLAIN_TEXT_TYPES = ("text/plain;charset=utf-8", "text/plain", "UTF8_STRING", "STRING", "TEXT")


@dataclass(frozen=True)
class CaptureError(Exception):
    category: str
    message: str

    def __str__(self) -> str:
        return self.message


def normalize_text(text: str, max_chars: int) -> str:
    if max_chars < 1:
        raise CaptureError("invalid", "文本长度上限无效")
    normalized = text.strip()
    if not normalized:
        raise CaptureError("empty", "没有读取到选中文本")
    if len(normalized) <= max_chars:
        return normalized
    if max_chars <= 3:
        return normalized[:max_chars]
    return normalized[: max_chars - 3].rstrip() + "..."


def capture_primary(timeout_ms: int, max_chars: int, runner=None) -> str:
    result = _wl_paste(runner, ["wl-paste", "--primary", "--no-newline"], timeout_ms / 1000, "选区")
    if result.returncode != 0:
        raise CaptureError("empty", "当前没有可用的 PRIMARY 选区")
    return normalize_text(_decode(result.stdout, "选区"), max_chars)


def capture_clipboard(timeout_ms: int, max_chars: int, runner=None) -> str:
    """Read the regular clipboard, for apps that never fill PRIMARY (some PDF viewers).

    One deadline covers both wl-paste calls, so the total wait stays within
    capture_timeout_ms.
    """
    deadline = time.monotonic() + timeout_ms / 1000
    listing = _wl_paste(runner, ["wl-paste", "--list-types"], _remaining(deadline), "剪贴板")
    if listing.returncode != 0:
        raise CaptureError("empty", "剪贴板为空")
    types = [line.strip() for line in _decode(listing.stdout, "剪贴板").splitlines() if line.strip()]
    if SECRET_HINT_TYPE in types:
        raise CaptureError("secret", "剪贴板内容被标记为密码，已跳过")
    text_type = next((kind for kind in _PLAIN_TEXT_TYPES if kind in types), None)
    text_type = text_type or next((kind for kind in types if kind.startswith("text/plain")), None)
    if text_type is None:
        raise CaptureError("empty", "剪贴板里没有文本")
    result = _wl_paste(runner, ["wl-paste", "--no-newline", "--type", text_type], _remaining(deadline), "剪贴板")
    if result.returncode != 0:
        raise CaptureError("empty", "剪贴板为空")
    return normalize_text(_decode(result.stdout, "剪贴板"), max_chars)


def _remaining(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise CaptureError("timeout", "读取剪贴板超时")
    return remaining


def _wl_paste(runner, args: list[str], timeout: float, subject: str):
    run = runner or subprocess.run
    try:
        return run(args, capture_output=True, timeout=timeout, check=False)
    except FileNotFoundError as exc:
        raise CaptureError("missing_dependency", "找不到 wl-paste，请安装 wl-clipboard") from exc
    except subprocess.TimeoutExpired as exc:
        raise CaptureError("timeout", f"读取{subject}超时") from exc
    except OSError as exc:
        raise CaptureError("system", f"读取{subject}失败") from exc


def _decode(output: object, subject: str) -> str:
    if isinstance(output, bytes):
        output = output.decode("utf-8", errors="replace")
    if not isinstance(output, str):
        raise CaptureError("invalid", f"{subject}内容格式无效")
    return output
