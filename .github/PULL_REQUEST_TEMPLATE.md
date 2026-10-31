## 改动说明

<!-- 一句话说清改了什么、为什么 -->

## 验证

- [ ] `python3 -m compileall -q orbit_translate orbit-translate.py tests` + `shellcheck install.sh`
- [ ] `/usr/bin/python3 -m unittest discover -s tests -t .`
- [ ] 涉及浮窗渲染：`ORBIT_GTK_ACCEPTANCE=1 /usr/bin/python3 -m unittest tests.tui.test_translate_popup_native`

## 注意

- **禁止添加 `Co-authored-by: Claude` 署名**。GitHub 会把 Claude 计入仓库 Contributors 列表。用 Claude 辅助没问题，但提交归你本人——不要让它在贡献者里露脸。
- 部署目录、入口名、包名与 `orbit-translate__custom__.toml` 是 Nyxuri 的消费契约，改动前先更新 `llms-wiki/nyxuri-integration.md`。
- TOML 不得出现明文 `api_key`；测试一律使用 `tests/utils.py:TempEnv`，网络请求一律 mock。
- 涉及 CLI、配置格式或渠道协议变动时，同步更新 `llms-wiki/` 对应页与 `CHANGELOG.md`。
