# Orbit Translate

Niri / Wayland 上的一次性划词翻译。选中文字、按快捷键、在指针下方看译文——浮窗自己关掉，后台什么都不留。

[English](Home)

<p align="center">
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/popup-sentence.png" alt="多渠道并行译文" width="31%" />
&nbsp;
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/popup-language-menu.png" alt="目标语言菜单" width="31%" />
&nbsp;
<img src="https://raw.githubusercontent.com/WALKERKILLER/orbit-translate/main/assets/screenshots/popup-dictionary.png" alt="单词查询：译文 + 词典卡片" width="31%" />
</p>

## 安装

运行依赖（Arch 系）：

```bash
sudo pacman -S --needed python-gobject gtk3 gtk-layer-shell wl-clipboard
```

- **Nyxuri 用户**：启用 Noctalia 插件就已经装好了，按 `Alt + E`。渠道设置在 Orbit › System Tools › Translate。
- **独立安装**：

  ```bash
  git clone --depth 1 https://github.com/WALKERKILLER/orbit-translate.git ~/orbit-translate
  cd ~/orbit-translate && ./install.sh
  ```

  然后在 Niri 里绑定入口：

  ```kdl
  binds {
      Alt+E repeat=false hotkey-overlay-title="Translate selection" {
          spawn "~/.config/noctalia/tools/orbit-translate.py"
      }
  }
  ```

## 文件位置

| 路径 | 是什么 |
| --- | --- |
| `~/.config/noctalia/tools/orbit-translate.py` | 入口 |
| `~/.config/noctalia/tools/orbit_translate/` | 程序文件（`install.sh` 会刷新） |
| `~/.config/noctalia/tools/orbit-translate__custom__.toml` | 你的配置（永不覆盖） |
| `~/.cache/orbit-translate/models-dev-v1.json.gz` | models.dev 公共目录，只在设置里按 `m` 后才有 |

`./install.sh --uninstall` 删除程序文件、保留配置。想一点不剩，再手动删掉 TOML 和缓存目录。

## 浮窗操作

| 动作 | 方法 |
| --- | --- |
| 交换语言 | 两个语言胶囊中间的按钮 |
| 选择语言 | 点击胶囊，菜单在下方展开 |
| 复制译文 | 卡片标题行的复制按钮 |
| 移动 / 缩放 | `Super + 左键拖动` / `Super + 右键拖动` |
| 关闭 | `Esc`（先关语言菜单），或等闲置倒计时 |

闲置倒计时在所有渠道完成后才开始；鼠标停留、选文字、滚动或拖动时暂停。

下一步：[配置手册](Configuration-zh) · [故障排除](Troubleshooting-zh)
