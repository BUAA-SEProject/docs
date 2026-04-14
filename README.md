# AUBB（Academic Unified Builder Bench）文档中心

本目录已经迁移为基于 VitePress 的文档站，推送到 `main` 后会通过 GitHub Actions 自动构建并发布到 GitHub Pages。

这里集中管理三类内容：

- 课程大作业要求与里程碑
- 软件开发计划书、需求、设计、测试、部署、用户手册等过程文档
- 前端、后端、客户端、数据库、API、协作规范等研发文档

## 如何使用

建议按下面的路径阅读和维护：

1. 从 [项目概览](01-overview/index.md) 了解项目背景、课程要求与里程碑。
2. 在 [过程文档](02-process-docs/index.md) 中持续补齐课程要求的正式交付件。
3. 在 [产品与需求](03-product/index.md) 中沉淀核心需求、角色与模块边界。
4. 在 [研发文档](04-development/index.md) 与 [API 文档](05-api/index.md) 中同步实现细节。
5. 在 [测试与运维](06-testing-and-ops/index.md) 和 [团队协作](07-team-and-workflow/index.md) 中维护验收、部署与协作流程。

## 本地运行

```bash
npm install
npm run docs:dev
```

构建静态站点：

```bash
npm run docs:build
```

## 顶层结构

- `01-overview`：课程背景、项目章程、路线图
- `02-process-docs`：计划书、需求、概要设计、详细设计、测试、部署、用户手册
- `03-product`：系统定位、用户角色、核心需求、模块地图
- `04-development`：架构、前后端、客户端、数据库、工程规范
- `05-api`：接口设计与错误码
- `06-testing-and-ops`：测试策略、环境部署、可观测性、验收清单
- `07-team-and-workflow`：分工、任务跟踪、文档维护、站点发布

## 维护原则

- 所有正式交付件优先在本目录维护，避免过程文档分散在聊天、网盘或个人笔记中。
- 需求、设计、代码、测试和部署文档保持相互对应，确保答辩时可以闭环说明。
- 新增 Markdown 页面后，务必同步更新 `SUMMARY.md`，VitePress 导航会基于它自动生成。
- 对外展示前，优先保证主链路文档完整：登录 -> 课程 -> 作业/实验 -> 提交 -> 评测 -> 批改 -> 成绩。
