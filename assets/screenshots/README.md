# Screenshots

README 与 Wiki 使用的效果图。全部使用固定示例数据离线渲染，配色为同一套 Nyxuri Material You 色板，2× 缩放。

| 文件 | 来源 |
| --- | --- |
| `popup-sentence.png` `popup-language-menu.png` `popup-dictionary.png` | `python3 scripts/render_screenshots.py` 生成：真实 `TranslationWindow` 在 Xvfb 中绘制导出，渠道请求为 fixture，不联网。浮窗外观变动后重新生成 |
| `tui-main.png` `tui-add.png` | 设置 TUI 在 tmux 中真实运行后的终端画面栅格化，来自 PR [ech678/Nyxuri#122](https://github.com/ech678/Nyxuri/pull/122)；TUI 外观变动后需重新截取 |
