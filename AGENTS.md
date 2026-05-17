# AGENTS.md - AUBB 文档中心

## 项目概览

- VitePress 文档站点，发布到 GitHub Pages
- 覆盖需求、设计、API 规格、测试、部署与团队工作流
- 通过 GitHub Actions 在 push 到 main 时自动部署

## 语言

- 所有文档使用中文编写
- 技术术语可保留英文

## 目录结构

- `01-overview/`：课程要求、项目章程、路线图
- `02-process-docs/`：SRS、设计文档、测试报告、部署指南、用户手册
- `03-product/`：系统概览、用户角色、需求、模块地图
- `04-development/`：架构、前后端文档、工程标准
- `05-api/`：API 文档与错误码
- `06-testing-and-ops/`：测试策略、部署、可观测性
- `07-team-and-workflow/`：角色、待办、贡献指南

## 工作规则

- 新增 Markdown 页面后必须更新 `SUMMARY.md`（VitePress 导航依赖此文件）
- 文档内容需与 `web/` 和 `server/` 的实际代码状态保持同步
- 验证命令：`npm run docs:build`（提交前必须通过）
- Commit 格式：`<type>(scope): <summary>`（中文、动词开头、≤ 50 字）

## 跨仓库引用

- `web/`：前端实现
- `server/`：后端实现，`server/docs/` 为内部开发文档
- 本仓库为面向外部的文档站点

## 指令优先级

1. 当前会话中用户的明确要求
2. 仓库自身规则、文档与约定
3. 本 `AGENTS.md`
4. 相关 Superpowers / skill 流程定义
