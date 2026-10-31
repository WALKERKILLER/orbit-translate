# 故障排除指南

先跑依赖检查，它不会开窗口：

```bash
~/.config/noctalia/tools/orbit-translate.py --check-deps
```

[English](Troubleshooting)

## “没有读取到选中文本”

工具读的是 Wayland **PRIMARY** 选区（`wl-paste --primary`），不是普通剪贴板。

- 看看应用到底给了什么：选中一段文字，再运行 `wl-paste --primary --no-newline`。
- 有些应用只写普通剪贴板，PDF 阅读器最常见——在 [TRACKING_ISSUE](TRACKING_URL) 跟踪（由 [Nyxuri#142](https://github.com/ech678/Nyxuri/issues/142) 迁来）。
- `capture_primary = false` 会彻底关闭捕获，改回 `true`。

## 没有结果

- 至少要启用一个渠道。免费预设只开 MyMemory，它要求 `source` 写明确语言码（不能是 `auto`），单次最多 500 UTF-8 bytes。
- 公共接口可能限流，或在你的网络里不可达。在 `--settings` 里对该渠道按 `t`——测试只显示本地错误分类，不显示原始响应。
- AI 渠道：检查基础地址（含版本目录、不含方法路径）、模型名，以及 Key 是否可达（`api_key_env` 指向的变量要存在于快捷键启动的进程环境里）。
- 词典和例句渠道会故意跳过长句。

## 浮窗起不来

- 必须在 Niri 的 Wayland 会话里，并装好 `gtk-layer-shell`。
- 入口运行 `PATH` 里第一个 `python3`（`#!/usr/bin/env python3`）。虚拟环境或 pyenv 的 `python3` 通常没有 PyGObject——用 `/usr/bin/python3 ~/.config/noctalia/tools/orbit-translate.py --check-deps` 确认。
- TOML 写坏了会提示“配置错误”和文件名。修好它，或者用 `--settings`，它不会保存无效配置。

## 钥匙串报错

`K` 需要 `kwallet-query`（KDE）或 `secret-tool`（libsecret）。第一次存储可能弹出钱包解锁或创建提示，要你自己完成。没有钥匙串时改用 `api_key_env`。

## 反馈问题

提交 [错误报告](https://github.com/WALKERKILLER/orbit-translate/issues/new/choose)，附上 `--check-deps` 输出、发行版和复现步骤。不要贴 API Key。
