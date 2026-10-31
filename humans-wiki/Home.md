# Orbit Translate

A one-shot selection translator for Niri / Wayland. Select text, press the shortcut, read the results under your pointer — the panel closes by itself and nothing keeps running in the background.

[简体中文](Home-zh)

<p align="center">
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/popup-sentence.png" alt="Several channels side by side" width="31%" />
&nbsp;
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/popup-language-menu.png" alt="Target language menu" width="31%" />
&nbsp;
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/popup-dictionary.png" alt="Word lookup with dictionary cards" width="31%" />
</p>

## Install

Runtime dependencies (Arch-based):

```bash
sudo pacman -S --needed python-gobject gtk3 gtk-layer-shell wl-clipboard
```

- **Nyxuri users**: already installed with the Noctalia plugin; press `Alt + E`. Channel settings: Orbit › System Tools › Translate.
- **Standalone**:

  ```bash
  git clone --depth 1 https://github.com/WALKERKILLER/orbit-translate.git ~/orbit-translate
  cd ~/orbit-translate && ./install.sh
  ```

  Then bind the entry in Niri:

  ```kdl
  binds {
      Alt+E repeat=false hotkey-overlay-title="Translate selection" {
          spawn "~/.config/noctalia/tools/orbit-translate.py"
      }
  }
  ```

## Files

| Path | What it is |
| --- | --- |
| `~/.config/noctalia/tools/orbit-translate.py` | Entry |
| `~/.config/noctalia/tools/orbit_translate/` | Program files (refreshed by `install.sh`) |
| `~/.config/noctalia/tools/orbit-translate__custom__.toml` | Your config (never overwritten) |
| `~/.cache/orbit-translate/models-dev-v1.json.gz` | Public models.dev catalog, only after pressing `m` in settings |

`./install.sh --uninstall` removes the program files and keeps your config. Delete the TOML and the cache directory yourself if you want nothing left.

## Using the Panel

| Action | How |
| --- | --- |
| Swap languages | Middle button between the two language chips |
| Pick a language | Click a chip; the menu opens below it |
| Copy a result | Copy button on the card header |
| Move / resize | `Super + left drag` / `Super + right drag` |
| Close | `Esc` (closes an open language menu first), or wait for the idle timer |

The idle timer only starts after all channels finish and pauses while your pointer rests on the panel, while selecting, scrolling or dragging.

Next: [Configuration](Configuration) · [Troubleshooting](Troubleshooting)
