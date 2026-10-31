# Troubleshooting

Run the dependency check first — it opens no window:

```bash
~/.config/noctalia/tools/orbit-translate.py --check-deps
```

[简体中文](Troubleshooting-zh)

## "No selected text"

The tool reads the Wayland **PRIMARY** selection (`wl-paste --primary`), not the regular clipboard.

- Check what the app actually provides: select something, then run `wl-paste --primary --no-newline`.
- Some apps only fill the regular clipboard. PDF viewers are the usual suspect — tracked in [TRACKING_ISSUE](TRACKING_URL) (moved from [Nyxuri#142](https://github.com/ech678/Nyxuri/issues/142)).
- `capture_primary = false` turns capture off entirely; set it back to `true`.

## No Results

- At least one channel must be enabled. The free preset only enables MyMemory, which needs an explicit `source` (not `auto`) and at most 500 UTF-8 bytes per request.
- Public endpoints may be rate-limited or unreachable from your network. Run `t` on that channel in `--settings` — the test shows a local error category instead of a raw response.
- AI channels: check the base URL (version directory, no method path), the model name, and that the key is reachable (`api_key_env` must exist in the environment of the process your shortcut starts).
- Dictionary and example channels skip long sentences on purpose.

## The Panel Doesn't Open

- You must be in a Wayland session with Niri; `gtk-layer-shell` must be installed.
- The entry runs the first `python3` in `PATH` (`#!/usr/bin/env python3`). A virtualenv or pyenv `python3` usually lacks PyGObject — check with `/usr/bin/python3 ~/.config/noctalia/tools/orbit-translate.py --check-deps`.
- A broken TOML shows "配置错误" (config error) with the file name. Fix it, or open `--settings`, which refuses to save an invalid file.

## Keyring Errors

`K` needs `kwallet-query` (KDE) or `secret-tool` (libsecret). The first store may trigger a wallet unlock or creation prompt — you have to complete it yourself. Without a keyring, use `api_key_env` instead.

## Reporting a Bug

Open a [Bug Report](https://github.com/WALKERKILLER/orbit-translate/issues/new/choose) with the `--check-deps` output, your distro, and the steps. Never paste API keys.
