# GitBook 同步说明

## 已验证结论

通过 GitBook MCP 查询，当前这套 Markdown 仓库可以直接通过 Git Sync 接入 GitBook。

关键信息：

- Git Sync 支持 GitHub 或 GitLab 双向同步
- 首次同步可以选择 `GitHub -> GitBook` 或 `GitBook -> GitHub`
- 如果仓库里新增了 Markdown 文件但没有写入 `SUMMARY.md`，GitBook 可能不会显示该页面

## 推荐接入步骤

1. 在 GitBook 中创建一个 Space
2. 点击 `Set up Git Sync`
3. 连接你的 GitHub 仓库和分支
4. 首次导入选择 `GitHub -> GitBook`
5. 导入后检查首页与目录是否正确显示

## 推荐使用方式

- 工程同学继续在仓库里维护 Markdown
- 非技术同学可直接在 GitBook 页面编辑
- 重要改动仍然通过分支和评审流程管理

## 后续可做增强

- 接入 GitBook Site Sections，把过程文档、研发文档、API 文档做成更清晰的顶栏分区
- 产出 OpenAPI 文件，在 GitBook 中开启交互式 API 展示
- 增加 FAQ、变更记录、答辩材料专区
