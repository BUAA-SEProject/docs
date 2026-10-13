# 文档协作约定

## 获取与提交

```sh
git clone https://github.com/BUAA-SEProject/docs.git
cd docs
git switch -c docs/your-topic
```

按主题修改文档，完成核对后提交并发起 Pull Request：

```sh
git diff --check
git status --short
git add <本次修改的文件>
git commit -m "docs: 更新需求调研结论"
git push -u origin docs/your-topic
```

一个提交尽量只处理一项清晰的修改，例如需求变更、模型调整或课堂反馈补充。提交前确认变更列表中没有 Office 锁文件、缓存、凭据和生成的 ZIP。

## 源稿与交付文件

- 优先在 Markdown 中维护可比较的正文；调整正文后，同步对应 Word 交付文件并检查分页、表格和图片。在同一个提交中说明同步情况。若直接编辑 Word，也要同步 Markdown。
- PPT 直接在 PowerPoint 中编辑；调整页码、讲述顺序或时间后，同步课堂讲稿和备注中的来源。
- 修改 PlantUML 后同步 PNG，并核对 SRS、SPEC、模型说明及追踪矩阵中的业务规则。现有 PlantUML 不等于已经完成课程要求的 CodeArts Modeling 交付。
- 保持 `研讨课材料包` 内的文件名和相对目录稳定。确需改名时，同步 Markdown 链接、Word 引用、PPT 备注与打包脚本。
- 课程 PDF 只保留在 `课程参考原文`。审查记录按日期新增，保留历史结论的上下文。

## 提交前检查

1. 在 GitHub 或本地 Markdown 预览中检查新增链接和图片。
2. 打开改动的 Word、PPT、模型导出图，检查内容及排版。
3. 需要交作业时运行 `python scripts/package_materials.py`，检查 `dist/` 中的输出。脚本校验 Office 文件的 ZIP 完整性与生成包内容，不代替课程内容或视觉审查。
4. 据实标注已完成、待验证和待填写事项。自动检查结果不能代替真实访谈、双组实验或成员人工复核。

`dist/`、旧生成工作区、历史备份与临时文件不提交到 Git。正式 Word、PPT、PDF、PNG 和 PlantUML 文件应随相应文档一起提交。
