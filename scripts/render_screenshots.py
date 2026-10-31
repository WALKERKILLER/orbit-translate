#!/usr/bin/env python3
"""Render the popup screenshots in assets/screenshots/ from fixture data.

    python3 scripts/render_screenshots.py [OUTPUT_DIR]

Runs the real TranslationWindow under a private Xvfb display (needs xvfb-run,
the GTK runtime, and the adw-gtk3 theme, breeze icons and Noto Sans fonts for an
exact match). No network, no real HOME: palette and GTK settings are fixtures
below. Layer shell is unavailable on X11, so its warnings are expected. The TUI
shots (tui-*.png) are terminal captures and are not produced here.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

# Nyxuri Material You palette the gallery was shot with (~/.cache/nyxuri/palette.toml).
PALETTE = """\
primary = "#4ed8e8"
on_primary = "#00363c"
primary_container = "#004f56"
on_primary_container = "#8df2ff"
secondary = "#81d3de"
on_secondary = "#00363c"
secondary_container = "#004f56"
on_secondary_container = "#9df0fb"
tertiary = "#a4c9fe"
on_tertiary = "#00315c"
tertiary_container = "#1f4876"
on_tertiary_container = "#d3e3ff"
error = "#ffb4ab"
on_error = "#690005"
error_container = "#93000a"
on_error_container = "#ffdad6"
background = "#0e141c"
on_background = "#dee2ee"
surface = "#0e141c"
on_surface = "#dee2ee"
surface_dim = "#0e141c"
surface_bright = "#343943"
surface_variant = "#3c4758"
on_surface_variant = "#bcc7db"
surface_container_lowest = "#090e16"
surface_container_low = "#161c24"
surface_container = "#1a2028"
surface_container_high = "#252a33"
surface_container_highest = "#2f353e"
outline = "#8691a4"
outline_variant = "#3c4758"
shadow = "#000000"
"""
GTK_SETTINGS = """\
[Settings]
gtk-application-prefer-dark-theme = true
gtk-theme-name = adw-gtk3-dark
gtk-icon-theme-name = breeze-dark
gtk-font-name = Noto Sans, 10
"""

SCALE = 2
MARGIN = (89, 78, 89, 107)  # left, top, right, bottom in output pixels
# Same backdrop as the TUI shots: surface_container_lowest fading diagonally
# into a deep teal, t = 0.35 * x / W + 0.65 * y / H.
BACKDROP_FROM = (0x09, 0x0E, 0x16)
BACKDROP_TO = (0x04, 0x32, 0x3A)


def launch(output: Path) -> int:
    if shutil.which("xvfb-run") is None:
        print("render_screenshots.py needs xvfb-run (xorg-server-xvfb).", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as temporary:
        home = Path(temporary)
        (home / ".cache" / "nyxuri").mkdir(parents=True)
        (home / ".cache" / "nyxuri" / "palette.toml").write_text(PALETTE, encoding="utf-8")
        (home / ".config" / "gtk-3.0").mkdir(parents=True)
        (home / ".config" / "gtk-3.0" / "settings.ini").write_text(GTK_SETTINGS, encoding="utf-8")
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "LANG": "zh_CN.UTF-8",
            "GDK_BACKEND": "x11",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        command = ["xvfb-run", "-a", "-s", "-screen 0 1920x1440x24",
                   sys.executable, str(Path(__file__).resolve()), "--child", str(output)]
        return subprocess.run(command, env=env, check=False, timeout=120).returncode


def render(output: Path) -> None:
    sys.path.insert(0, str(ROOT))
    sys.dont_write_bytecode = True
    from unittest.mock import patch

    import cairo

    from orbit_translate.config import parse_config
    from orbit_translate.providers import (
        ProviderOutcome,
        extract_bing_dictionary_text,
        extract_cambridge_dictionary_text,
    )
    from orbit_translate.ui import GLib, TranslationWindow

    def pump(seconds: float) -> None:
        deadline = time.monotonic() + seconds
        context = GLib.MainContext.default()
        while time.monotonic() < deadline:
            while context.pending():
                context.iteration(False)
            time.sleep(0.002)

    def window_for(text: str, providers: list[tuple[str, str, str]]) -> TranslationWindow:
        config = parse_config({
            "source": "en", "target": "zh-CN", "dismiss_after_ms": 120000, "max_cards": 4,
            "providers": [{"id": i, "name": n, "type": t, "enabled": True} for i, n, t in providers],
        })
        window = TranslationWindow(config, text)
        # X11 has no layer shell: give the window the fullscreen extent it has on
        # niri, so the panel's CSS shadow is not clipped by the window edge.
        window.set_size_request(1200, 1400)
        window.start()
        pump(0.3)
        window._move_panel(300, 120)
        pump(0.3)
        return window

    def show(window: TranslationWindow, outcomes: list[ProviderOutcome]) -> None:
        for outcome in outcomes:
            window._apply_outcome(outcome, window.translation_generation)
            pump(0.35)
        pump(0.6)

    def snapshot(window: TranslationWindow, name: str) -> None:
        panel = window.panel.get_allocation()
        left, top, right, bottom = MARGIN
        width = panel.width * SCALE + left + right
        height = panel.height * SCALE + top + bottom
        if window.language_menu.is_open():
            menu = window.language_menu.get_allocation()
            height = max(height, (menu.y + menu.height - panel.y) * SCALE + top + bottom)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(surface)
        a, b = 0.35 / width, 0.65 / height
        gradient = cairo.LinearGradient(0, 0, a / (a * a + b * b), b / (a * a + b * b))
        gradient.add_color_stop_rgb(0, *(c / 255 for c in BACKDROP_FROM))
        gradient.add_color_stop_rgb(1, *(c / 255 for c in BACKDROP_TO))
        cr.set_source(gradient)
        cr.paint()
        cr.translate(left, top)
        cr.scale(SCALE, SCALE)
        cr.translate(-panel.x, -panel.y)
        window.fade_surface.draw(cr)
        surface.flush()
        surface.write_to_png(str(output / f"{name}.png"))
        print(f"{name}.png {width}x{height}")

    engine = patch("orbit_translate.ui.ProviderEngine").start().return_value
    engine.start.return_value = engine
    patch.object(TranslationWindow, "_get_pointer_position", return_value=None).start()
    patch.object(TranslationWindow, "_set_clipboard", return_value=True).start()

    window = window_for(
        "Orbit Translate reads the Wayland primary selection, asks several "
        "channels at once, and quietly exits when you are done reading.",
        [("deepl", "DeepL", "deepl"), ("yandex", "Yandex", "yandex"), ("mymemory", "MyMemory", "mymemory")],
    )
    show(window, [
        ProviderOutcome("deepl", "DeepL", text="Orbit Translate 读取 Wayland 主选区，同时询问多个渠道，并在你读完后悄然退出。"),
        ProviderOutcome("yandex", "Yandex", text="Orbit Translate 会读取 Wayland 主选择内容，同时向多个渠道发出请求，在你阅读完毕后安静地退出。"),
        ProviderOutcome("mymemory", "MyMemory", text="Orbit Translate 读取 Wayland 的主要选区，一次询问多个渠道，并在您阅读完毕后悄悄退出。"),
    ])
    snapshot(window, "popup-sentence")
    window.target_selector.clicked()
    pump(0.6)
    snapshot(window, "popup-language-menu")
    window.destroy()
    pump(0.1)

    bing = extract_bing_dictionary_text({"value": [{"meaningGroups": [
        {"partsOfSpeech": [{"description": "发音", "name": name}],
         "meanings": [{"richDefinitions": [{"fragments": [{"text": "/ˌserənˈdɪpəti/"}]}]}]}
        for name in ("美式", "英式")
    ] + [
        {"partsOfSpeech": [{"description": "快速释义", "name": "名词"}],
         "meanings": [{"richDefinitions": [{"fragments": [{"text": "意外发现珍奇事物的本领；机缘巧合"}]}]}]},
        {"partsOfSpeech": [{"description": "变形", "name": "复数"}],
         "meanings": [{"richDefinitions": [{"fragments": [{"text": "serendipities"}]}]}]},
    ]}]})
    cambridge = extract_cambridge_dictionary_text(
        '<div class="pr entry-body__el"><span class="region">UK</span><span class="pron">/ˌser.ənˈdɪp.ə.ti/</span>'
        '<span class="posgram">noun</span><span class="dtrans-se">意外发现珍奇事物的运气；机缘凑巧</span>'
        '<span class="eg">Finding that book was pure serendipity.</span><span class="trans">找到那本书纯属机缘巧合。</span></div>'
    )
    window = window_for("serendipity", [
        ("deepl", "DeepL", "deepl"), ("bing-dict", "Bing 词典", "bing_dict"), ("cambridge-dict", "剑桥词典", "cambridge_dict"),
    ])
    show(window, [
        ProviderOutcome("deepl", "DeepL", text="机缘巧合"),
        ProviderOutcome("bing-dict", "Bing 词典", text=bing),
        ProviderOutcome("cambridge-dict", "剑桥词典", text=cambridge),
    ])
    snapshot(window, "popup-dictionary")
    window.destroy()
    pump(0.1)


def main(argv: list[str]) -> int:
    if argv[:1] == ["--child"]:
        render(Path(argv[1]))
        return 0
    output = Path(argv[0]) if argv else ROOT / "assets" / "screenshots"
    output.mkdir(parents=True, exist_ok=True)
    return launch(output.resolve())


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
