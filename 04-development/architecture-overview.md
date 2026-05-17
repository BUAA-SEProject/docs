---
title: "总体架构"
section: "04-development"
status: current
---
# 总体架构

## 1. 当前技术栈

| 层次 | 技术 |
| --- | --- |
| Web 前端 | Next.js 16 (App Router)、React 19、TypeScript、Tailwind CSS 4 |
| UI 能力 | shadcn/ui、Monaco Editor、xterm.js、ECharts |
| 状态与数据 | TanStack Query、Zustand、Axios |
| 后端 | Spring Boot 4、Java 25、Spring MVC、Spring Security |
| 数据访问 | MyBatis-Plus、Flyway |
| 数据层 | PostgreSQL、MinIO 兼容对象存储 |
| 异步任务 | RabbitMQ（评测队列第一阶段） |
| 判题 | go-judge（集成在同一 Spring Boot 应用内） |
| 认证 | JWT Bearer access token + opaque refresh token |
| 运维 | Docker Compose、Nginx、Prometheus、Grafana、Loki |

## 2. 开源组件选型说明

| 能力 | 组件 | 采用方式 | 说明 |
| --- | --- | --- | --- |
| 在线编辑器 | Monaco Editor | 直接集成 | 支撑多文件编辑、语言高亮和模型管理 |
| 输出终端 | xterm.js | 直接集成 | 展示试运行输出与执行状态 |
| 沙箱与判题 | `go-judge` | 直接集成 | 提供统一 API、文件缓存、资源限制和容器池 |
| 数据库迁移 | Flyway | 直接集成 | 管理表结构变更与初始化脚本 |
| 消息队列 | RabbitMQ | 直接集成 | 评测作业入队，支持后续重试和死信治理扩展 |
| 对象存储 | MinIO | 直接集成 | 评测报告、实验报告附件等文件存储 |

## 3. 架构视图

```text
web (Next.js 16)
   |
server (Spring Boot 4)
 |   |      |        |
DB  MinIO  RabbitMQ  go-judge
```

- `server/`：Spring Boot 后端，包含全部业务模块与评测执行
- `web/`：Next.js 前端，App Router 架构
- `docs/`：VitePress 文档站点

## 4. 设计原则

- 优先采用模块化单体，避免为课程项目引入不必要的分布式复杂度。
- 评测任务集成在同一 Spring Boot 应用内，通过 RabbitMQ 异步入队，关闭队列时回退到应用内异步监听。
- 通过统一工作区快照模型隔离"在线 IDE 草稿"和"正式提交"。
- 通过 Spring Security + 业务层鉴权双重控制权限边界。
- 通过统一审计与日志上下文保证可追踪性。

## 5. 仓库布局

| 目录 | 内容 |
| --- | --- |
| `web/` | Next.js 16 前端应用 |
| `server/` | Spring Boot 4 后端应用 |
| `docs/` | VitePress 文档站点 |

## 6. 包结构

当前仓库采用模块优先的模块化单体结构：业务代码进入 `com.aubb.server.modules.<module>`，模块内部再细分 `api / application / domain / infrastructure` 四层。

当前已落地的模块：

- `modules.identityaccess`：登录、JWT、当前用户、用户管理、教务画像、组织成员关系、平台治理身份
- `modules.course`：学期、课程模板、开课实例、教学班、课程成员、班级功能开关
- `modules.assignment`：作业创建、列表、详情、状态流转、题库管理、结构化试卷快照
- `modules.submission`：正式提交受理、分题答案、评分摘要、提交附件
- `modules.grading`：人工批改、成绩发布、成绩册、导入导出、统计与排名
- `modules.judge`：评测作业入队、go-judge 适配、评测结果回写、评测报告
- `modules.lab`：教学班级实验、实验报告、对象存储附件
- `modules.notification`：站内通知、收件状态、未读数、关键教学事件入箱
- `modules.organization`：学校/学院/课程/班级组织树
- `modules.platformconfig`：单份即时生效的平台配置
- `modules.audit`：审计记录写入与分页检索

共享顶层包：

- `config`：安全、持久化、序列化等跨模块框架配置
- `common`：分页、错误模型、请求上下文、对象存储等共享能力
- `infrastructure.persistence`：跨模块复用的持久化适配

## 7. 基础设施边界

- PostgreSQL 是关系型事实来源
- RabbitMQ 当前已承接 judge 队列第一阶段，并保留给后续独立 worker、重试和死信治理扩展
- MinIO 承接共享对象存储，当前由 `common.storage` 对外暴露统一接口
- go-judge 承接当前脚本型自动评测执行
- Flyway 负责数据库模式演进
- MyBatis-Plus 负责主数据持久化

## 8. 认证与授权

- 认证方式：JWT Bearer access token，服务端签发；受保护请求除验签外，还会按 `sid` 回查 `auth_sessions` 与当前用户状态。
- 令牌内容：用户标识、账号状态、默认组织、画像快照、身份列表、`sid` 和授权所需的 authority。
- 平台治理身份：`SCHOOL_ADMIN`、`COLLEGE_ADMIN`、`COURSE_ADMIN`、`CLASS_ADMIN`。
- 身份分配模型：一个用户可拥有多个作用域身份，每个身份都绑定一个组织节点。
- refresh token 当前使用 opaque token，仅保存 hash。
- `logout`、`/api/v1/auth/revoke`、管理员强制失效和账号停用都会让旧会话即时失效。

## 9. 跨模块约束

- 所有对外接口统一由 `server` 暴露，基线路径 `/api/v1`。
- 评测任务不单独部署，集成在同一 Spring Boot 应用内。
- 在线运行与正式评测共用 `go-judge`，但必须写入不同数据表。
- 平台治理、课程、任务、工作区、提交、成绩共享统一的用户、课程、任务主键体系。
- 审计日志由应用层统一记录，不分散在页面逻辑中。

## 10. 扩展点

- 新增语言或运行环境时，仅扩展任务语言模板和 `go-judge` rootfs / 编译器配置。
- 若后续引入交互题，可基于 `go-judge` 的 `pipeMapping` 能力扩展。
- 若后续并发明显增大，可评估引入独立 judge-worker 服务。
