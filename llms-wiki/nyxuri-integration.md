# Nyxuri Integration — 上游仓库与消费方边界

> 本页是 Orbit Translate 与 Nyxuri 之间的接口契约，以本仓库源码与 Nyxuri 的契约测试为准。
> 来源：Nyxuri ROADMAP R0-5「减法外迁」——`orbit_translate` 从 `plugins/noctalia/tools/` 外迁为独立上游仓库，
> 先例为 key-cli → Clavis；[ech678/Nyxuri#142](https://github.com/ech678/Nyxuri/issues/142) 随迁到本仓库跟踪。

## 本仓库负责

- 程序本体：`orbit-translate.py` + `orbit_translate/`，零常驻、纯标准库 + GTK3/GtkLayerShell。
- 用户配置模板：`config/orbit-translate__custom__.toml`（免费预设）。
- 运行时契约（见 [orbit-translate](orbit-translate.md)）：CLI、配置格式、渠道协议、凭据边界、调色加载顺序。
- 单测与安装器：`tests/`、`install.sh`。

## Nyxuri 负责

| 契约 | Nyxuri 位置 | 说明 |
|---|---|---|
| 部署位置 | `~/.config/noctalia/tools/` | 入口、包与 Dunder 配置同目录；`config_path()` 依赖这一位置 |
| 选区快捷键 | `plugins/niri/binds.kdl` → `shell-action.sh translate` | `Alt+E repeat=false`，网关在自研 Shell 下转交 `--action` |
| 设置入口 | Orbit `System Tools › Translate`（`cmd = "translate"`）→ `niri-scratch-toggle.sh translate` | Scratchpad Kitty 中运行 `orbit-translate.py --settings` |
| 包声明 | `plugins/noctalia/manifest.toml` | `python-gobject`、`gtk-layer-shell`、`wl-clipboard` |
| 调色事实源 | `~/.cache/nyxuri/palette.toml` | 本仓库只读；缺失时回退 `nyxniri/` → `noctalia/starship-palette.toml` → 内置色 |

上面这些消费方契约原先由 Nyxuri 的 `test_translate_integration.py` 一并固定（Orbit 菜单项、`Alt+E` 绑定、
manifest 包声明）。外迁后它们只验证 Nyxuri 自己的文件，应留在 Nyxuri 测试里；本仓库只保留调色与模板契约。

## 不变量

1. **路径不漂移**：入口名、包名、配置文件名与部署目录保持与外迁前一致，Nyxuri 切换来源时不改 KDL、菜单或脚本。
2. **不写真实家目录**：本仓库测试一律走 `tests/utils.py:TempEnv`。
3. **单向依赖**：本仓库不 import `nyxuri`，也不读 Nyxuri 仓库文件；Nyxuri 只把本仓库当文件来源。
4. **用户配置主权**：任何安装或更新路径都不覆盖已存在的 `orbit-translate__custom__.toml`。

## 版本与来源

Nyxuri 侧应按 tag 或固定 commit 拉取本仓库，避免跟随 `main` 漂移。外迁保留了原路径
（`configs/` → `units/` → `plugins/noctalia/tools/`）上的全部提交历史与作者信息。
