# 软件概要设计说明书

## 1. 文档信息

- 文档名称：AUBB（Academic Unified Builder Bench）软件概要设计说明书
- 版本：v1.2
- 状态：设计基线
- 更新日期：2026-04-14
- 编写依据：SRS v4.3、软件开发计划书 v2.0、课程大作业要求
- 参考标准：ISO/IEC/IEEE 42010、IEEE 1016-2009

## 2. 设计目标与约束

### 2.1 设计目标

1. 支撑“平台初始化 -> 建课 -> 发任务 -> 学员在线 IDE 编辑 / 运行 / 提交 -> 自动评测 -> 人工批改 -> 成绩发布”的完整教学主链路。
2. 在课程项目复杂度可控前提下，明确模块边界、接口边界、数据边界和部署边界。
3. 通过复用成熟开源组件，降低在线 IDE、判题沙箱、统一认证和运维观测的自研成本。
4. 以后端稳定性、事务一致性、权限治理和可维护性为优先，形成适合教学管理系统的 Spring 技术栈基线。

### 2.2 关键约束

- 系统主入口为 Web 浏览器，不建设原生客户端。
- 编程任务必须支持浏览器内在线 IDE 编辑、运行和正式提交。
- 代码运行与正式评测必须隔离于业务主服务之外。
- 首版优先采用模块化单体 + Worker，不采用分布式事务和远程开发容器集群。
- `go-judge` 生产部署以 Linux 为前提，Windows / macOS 仅用于本地研究或演示验证。

## 3. 系统上下文

### 3.1 外部实体

| 外部实体 | 作用 | 与本系统交互内容 |
| --- | --- | --- |
| 浏览器 | 用户操作入口 | 页面访问、表单提交、在线 IDE 编辑、运行结果查看 |
| go-judge 沙箱服务 | 执行试运行与正式评测 | 代码 / 文件快照、运行参数、资源限制、执行结果 |
| 文件存储服务 | 存储课程资源、模板工程、提交快照和导出文件 | 文件上传、下载、生命周期管理 |
| 消息通道 | 邮件、短信、企业 IM 等扩展通知 | 通知发送请求和回执 |
| 统一认证 | 可选 SSO 来源 | 用户身份信息与登录态 |

### 3.2 系统上下文图

```text
Teacher / Student / Admin
          |
       Browser
          |
     platform-web
          |
      platform-api
   /   |      |       |          \
DB  Redis  S3 Store  Stream MQ  Auth Adapter
                   |                |
               judge-worker     Keycloak(optional)
                   |
          go-judge cluster (Linux)
```

## 4. 总体技术选型

### 4.1 推荐技术栈

| 层次 | 技术 / 产品 | 选型说明 |
| --- | --- | --- |
| Web 前端 | Vue 3、TypeScript、Vite、Vue Router、Pinia | 组件化开发效率高，适合课程项目交付 |
| 在线 IDE | Monaco Editor、xterm.js | 复用成熟编辑器和终端输出组件，避免自研编辑内核 |
| UI 与图表 | Element Plus、ECharts | 快速构建后台与统计页面 |
| 后端 API | Spring Boot 4、Java 25、Spring MVC | 生态成熟，适合事务型后台、权限治理和分层设计 |
| 安全与认证 | Spring Security、JWT Resource Server | 适合 API 化访问，可平滑扩展 OIDC |
| 数据访问 | MyBatis-Plus + MyBatis XML、Flyway | 简单 CRUD 效率高，复杂查询可控，数据库变更可版本化 |
| 数据层 | PostgreSQL、Redis | PostgreSQL 承担核心事务模型，Redis 承担缓存和消息流 |
| 异步任务 | Redis Stream + Spring Scheduler | 复用已有 Redis，降低中间件数量，足够覆盖运行、评测、通知任务 |
| 对象存储 | S3 兼容存储 | 开发 / 答辩环境默认 MinIO；私有化可替换 Ceph RGW 或云对象存储 |
| 判题沙箱 | `criyle/go-judge` | 提供 REST / WebSocket / gRPC 接口、容器池、cgroup / namespace 隔离和文件缓存能力 |
| 统一认证 | Keycloak（可选） | 后续需要 OIDC / SAML / LDAP 时可直接接入 |
| 运维观测 | Nginx、Docker Compose、Prometheus、Grafana、Loki | 支撑本地演示、课程答辩和基础观测 |

### 4.2 开源组件复用策略

| 能力 | 推荐开源项目 | 采用策略 | 说明 |
| --- | --- | --- | --- |
| 浏览器代码编辑 | Monaco Editor | 直接采用 | 具备模型管理、多语言支持和大文件编辑能力 |
| 运行输出面板 | xterm.js | 直接采用 | 用于承载 stdout / stderr 与交互式输出展示 |
| 判题与沙箱 | `go-judge` | 直接采用 | 提供统一 API、容器池、资源限制、缓存文件 `fileId` 和 `pipeMapping` 能力 |
| 数据库迁移 | Flyway | 直接采用 | 便于版本化维护表结构和初始化脚本 |
| 统一认证 | Keycloak | 可选接入 | 若后续需要统一认证，可通过 OIDC 适配层接入 |
| 队列观测 | Redis Insight / 自定义管理页 | 按需接入 | 观察 Stream 队列堆积、消费组和失败消息 |

### 4.3 不采用的方案

- V1 不采用 NestJS / Prisma / BullMQ 方案，原因是该项目以后台治理、事务和权限控制为核心，Spring Boot 在教学管理系统场景下更稳。
- V1 不直接引入 `code-server`、Eclipse Theia 等完整远程开发环境。
- 原因是这类方案更适合长期持久化远程工作区，会显著增加容器编排、资源隔离和运维成本。

## 5. 架构风格与分层

### 5.1 架构风格

- 业务层采用模块化单体，降低首版实现和运维复杂度。
- 运行与评测采用独立 Worker 调度，避免长耗时任务阻塞 Web 请求。
- 在线 IDE 工作区与正式提交解耦，保证“运行”与“评测 / 成绩”边界清晰。
- 文件、运行、评测和通知统一走事件与消息流机制，增强可恢复性。

### 5.2 分层结构

| 层次 | 组件 | 职责 |
| --- | --- | --- |
| 表现层 | `platform-web` | 路由、页面、在线 IDE、表单校验、图表展示 |
| 接口层 | `platform-api` | Controller、鉴权、请求校验、响应封装 |
| 应用层 | Application Service | 业务编排、事务协调、幂等控制、事件发布 |
| 领域层 | 平台治理、课程、任务、IDE 工作区、提交、评测、批改、通知模块 | 核心业务规则与状态流转 |
| 基础设施层 | PostgreSQL、Redis、S3 兼容存储、`go-judge`、日志与监控 | 存储、缓存、消息流、执行、观测 |

## 6. 逻辑模块划分

| 模块 | 核心职责 | 主要用户 |
| --- | --- | --- |
| 平台治理 | 平台配置、学校/学院/课程/班级组织、用户、作用域身份、审计、平台概览 | 分层管理员 |
| 身份认证 | 登录、退出、JWT、权限检查、账号状态管理 | 全角色 |
| 课程管理 | 课程、成员、资源、章节结构、邀请码 | 教师、学员 |
| 任务管理 | 任务说明、语言配置、模板工程、提交规则、评分规则 | 教师 |
| IDE 工作区 | 在线编辑、多文件工程、草稿自动保存、试运行、控制台展示 | 学员 |
| 提交中心 | 正式提交受理、快照固化、提交历史、下载与对比 | 学员、教师 |
| 判题中心 | 评测排队、编译缓存、用例执行、结果归一化、重评 | 系统、教师 |
| 批改与成绩 | 人工评分、Rubric、成绩生成、发布、撤回、复核 | 教师、助教、学员 |
| 通知中心 | 站内通知、公告、多渠道通知扩展 | 全角色 |
| 运营概览 | 课程概览、平台概览、异常与审计检索 | 管理员、运维 |

## 7. 核心业务流程

### 7.1 教学主链路

```text
管理员初始化平台
  -> 教师创建课程与任务
  -> 学员进入在线 IDE
  -> 学员运行代码验证样例
  -> 学员正式提交代码快照
  -> 系统异步发起评测
  -> 教师查看评测并人工批改
  -> 系统生成并发布成绩
  -> 学员查看反馈与成绩
```

### 7.2 关键时序一：在线 IDE 试运行

```text
Student -> Web: 打开任务 IDE
Web -> API: 拉取任务模板与个人工作区
Student -> Web: 编辑代码并点击运行
Web -> API: 创建 run session
API -> Redis Stream: 写入 sandbox.run 事件
judge-worker -> go-judge: 执行样例 / 自定义输入
go-judge -> judge-worker: 返回 stdout/stderr/资源指标
judge-worker -> DB: 写入 sandbox_runs
Student -> API: 轮询运行结果
```

### 7.3 关键时序二：正式提交与自动评测

```text
Student -> Web: 点击正式提交
Web -> API: 发送工作区快照引用
API -> Postgres: 写入 submission / snapshot
API -> Redis Stream: 写入 submission.accepted 事件
judge-worker -> go-judge: 编译并缓存产物
judge-worker -> go-judge: 逐个隐藏用例执行
go-judge -> judge-worker: 返回结构化结果
judge-worker -> DB: 写入 judge_runs 并更新 submission 状态
API -> Notification: 发送评测完成事件
```

### 7.4 关键时序三：人工批改与成绩发布

```text
Teacher -> API: 打开提交详情
Teacher -> API: 保存评语 / Rubric / 人工分
API -> DB: 写入 review_record
API -> DB: 计算 grade
Teacher -> API: 发布成绩
API -> Notification: 发布成绩通知
Student -> API: 查看成绩与评语
```

## 8. 数据设计总览

### 8.1 核心实体

- 平台治理：`platform_configs`、`org_units`、`users`
- 课程域：`courses`、`course_members`、`course_resources`
- 任务域：`tasks`、`task_language_profiles`、`task_testcases`、`task_starter_files`、`task_rubrics`
- IDE 与运行：`ide_workspaces`、`ide_workspace_files`、`workspace_snapshots`、`sandbox_runs`
- 提交与评测：`submissions`、`submission_files`、`judge_runs`
- 批改与成绩：`review_records`、`grades`、`grade_rechecks`
- 消息与审计：`notifications`、`announcements`、`audit_logs`

### 8.2 数据原则

- 所有关键对象必须具备状态字段、创建时间、更新时间和操作者留痕。
- 工作区数据是可变草稿，正式提交与正式评测数据必须采用不可变快照。
- 提交、评测、成绩等关键结果采用“追加历史 + 当前有效引用”策略，不做无痕覆盖。
- 文件实体与业务实体解耦，数据库保存对象存储引用与元数据。

## 9. 接口设计总览

### 9.1 API 风格

- 基础路径：`/api/v1`
- 数据格式：JSON，文件上传使用 `multipart/form-data`
- 认证方式：Spring Security + JWT Bearer Token，可扩展到 OIDC
- 错误模型：统一错误码、消息、请求 ID

### 9.2 API 分组

| 分组 | 说明 |
| --- | --- |
| `/auth/*` | 登录、退出、当前用户、统一认证回调 |
| `/admin/*` | 平台配置、组织、用户、平台级概览、审计 |
| `/courses/*` | 课程、成员、资源、邀请码 |
| `/tasks/*` | 任务、语言配置、模板工程、测试用例、Rubric |
| `/ide/*` | 工作区拉取、文件保存、试运行、运行结果查询 |
| `/submissions/*` | 正式提交创建、提交详情、提交历史、评测状态 |
| `/grades/*` | 批改记录、成绩发布、成绩导出、复核 |
| `/notifications/*` | 站内通知、公告、已读状态 |

## 10. 部署视图

### 10.1 最小可运行拓扑

| 节点 | 服务 |
| --- | --- |
| Web 节点 | Nginx + `platform-web` |
| API 节点 | `platform-api`（Spring Boot） |
| Worker 节点 | `judge-worker`（Spring Boot） |
| 沙箱节点 | `go-judge` + 编译器 / 运行时环境 |
| 数据节点 | PostgreSQL、Redis、S3 兼容存储 |
| 观测节点 | Prometheus、Grafana、Loki |

### 10.2 部署特性

- API 与 Worker 可水平扩展。
- `go-judge` 节点可按课程高峰期独立扩容，Worker 通过负载均衡访问。
- 沙箱节点必须运行在具备 Linux namespace / cgroup 能力的宿主环境。
- Redis 当前承担缓存和消息流，部署时应配置持久化与内存水位。

## 11. 安全、可靠性与可观测性设计

### 11.1 安全

- 所有受保护接口必须由 Spring Security 统一拦截，课程级权限在业务层二次校验。
- 在线运行与正式评测均通过 `go-judge` 执行，默认禁用外网访问，限制 CPU、内存、运行时间、输出大小和文件系统权限。
- 审计日志记录登录、平台配置更新、导入、任务发布、成绩发布、权限调整、导出和重评行为。

### 11.2 可靠性

- 正式提交采用“先固化快照、再落库、后发消息”的模式，保证受理成功即不丢失。
- 试运行失败不影响工作区保存；评测失败不影响课程浏览、历史提交与成绩查询。
- Flyway 负责数据库迁移，降低手工改表风险。

### 11.3 可观测性

- 输出结构化日志，带 `requestId`、`userId`、`courseId`、`taskId`、`submissionId` 等上下文。
- 核心指标包括 API 延迟、运行队列深度、评测队列深度、评测失败率、工作区保存失败率、成绩发布量。
- 提供教师课程概览和管理员平台概览双层仪表盘。

## 12. 设计取舍

| 设计点 | 选择 | 原因 |
| --- | --- | --- |
| 后端框架 | Spring Boot 3 + Java 21 | 更适合事务型后台、权限治理、批处理和审计类系统 |
| 数据访问 | MyBatis-Plus + MyBatis XML | 兼顾开发效率与复杂查询可控性 |
| 异步方案 | Redis Stream + Worker | 复用 Redis，组件更少，满足课程项目场景 |
| 在线 IDE 方案 | Monaco Editor + 自定义工作区 | 满足作业编辑 / 运行 / 提交场景，明显轻于完整远程 IDE |
| 判题方案 | `go-judge` + 自定义 `judge-worker` | 支持沙箱隔离、编译缓存、统一结果归一化，适合教学平台接入 |

## 13. 追踪关系

| 设计元素 | 对应 SRS |
| --- | --- |
| 平台治理模块 | FR-CFG-*、FR-IAM-*、FR-OPS-* |
| 课程与任务模块 | FR-CRS-*、FR-TSK-* |
| 在线 IDE 与提交模块 | FR-SUB-* |
| 判题与沙箱模块 | FR-JDG-* |
| 批改与成绩模块 | FR-REV-* |
| 可观测与安全设计 | NFR-SEC-*、NFR-REL-*、NFR-OBS-* |
