# Changelog

此文件记录 Orbit Translate 每个版本中用户可感知的重要变化。

格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [Unreleased]

### Added
- 从 Nyxuri 外迁为独立仓库（Nyxuri ROADMAP R0-5）：保留 `configs/` → `units/` → `plugins/noctalia/tools/` 路径上的完整提交历史与作者
- `install.sh`：不依赖 Nyxuri 的独立安装，目标与 Nyxuri 部署位置相同（`~/.config/noctalia/tools/`）；只在缺失时复制配置模板，`--uninstall` 保留用户配置
- 双语 README、用户 Wiki（`humans-wiki/`，自动同步到 GitHub Wiki）与架构契约（`llms-wiki/`）
- CI：Python 3.11 – 3.15 单测矩阵、Arch 系统 GTK3 + GtkLayerShell 全量单测、ShellCheck 与文档门禁

### Changed
- 测试与 Nyxuri 解耦：本仓库自带 `tests/utils.py:TempEnv`；PTY 等待时限的倍率变量改名 `ORBIT_PRESENTATION_TIMEOUT_SCALE`
- Nyxuri 侧的接线契约（`Alt+E` 绑定、Orbit 菜单项、manifest 包声明）留在 Nyxuri 测试中，本仓库只保留调色与配置模板契约

[Unreleased]: https://github.com/WALKERKILLER/orbit-translate/commits/main
