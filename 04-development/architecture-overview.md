# 总体架构

## 1. 推荐技术栈

| 层次 | 技术 |
| --- | --- |
| Web 前端 | Vue 3、TypeScript、Vite、Vue Router、Pinia |
| UI 能力 | Element Plus、Monaco Editor、ECharts |
| 后端 | NestJS、TypeScript、Prisma |
| 数据层 | PostgreSQL、Redis、MinIO |
| 异步任务 | BullMQ / Redis Queue |
| 判题 | Judge0 CE + 自定义 `judge-worker` |
| 运维 | Docker Compose、Nginx、Prometheus、Grafana |

## 2. 架构视图

```text
platform-web
   |
platform-api
 |   |    |    \
DB Redis MinIO  Queue
                 |
            judge-worker
                 |
              Judge0
```

## 3. 设计原则

- 优先采用模块化单体，避免为课程项目引入不必要的分布式复杂度。
- 通过异步 Worker 隔离耗时评测任务。
- 通过统一接口契约隔离前后端与第三方判题组件。
- 通过统一审计与日志上下文保证可追踪性。

## 4. 仓库分层

| 目录 | 内容 |
| --- | --- |
| `apps/platform-web` | 前端 SPA |
| `apps/platform-api` | 业务 API |
| `apps/judge-worker` | 评测调度与结果归一化 |
| `packages/shared-types` | 共享类型、枚举、错误码 |
| `infra/docker` | Docker Compose 与镜像配置 |
| `infra/sql` | 初始化脚本与种子数据 |

## 5. 跨模块约束

- 所有对外接口统一由 `platform-api` 暴露。
- `judge-worker` 不直接暴露给浏览器，只消费队列并写回结果。
- 平台治理、课程、任务、提交、成绩共享统一的用户、课程、任务主键体系。
- 审计日志由 API 层统一记录，不分散在页面逻辑中。

## 6. 扩展点

- 接入统一认证时，仅替换认证适配层，不改业务领域模型。
- 新增语言或运行环境时，仅扩展判题模板和 Judge0/镜像配置。
- 后续增加 AI 助教时，作为可选模块接入通知与课程上下文，不耦合主链路。
