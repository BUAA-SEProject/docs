# AUBB 文档中心

详细工作流规则见 `AGENTS.md`。

## 技术栈

- VitePress（Vue 驱动的静态站点生成器）
- 发布到 GitHub Pages

## 快速验证

```bash
npm run docs:build
```

## 关键约束

- 新增页面后必须更新 `SUMMARY.md`
- 文档内容需与 `web/` 和 `server/` 实际代码保持同步
- 所有文档使用中文，技术术语可保留英文
