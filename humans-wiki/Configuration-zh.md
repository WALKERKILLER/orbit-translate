# 配置手册

配置文件：`~/.config/noctalia/tools/orbit-translate__custom__.toml`。最省事的方式是打开设置界面：

```bash
~/.config/noctalia/tools/orbit-translate.py --settings
```

[English](Configuration)

## 设置界面

<p align="center">
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/tui-main.png" alt="渠道设置 TUI" width="62%" />
&nbsp;
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/tui-add.png" alt="AI 协议选择" width="34%" />
</p>

| 按键 | 用途 |
| --- | --- |
| `↑ ↓` / `j k` | 选择渠道 |
| `空格` | 开关渠道 |
| `a` | 添加 AI 渠道（选择协议） |
| `m` | 从 models.dev 搜索提供商与文本模型 |
| `e` / `Enter` | 编辑选中渠道 |
| `K` | 脱敏输入 API Key 并存入系统钥匙串 |
| `t` | 用示例文本测试选中渠道 |
| `d` | 确认后移除渠道 |
| `s` | 保存——按之前什么都不写 |
| `Tab` / `Shift-Tab` | 在列表与操作栏之间切换焦点 |
| `?` | 帮助 |
| `q` / `Esc` | 退出（有未保存改动时先确认） |

保存前走和浮窗同一套校验，先写 `0600` 备份再原子替换。如果别的程序同时改了文件，保存会停下来，不会覆盖对方。`--settings --config PATH` 编辑另一个文件，不碰默认配置。

## 根级键

| 键 | 默认值 | 范围 / 含义 |
| --- | --- | --- |
| `source` | `"auto"` | 源语言码（MyMemory 需要明确语言码） |
| `target` | `"zh-CN"` | 目标语言码 |
| `capture_primary` | `true` | 读取 Wayland PRIMARY 选区 |
| `capture_timeout_ms` | `350` | 100 – 5000 |
| `request_timeout_ms` | `6000` | 500 – 120000，单渠道 |
| `max_chars` | `8000` | 1 – 50000，超出截断 |
| `max_parallel` | `8` | 1 – 16 并发请求 |
| `max_cards` | `4` | 1 – 16 张结果卡片 |
| `dismiss_after_ms` | `12000` | 1000 – 120000，闲置多久后关闭 |
| `show_source` | `true` | 显示原文区 |
| `auto_copy` | `false` | 自动复制第一条译文 |

仓库附带的模板是免费预设：只开 MyMemory，`en → zh-CN`。

## 渠道

每个渠道是一个 `[[providers]]`，包含 `id`、`name`、`type`、`enabled` 和类型专属字段。

| 类别 | `type` |
| --- | --- |
| 免费 / 公共接口 | `mymemory` `google` `deepl` `bing` `lingva` `yandex` `transmart` |
| 词典 / 例句 | `ecdict` `bing_dict` `cambridge_dict` `tatoeba`（只接短词组：≤4 词、≤48 字符） |
| 自建 | `libretranslate` |
| AI | `openai_compatible` `openai_responses` `anthropic` `gemini` `ollama` |
| 本地命令 | `command`（参数数组，不经过 shell） |

公共接口随时可能限流或下线；`base_url` 可以换成兼容镜像。

### AI 协议

| 协议 | `type` | 基础地址示例 |
| --- | --- | --- |
| OpenAI Chat Completions / 兼容网关 | `openai_compatible` | `https://api.openai.com/v1` |
| OpenAI Responses | `openai_responses` | `https://api.openai.com/v1` |
| Anthropic Messages | `anthropic` | `https://api.anthropic.com/v1` |
| Gemini GenerateContent | `gemini` | `https://generativelanguage.googleapis.com/v1beta` |
| Ollama 本地 | `ollama` | `http://127.0.0.1:11434` |

基础地址包含 API 版本目录，不含最终方法路径。在线 AI 通常收费，示例测试也会真的发一次请求。

## API Key

TOML 里写明文 `api_key` 会被拒绝。二选一：

- `api_key_env = "OPENAI_API_KEY"`——从快捷键启动的进程环境里读。
- 在设置界面按 `K`——Key 经 stdin 写进 KWallet（`kwallet-query`）或 Secret Service（`secret-tool`），TOML 只留 `api_key_secret` 引用。

没有可用钥匙串时安全失败，绝不降级为明文文件。移除渠道不会悄悄删掉钥匙串里的 Key。

## 调色

浮窗和设置界面依次读取 `~/.cache/nyxuri/palette.toml` → `nyxniri/palette.toml` → `noctalia/starship-palette.toml` → 内置色。`NO_COLOR=1` 时终端界面只用文字和边框表达层级。
