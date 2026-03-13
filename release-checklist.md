# Release checklist for bear-notes

## 发布前检查

- [ ] README 已说明用途、安装、目录结构、脚本用法
- [ ] LICENSE 已添加
- [ ] config.example.json 不含私有路径和隐私信息
- [ ] 脚本中无硬编码个人目录、账号、隐私标签
- [ ] 示例 prompt 不暴露个人数据
- [ ] 如果包含 Bear 自动化，注明 macOS / Bear 环境依赖
- [ ] 明确哪些能力是稳定的，哪些仍是实验性能力
- [ ] 若公开发布，最好补一个截图或 demo GIF

## 仓库设置建议

- [ ] 仓库名称明确，例如 `bear-notes-skill` 或 `openclaw-bear-notes`
- [ ] 仓库描述一句话讲清用途
- [ ] 默认分支 README 可直接看懂
- [ ] 添加 topics：`bear` `notes` `openclaw` `skills` `macos` `applescript`

## 身份与署名

- [ ] 确认是否使用主账号发布
- [ ] 或使用单独品牌号 / 小号发布
- [ ] 检查 git user.name
- [ ] 检查 git user.email
- [ ] 如需公开邮箱保护，使用 GitHub noreply 邮箱

## 首发后

- [ ] 补 issue template（可选）
- [ ] 补 roadmap（可选）
- [ ] 标注当前限制：追加逻辑依赖 UI 自动化，可能受系统语言/界面变化影响
