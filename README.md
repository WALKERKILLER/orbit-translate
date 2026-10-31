<a id="readme-top"></a>

<div align="right">
<strong>English</strong> | <a href="README.zh-CN.md">简体中文</a>
</div>

<div align="center">

<h1>Orbit Translate</h1>

<p><strong>A one-shot selection translator for Niri / Wayland</strong><br />
<sub>Select, press a key, read — then it gets out of your way (ゆっくりしていってね！)</sub></p>

<p>
<a href="https://github.com/WALKERKILLER/orbit-translate/stargazers"><img height="22" src="https://m3-markdown-badges.vercel.app/stars/3/3/WALKERKILLER/orbit-translate" alt="Stars" /></a>
&nbsp;
<a href="https://www.python.org"><img height="22" src="https://ziadoua.github.io/m3-Markdown-Badges/badges/Python/python1.svg" alt="Python" /></a>
&nbsp;
<a href="LICENSE"><img height="22" src="https://ziadoua.github.io/m3-Markdown-Badges/badges/LicenceGPLv3/licencegplv33.svg" alt="GPL-3.0" /></a>
&nbsp;
<a href="https://github.com/WALKERKILLER/orbit-translate/actions/workflows/ci.yml"><img height="22" src="https://github.com/WALKERKILLER/orbit-translate/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
</p>

<p>
<sub><em>Born in <a href="https://github.com/ech678/Nyxuri">Nyxuri</a> · Read the <a href="https://github.com/WALKERKILLER/orbit-translate/wiki/Home">Wiki</a></em></sub>
</p>
<br />

</div>

> **Things to note**: Orbit Translate started as a Noctalia companion tool inside [Nyxuri](https://github.com/ech678/Nyxuri) and moved out into its own repository under Nyxuri roadmap item R0-5. Nyxuri users don't need to change anything — the install location and the shortcut stay the same.

## What is Orbit Translate

Select some text, hit the shortcut, and a small Material 3 tonal panel pops up right under your pointer, asking several translation channels at once. When you're done reading, it closes by itself.

**No daemon, no tray icon, no translation cache.** Every keypress is one short-lived process: read the Wayland PRIMARY selection, query in parallel, show results, exit.

- **Many channels in parallel**: MyMemory, Google, DeepL, Bing, Yandex, Lingva, Tencent TranSmart; ECDICT, Bing / Cambridge dictionaries; Tatoeba examples; plus Ollama, OpenAI / Anthropic / Gemini protocols and self-hosted LibreTranslate. Public endpoints follow Pot's request and parsing rules and stay off by default (except MyMemory) — turn on what you want.
- **Quiet feedback**: only successful cards show up, in stable channel order; failures never flash by, and you only get a single notice if everything fails.
- **Configure in the terminal**: `--settings` opens a `curses` UI — toggle channels, add AI, press `m` to search models.dev, run a sample test, save explicitly.
- **Keys never hit the disk in plain text**: the TOML rejects `api_key`; use an environment variable or a KWallet / Secret Service reference.
- **Follows your wallpaper**: reads Nyxuri's Monet palette, falls back to built-in colors.
- **Small touches**: flips above the pointer when there's no room below; `Super + left drag` moves, `Super + right drag` resizes; it won't close while your pointer is resting on it.

## Installation

Runtime needs Niri, `wl-clipboard`, GTK3, `gtk-layer-shell`, and PyGObject for the system Python (3.11+):

```bash
sudo pacman -S --needed python-gobject gtk3 gtk-layer-shell wl-clipboard
```

### Nyxuri Users

If Nyxuri is installed with the Noctalia plugin enabled, you already have it — press `Alt + E`.

### Standalone

```bash
git clone --depth 1 https://github.com/WALKERKILLER/orbit-translate.git ~/orbit-translate
cd ~/orbit-translate && ./install.sh
```

The program goes to `~/.config/noctalia/tools/`. The first run seeds the free preset config `orbit-translate__custom__.toml`; later runs only refresh program files and never touch your config. `./install.sh --uninstall` removes the program and keeps the config.

Then add a shortcut to your Niri config (for example `~/.config/niri/__custom__.kdl`):

```kdl
binds {
    Alt+E repeat=false hotkey-overlay-title="Translate selection" {
        spawn "~/.config/noctalia/tools/orbit-translate.py"
    }
}
```

## Directory Structure

```text
orbit-translate
├── orbit-translate.py          # Entry: translate selection / --settings / --check-deps
├── orbit_translate/            # The program (stdlib + GTK3 only)
├── config/                     # User config template (free preset)
├── install.sh                  # Standalone install / uninstall
├── tests/                      # Contract tests (core / catalog / tui)
├── llms-wiki/                  # Architecture contracts & design decisions
└── humans-wiki/                # User manual (synced to the GitHub Wiki)
```

## Configuration

```bash
~/.config/noctalia/tools/orbit-translate.py --settings
```

Channel toggles, AI protocols, API keys and the models.dev quick setup all live here. Field reference: [Configuration (Wiki)](https://github.com/WALKERKILLER/orbit-translate/wiki/Configuration).

## Troubleshooting

Start with `~/.config/noctalia/tools/orbit-translate.py --check-deps`. For no selection, no results or a panel that won't open, see the [Troubleshooting Guide (Wiki)](https://github.com/WALKERKILLER/orbit-translate/wiki/Troubleshooting).

## Development

```bash
python3 -m compileall -q orbit_translate orbit-translate.py tests
/usr/bin/python3 -m unittest discover -s tests -t .
shellcheck install.sh
```

Change routing, invariants and the definition of done live in [AGENTS.md](AGENTS.md); runtime contracts in the [llms-wiki](llms-wiki/llms.txt).

## Community

**Contact:** Bug reports at [GitHub Issues](https://github.com/WALKERKILLER/orbit-translate/issues) · The desktop setup lives at [ech678/Nyxuri](https://github.com/ech678/Nyxuri)

**Thanks:**

* [Nyxuri](https://github.com/ech678/Nyxuri) ([@ech678](https://github.com/ech678)) — where this tool was born, and its visual language
* [Pot](https://github.com/pot-app/pot-desktop) — protocol reference for the free channels
* [models.dev](https://github.com/anomalyco/models.dev) — AI provider and model catalog (MIT)

Released under [GPL-3.0](LICENSE).

<p align="right">(<a href="#readme-top">back to top</a>)</p>
