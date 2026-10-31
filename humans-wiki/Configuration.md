# Configuration

Config file: `~/.config/noctalia/tools/orbit-translate__custom__.toml`. The easiest way to edit it is the settings UI:

```bash
~/.config/noctalia/tools/orbit-translate.py --settings
```

[简体中文](Configuration-zh)

## Settings UI

| Key | Action |
| --- | --- |
| `↑ ↓` / `j k` | Select a channel |
| `Space` | Enable / disable |
| `a` | Add an AI channel (pick a protocol) |
| `m` | Search models.dev for a provider and text model |
| `e` / `Enter` | Edit the selected channel |
| `K` | Store an API key in the system keyring (masked input) |
| `t` | Run a sample translation against the selected channel |
| `d` | Remove the channel (with confirmation) |
| `s` | Save — nothing is written before this |
| `Tab` / `Shift-Tab` | Move focus between the list and the action bar |
| `?` | Help |
| `q` / `Esc` | Quit (asks before discarding unsaved changes) |

Saving runs the same validation as the panel, writes a `0600` backup, then replaces the file atomically. If another program changed the file meanwhile, saving stops instead of overwriting it. `--settings --config PATH` edits a different file without touching your default config.

## Top-level Keys

| Key | Default | Range / meaning |
| --- | --- | --- |
| `source` | `"auto"` | Source language code (MyMemory needs an explicit code) |
| `target` | `"zh-CN"` | Target language code |
| `capture_primary` | `true` | Read the Wayland PRIMARY selection |
| `capture_timeout_ms` | `350` | 100 – 5000 |
| `request_timeout_ms` | `6000` | 500 – 120000, per channel |
| `max_chars` | `8000` | 1 – 50000, longer selections are cut |
| `max_parallel` | `8` | 1 – 16 concurrent requests |
| `max_cards` | `4` | 1 – 16 result cards |
| `dismiss_after_ms` | `12000` | 1000 – 120000 idle time before closing |
| `show_source` | `true` | Show the source text area |
| `auto_copy` | `false` | Copy the first result automatically |

The shipped template is the free preset: only MyMemory is on, `en → zh-CN`.

## Channels

Each channel is a `[[providers]]` entry with `id`, `name`, `type`, `enabled` plus type-specific fields.

| Kind | `type` |
| --- | --- |
| Free / public | `mymemory` `google` `deepl` `bing` `lingva` `yandex` `transmart` |
| Dictionary / examples | `ecdict` `bing_dict` `cambridge_dict` `tatoeba` (short phrases only: ≤4 words, ≤48 chars) |
| Self-hosted | `libretranslate` |
| AI | `openai_compatible` `openai_responses` `anthropic` `gemini` `ollama` |
| Local command | `command` (argument array, never through a shell) |

Public endpoints can rate-limit or disappear without notice; `base_url` lets you point at a compatible mirror.

### AI Protocols

| Protocol | `type` | Base URL example |
| --- | --- | --- |
| OpenAI Chat Completions / compatible gateway | `openai_compatible` | `https://api.openai.com/v1` |
| OpenAI Responses | `openai_responses` | `https://api.openai.com/v1` |
| Anthropic Messages | `anthropic` | `https://api.anthropic.com/v1` |
| Gemini GenerateContent | `gemini` | `https://generativelanguage.googleapis.com/v1beta` |
| Ollama (local) | `ollama` | `http://127.0.0.1:11434` |

The base URL includes the API version directory but not the final method path. Online AI usually costs money, and the sample test sends a real request.

## API Keys

A plain `api_key` in the TOML is rejected. Pick one:

- `api_key_env = "OPENAI_API_KEY"` — read from the environment of the process started by your shortcut.
- Press `K` in the settings UI — the key goes to KWallet (`kwallet-query`) or Secret Service (`secret-tool`) through stdin, and the TOML only keeps an `api_key_secret` reference.

If no keyring is available, it fails safely; it never falls back to a plain-text file. Removing a channel does not silently delete its key from the keyring.

## Palette

The panel and the settings UI read `~/.cache/nyxuri/palette.toml`, then `nyxniri/palette.toml`, then `noctalia/starship-palette.toml`, then built-in colors. `NO_COLOR=1` makes the terminal UI use text and borders only.
