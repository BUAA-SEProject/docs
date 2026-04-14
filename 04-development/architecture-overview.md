# 总体架构

## 1. 推荐技术栈

| 层次 | 技术 |
| --- | --- |
| Web 前端 | Vue 3、TypeScript、Vite、Vue Router、Pinia |
| UI 能力 | Element Plus、Monaco Editor、xterm.js、ECharts |
| 后端 | Spring Boot 3、Java 21、Spring MVC、Spring Security |
| 数据访问 | MyBatis-Plus、MyBatis XML、Flyway |
| 数据层 | PostgreSQL、Redis、S3 兼容对象存储 |
| 异步任务 | Redis Stream、Spring Scheduler |
| 判题与运行 | `criyle/go-judge` + 自定义 `judge-worker` |
| 统一认证 | Spring Session、OIDC 适配层、Keycloak（可选） |
| 运维 | Docker Compose、Nginx、Prometheus、Grafana、Loki |

## 2. 开源组件选型说明

| 能力 | 组件 | 采用方式 | 说明 |
| --- | --- | --- | --- |
| 在线编辑器 | Monaco Editor | 直接集成 | 支撑多文件编辑、语言高亮和模型管理 |
| 输出终端 | xterm.js | 直接集成 | 展示试运行输出与执行状态 |
| 沙箱与判题 | `go-judge` | 直接集成 | 提供统一 API、文件缓存、资源限制和容器池 |
| 单点登录 | Keycloak | 按需接入 | 统一认证、用户联邦、OIDC / SAML 扩展 |
| 数据库迁移 | Flyway | 直接集成 | 管理表结构变更与初始化脚本 |

## 3. 架构视图

```text
platform-web
   |
platform-api (Spring Boot)
 |   |      |        |          \
DB Redis  S3Store  Stream MQ   OIDC Adapter
                    |
          judge-worker (Spring Boot)
                    |
                go-judge
```

## 4. 设计原则

- 优先采用模块化单体，避免为课程项目引入不必要的分布式复杂度。
- 通过独立 Worker 隔离试运行与正式评测任务。
- 通过统一工作区快照模型隔离“在线 IDE 草稿”和“正式提交”。
- 通过 Spring Security + 业务层鉴权双重控制权限边界。
- 通过统一审计与日志上下文保证可追踪性。

## 5. 仓库分层

| 目录 | 内容 |
| --- | --- |
| `frontend/platform-web` | 前端 SPA 与在线 IDE 页面 |
| `backend/platform-api` | Spring Boot 业务 API |
| `backend/judge-worker` | Spring Boot Worker，处理运行与评测消息 |
| `backend/common` | 公共错误码、枚举、响应模型、工具类 |
| `infra/docker` | Docker Compose 与镜像配置 |
| `infra/gojudge` | `go-judge` 配置、rootfs / 镜像说明 |
| `infra/sql` | Flyway 脚本与种子数据 |

## 6. 跨模块约束

- 所有对外接口统一由 `platform-api` 暴露。
- `judge-worker` 不直接暴露给浏览器，只消费消息流并写回结果。
- 在线运行与正式评测共用 `go-judge`，但必须写入不同数据表。
- 平台治理、课程、任务、工作区、提交、成绩共享统一的用户、课程、任务主键体系。
- 审计日志由应用层统一记录，不分散在页面逻辑中。

## 7. 扩展点

- 接入统一认证时，仅替换认证适配层，不改业务领域模型。
- 新增语言或运行环境时，仅扩展任务语言模板和 `go-judge` rootfs / 编译器配置。
- 若后续引入交互题，可基于 `go-judge` 的 `pipeMapping` 能力扩展。
- 若后续并发明显增大，再评估将 Redis Stream 替换为 RabbitMQ / Kafka。
