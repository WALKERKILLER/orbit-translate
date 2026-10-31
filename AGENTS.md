# AGENTS.md (这个是给 AI 开发看的，当然你也可以看一下)

## 0. 协作原则

Orbit Translate 是 Nyxuri 外迁出来的小工具：一次快捷键、一个短命进程、用完就走。
极简不是风格是秩序——不加常驻、不加依赖、不留缓存残渣。

- "能跑但脏" vs "慢一点但干净可控"——默认选后者。
- 只动请求范围，不顺手重构无关代码；汇报说重点。

---

## 1. 真值体系与改动路由

- **真值分工**：运行时行为以**源码（`orbit_translate/` + `orbit-translate.py`）与契约测试（`tests/`）**为准；
  架构契约与设计意图以 [llms-wiki/llms.txt](llms-wiki/llms.txt) 为准。
- **改动范围 ➔ 必读契约 ➔ 定向验证**：

| 改动范围 | 必读 | 验证 |
| --- | --- | --- |
| 配置 / 渠道协议 / 凭据 (`config.py`, `providers.py`, `credentials.py`, `engine.py`) | `orbit-translate.md` | `python3 -m unittest discover -s tests/core -t .` |
| models.dev 目录 (`catalog.py`) | `orbit-translate.md`（缓存节） | `python3 -m unittest discover -s tests/catalog -t .` |
| 设置 TUI / 浮窗 (`tui*.py`, `ui.py`, `widgets.py`, `geometry.py`, `theme.py`, `presentation.py`) | `orbit-translate.md` | `/usr/bin/python3 -m unittest discover -s tests/tui -t .` |
| 部署路径 / 配置模板 / 安装器 (`install.sh`, `config/`) | `nyxuri-integration.md` | `python3 -m unittest tests.test_install tests.core.test_translate_integration` + `shellcheck install.sh` |
| 文档 (`*.md`, `llms-wiki/`, `humans-wiki/`) | `llms.txt` | `python3 -m unittest tests.test_docs` |
| CI / 仓库规则 (`.github/`) | 本页第 4 节 | 推送后看 Actions |
| 版本发布 (`CHANGELOG.md`) | Keep a Changelog | `git log <last-tag>..HEAD` 对齐净变更 |

---

## 2. 核心不变量

1. **零常驻**：每次触发一个短生命周期进程；不加 daemon、托盘、翻译缓存或历史记录。
2. **纯标准库**：除系统 PyGObject（GTK3 + GtkLayerShell）外零 pip 依赖；需 Python 3.11+（`tomllib`）。
3. **路径契约**：部署目录 `~/.config/noctalia/tools/`、入口名、包名、`orbit-translate__custom__.toml` 不改名；
   变更必须先改 [nyxuri-integration](llms-wiki/nyxuri-integration.md) 并通知 Nyxuri。
4. **凭据边界**：TOML 拒绝明文 `api_key`；Key 只走环境变量或系统钥匙串，经 stdin 传递，不进 argv / 日志。
5. **用户配置主权**：安装与更新永不覆盖已存在的用户配置。
6. **权限防御**：`install.sh` 拒绝以 root 运行。

---

## 3. 按需验证

- 纯文档：免测直接交付；动到链接或索引时跑 `python3 -m unittest tests.test_docs`。
- 模块代码：按第 1 节路由表定向跑对应测试。
- 全量回归（重大改动或发版前）：
  ```bash
  python3 -m compileall -q orbit_translate orbit-translate.py tests
  /usr/bin/python3 -m unittest discover -s tests -t .
  shellcheck install.sh
  ```
- 真实 GTK surface：`ORBIT_GTK_ACCEPTANCE=1 /usr/bin/python3 -m unittest tests.tui.test_translate_popup_native`。

---

## 4. 协作工作流与完成定义

- **分支**：`main` 受规则集保护——只经 PR 合入、CI 全绿、线性历史、禁止强推与删除。
- **测试规范**：新测试必须使用 `tests/utils.py:TempEnv`，严禁写入真实 `~/.config` / `~/.cache`；
  外部命令必须有参数形状断言；网络请求一律 mock。
- **提交**：Conventional Commits（`feat:` / `fix:` / `docs:` / `test:` / `ci:` / `chore:`），
  正文中文或英文均可；禁止 `Co-authored-by: Claude` 署名。
- **完成检查**：
  1. 定向测试绿；
  2. 改动契约、CLI 或配置格式时，`llms-wiki/` 对应页已同步事实；
  3. 用户可感知的变化记进 `CHANGELOG.md` 的 `[Unreleased]`；
  4. 不主动 commit，除非用户明确要求。
