---
title: "软件详细设计说明书"
section: "02-process-docs"
status: current
---
# 软件详细设计说明书

## 1. 文档信息

- 文档名称：AUBB（Academic Unified Builder Bench）软件详细设计说明书
- 版本：v1.3
- 状态：设计基线
- 更新日期：2026-04-15
- 编写依据：SRS v4.4、概要设计说明书 v1.3、模块地图、API 设计草案
- 参考标准：IEEE 1016-2009

## 2. 代码仓与目录建议

```text
seproject/
  frontend/
    platform-web/
  backend/
    pom.xml
    common/
    platform-api/
    judge-worker/
  infra/
    docker/
    sql/
    grafana/
    gojudge/
  docs/
```

### 2.1 当前仓库实现

当前后端仓库以单模块 `AUBB-Server` 为主，围绕 `com.aubb.server.modules.<module>` 组织业务代码，模块内部继续采用 `api / application / domain / infrastructure` 四层；共享能力保留在 `common`、`config` 和 `infrastructure.persistence`。课程域与 `judge-worker` 仍作为后续扩展位保留在系统级设计中。

## 3. 前端详细设计

### 3.1 路由结构

| 路由前缀 | 页面 | 权限 |
| --- | --- | --- |
| `/login` | 登录页 | 匿名 |
| `/student/courses` | 学员课程列表 | 学员 |
| `/student/courses/:courseId/tasks/:taskId` | 学员任务详情 | 学员 |
| `/student/courses/:courseId/tasks/:taskId/ide` | 学员在线 IDE | 学员 |
| `/teacher/courses` | 教师课程列表 | 教师 / 助教 |
| `/teacher/courses/:courseId/tasks/new` | 任务创建页 | 教师 |
| `/teacher/courses/:courseId/tasks/:taskId/languages` | 任务语言 / 用例配置页 | 教师 |
| `/teacher/submissions/:submissionId` | 提交详情与批改页 | 教师 / 助教 |
| `/admin/config` | 平台配置 | 管理员 |
| `/admin/users` | 用户与组织管理 | 管理员 |
| `/admin/audit` | 审计日志 | 管理员 / 运维 |

### 3.2 状态管理模块

| Store | 负责状态 |
| --- | --- |
| `authStore` | 当前用户、角色、登录态、菜单权限 |
| `courseStore` | 课程列表、课程详情、成员、资源 |
| `taskStore` | 任务详情、提交规则、语言配置、Rubric、测试用例 |
| `ideStore` | 工作区文件树、当前语言、活动文件、编辑脏状态、保存状态 |
| `runStore` | 试运行输入、运行历史、stdout / stderr、运行状态 |
| `submissionStore` | 正式提交列表、当前提交、评测状态 |
| `gradeStore` | 批改记录、成绩单、复核状态 |
| `adminStore` | 平台配置、用户、组织、审计统计 |

### 3.3 在线 IDE 页面布局

- 左侧：文件树、模板工程说明、文件新建 / 重命名 / 删除入口。
- 中部：基于 Monaco Editor 的多标签页编辑区。
- 下方：运行控制台，展示标准输出、标准错误、资源摘要和最近运行记录。
- 右侧：任务说明、样例、提交限制、当前评测状态和正式提交入口。

### 3.4 页面交互规则

- 文件编辑采用 2 秒防抖自动保存，并支持手动保存。
- 点击“运行”前先将当前编辑缓冲区同步到工作区。
- 点击“正式提交”时，若存在未保存改动，先触发强制保存并在成功后固化快照。
- 运行结果与正式评测结果分别展示，视觉和文案必须显式区分。

## 4. 后端详细设计

### 4.1 部署单元

| 服务 | 技术栈 | 责任 |
| --- | --- | --- |
| `platform-api` | Spring Boot 4、Spring MVC、Spring Security、MyBatis-Plus | 对外 API、权限、事务、业务编排 |
| `judge-worker` | Spring Boot 4、Spring Data Redis、定时调度 | 消费运行 / 评测消息、调用 `go-judge`、归一化结果 |

### 4.2 包结构设计

```text
com.aubb.server
  ├─ modules
  │   ├─ identityaccess
  │   ├─ organization
  │   ├─ platformconfig
  │   └─ audit
  ├─ common
  ├─ config
  ├─ infrastructure
  │   └─ persistence
```

### 4.3 模块内部分层

| 层次 | 职责 | 说明 |
| --- | --- | --- |
| `modules.<module>.api` | 接口定义、参数接收、响应输出 | 只做协议转换，不承载业务逻辑 |
| `modules.<module>.application` | 应用服务 | 编排事务、调用领域规则、执行作用域授权 |
| `modules.<module>.domain` | 领域规则 | 密码、角色、组织层级等核心规则 |
| `modules.<module>.infrastructure` | Mapper 与实体 | 数据访问、持久化与模块内外部适配 |
| `common / config / infrastructure.persistence` | 共享基础设施 | 承载跨模块通用配置、错误模型、请求上下文和持久化公共适配 |

### 4.4 请求处理链路

```text
Nginx
  -> Spring Security FilterChain
  -> Login/User Context Filter
  -> Controller
  -> Application Service
  -> Domain Service
  -> Mapper
  -> PostgreSQL / Redis / S3 / Redis Stream
```

### 4.5 认证与权限设计

#### 4.5.1 Spring Security 过滤链

- 匿名放行：`/api/v1/auth/login`、`/api/v1/auth/logout`、健康检查、静态资源。
- 认证入口：基于用户名密码登录后签发 JWT，客户端通过 `Authorization: Bearer <token>` 传递访问令牌。
- 令牌校验：API 侧使用 Spring Security Resource Server 校验 JWT 签名、有效期和声明。
- CSRF：当前治理接口使用 Bearer Token，无需依赖 CSRF Token。

#### 4.5.2 权限模型

- 平台治理权限：学校/学院/课程/班级管理员通过 JWT 中的 authority 与应用层作用域校验联合控制。
- 课程级权限：教师、助教、学员通过 `course_members` 关系在业务层二次校验。
- 数据级权限：提交、成绩、工作区等资源进入应用服务后再次检查归属关系。

#### 4.5.3 统一认证扩展

- 若启用 Keycloak，则采用 OIDC code flow。
- 外部身份映射表属于后续统一认证扩展位，当前 Phase 2 不进入落库实现。
- 外部身份登录成功后，仍要回填平台内角色与组织信息，不直接信任外部系统的课程权限。

### 4.6 数据访问设计

#### 4.6.1 ORM / Mapper 策略

- 简单单表 CRUD：优先使用 MyBatis-Plus。
- 多表联查、聚合统计、分页筛选：使用 MyBatis XML 自定义 SQL。
- 禁止 Controller 直接调用 Mapper，必须经由 Application Service / Domain Service。

#### 4.6.2 数据转换策略

- 请求体 `DTO` 只用于接口层。
- 数据库表对应 `Entity`。
- 页面或接口返回统一输出 `VO`。
- DTO / Entity / VO 转换使用 MapStruct，避免手写大量样板代码。

### 4.7 事务设计

| 场景 | 事务边界 | 说明 |
| --- | --- | --- |
| 创建课程 | `CourseAppService#createCourse` | 创建课程、负责人关系、审计记录一次提交 |
| 发布任务 | `TaskAppService#publishTask` | 任务状态变更、版本留痕、校验配置一致提交 |
| 保存工作区 | `IdeWorkspaceAppService#saveFiles` | 文件 upsert、版本递增在单事务内完成 |
| 正式提交 | `SubmissionAppService#createSubmission` | 先固化快照，再写提交记录和审计，最后发消息 |
| 发布成绩 | `GradeAppService#publishGrade` | 成绩状态变更、通知事件、审计记录一次提交 |

事务规则：

- 外部调用 `go-judge`、S3 上传、Redis Stream 发消息不应长时间占用数据库事务。
- 需要消息投递的场景采用“本地事务成功后发送消息”的方式，失败由补偿任务处理。
- 重评、批量导入等接口必须支持幂等键或显式去重条件。

### 4.8 Redis 设计

#### 4.8.1 Key 规划

| Key 模式 | 作用 |
| --- | --- |
| `jwt:blacklist:*` | 预留的令牌撤销扩展位，当前版本未启用 |
| `cache:platform-config` | 平台配置缓存 |
| `cache:course:{courseId}` | 课程基础信息缓存 |
| `rate:login:{username}` | 登录失败计数 |
| `lock:submission:{taskId}:{userId}` | 同一任务提交互斥锁 |

#### 4.8.2 Stream 规划

| Stream | 消息类型 | 消费组 |
| --- | --- | --- |
| `stream:sandbox-run` | 试运行任务 | `judge-worker` |
| `stream:submission-judge` | 正式评测任务 | `judge-worker` |
| `stream:notification` | 通知发送任务 | `notify-worker` 或 `platform-api` |

消费规则：

- 使用消费者组保证多实例并发消费。
- Worker 启动时扫描 pending list，对长时间未确认消息做恢复。
- 死信消息进入 `stream:dead-letter`，供后台人工处理。

### 4.9 定时任务设计

| 定时任务 | 实现方式 | 作用 |
| --- | --- | --- |
| 任务自动关闭 | `@Scheduled` | 到达截止时间后关闭任务 |
| 草稿压缩清理 | `@Scheduled` | 清理旧工作区版本 |
| 缓存文件清理 | `@Scheduled` | 清理 `go-judge` 缓存产物 |
| 审计归档 | `@Scheduled` | 转储或清理历史日志 |
| 消息补偿 | `@Scheduled` | 重试失败通知或未确认评测消息 |

### 4.10 审计与异常设计

- 关键操作审计通过 `AuditLogAppService` 统一写入。
- 统一异常处理使用 `@RestControllerAdvice`，映射为稳定错误码。
- 所有请求日志必须带 `requestId`；登录、提交、评测、成绩链路增加 `userId`、`courseId`、`taskId`、`submissionId`。

## 5. 关键模块详细设计

### 5.1 认证与访问令牌

#### 5.1.1 登录流程

1. `AuthController#login` 接收用户名 / 密码。
2. `AuthAppService` 调用 `UserMapper` 查询用户。
3. 校验账号状态、密码哈希、失败次数与锁定时间。
4. 认证成功后由服务端签发 JWT，并返回给客户端。
5. `AuditLogAppService` 记录登录结果。

#### 5.1.2 关键类建议

| 类名 | 作用 |
| --- | --- |
| `SecurityConfig` | Security 过滤链配置 |
| `JwtTokenService` | 访问令牌签发与解析 |
| `AuthenticationApplicationService` | 登录、退出、账号状态校验与主用户上下文装配 |
| `JwtPrincipalAuthenticationConverter` | 将 JWT 声明转换为认证主体 |

### 5.2 平台治理模块

- `PlatformConfigAppService` 负责当前平台配置读取与即时更新。
- `OrgUnitAppService` 负责学校/学院/课程/班级组织树维护和层级校验。
- `UserAdministrationApplicationService` 负责用户导入、分页查询、详情、作用域身份变更与账号状态管理。
- 用户系统当前已实现“基础资料 + 教务画像 + 组织成员关系 + 平台治理身份”；课程成员角色由 `course_members` 在课程域承接。
- 导入接口采用“先解析 CSV -> 行级校验 -> 行级事务写库 / 局部成功 -> 输出结果报告”的处理模式。

### 5.3 课程与任务模块

#### 5.3.1 课程管理

- 当前课程第一切片围绕 `course_catalogs -> course_offerings -> teaching_classes -> course_members` 展开。
- 创建开课实例时自动创建 COURSE 组织节点，并写入负责教师成员关系。
- 教学班创建时自动创建 CLASS 组织节点。
- 学生当前不能自主选课；课程成员仅允许教师批量添加或导入既有系统用户。
- 助教权限当前采用固定边界：可查看授权教学班成员，不可批量加人或修改班级功能开关。
- 课程归档后禁止新提交，但保留查询历史成绩和提交记录。

#### 5.3.2 任务管理

- 任务编辑分为草稿保存和发布两个动作。
- 发布前必须校验开放时间、截止时间、评分模式、语言配置和测试用例完整性。
- 编程任务至少存在一个默认 `task_language_profile`。

### 5.4 IDE 工作区模块

#### 5.4.1 工作区初始化

- 学员首次进入 IDE 时，按 `task_starter_files` 初始化 `ide_workspaces` 和 `ide_workspace_files`。
- 若任务支持多语言，则按默认语言初始化模板文件。

#### 5.4.2 工作区保存

- 前端每次提交文件变更时调用 `/ide/workspaces/{id}/files`。
- `IdeWorkspaceAppService` 执行文件级 upsert，并递增 `version_no`。
- 保存失败时写入 `save_failed` 状态，供前端恢复提示。

#### 5.4.3 工作区快照

- 试运行和正式提交都必须先生成快照。
- 快照一经生成不可修改，只能追加新快照。
- 快照文件保存到对象存储，数据库仅存元数据与哈希。

### 5.5 在线运行模块

#### 5.5.1 运行创建

- `IdeRunController` 接收运行请求。
- `RunAppService` 检查任务开放窗口、语言配置与工作区归属。
- 创建 `sandbox_runs` 记录后写入 `stream:sandbox-run`。

#### 5.5.2 运行回写

- `judge-worker` 消费消息，调用 `go-judge` 执行。
- 结果映射为 `sandbox_runs.status`、`stdout_text`、`stderr_text`、`compile_output`、`time_ms`、`memory_kb`。
- 试运行结果不进入成绩计算，不改变 `submissions` 状态。

### 5.6 正式提交模块

#### 5.6.1 提交受理

- `SubmissionAppService` 依次校验课程成员、任务状态、截止时间、提交次数、文件大小。
- 保存工作区快照。
- 写入 `submissions` 和 `submission_files`。
- 写入审计日志。
- 提交 `submission.accepted` 消息至 `stream:submission-judge`。

#### 5.6.2 并发控制

- 同一学员同一任务的正式提交在受理阶段加 Redis 分布式锁。
- 受理失败不扣减提交次数。
- 若快照已写入但提交未落库，补偿任务应清理孤儿快照。

### 5.7 判题中心

#### 5.7.1 `go-judge` 适配器设计

| 类名 | 作用 |
| --- | --- |
| `GoJudgeClient` | 调用 `go-judge` REST API |
| `CompileCommandBuilder` | 根据语言模板构造编译请求 |
| `RunCommandBuilder` | 构造用例执行请求 |
| `JudgeResultNormalizer` | 将原始结果转为平台统一结构 |

#### 5.7.2 评测流程

1. Worker 读取 `submission.accepted` 消息。
2. 查询提交快照、语言配置和隐藏用例。
3. 对编译型语言先执行编译，取回缓存 `fileId`。
4. 逐个隐藏用例执行，累计得分和测试点结果。
5. 归一化结果写入 `judge_runs`。
6. 更新 `submissions.current_judge_run_id` 和状态。
7. 投递通知消息。

#### 5.7.3 重评

- 重评不覆盖旧记录，而是创建新的 `judge_runs`。
- 最新成功评测结果写回 `submissions.current_judge_run_id`。
- 所有重评动作必须写审计日志。

### 5.8 批改与成绩模块

#### 5.8.1 人工批改

- `ReviewAppService` 保存评语、Rubric 快照和人工分。
- 一次提交允许多次批改记录，默认最新一条为当前有效记录。

#### 5.8.2 成绩生成

- `GradeAppService` 根据自动分、人工分和权重生成最终成绩。
- 未完成必要批改时，不允许发布成绩。
- 撤回成绩只改变显示状态，不删除历史记录。

### 5.9 通知与公告模块

- 站内通知优先同步写库，异步扩展消息通道。
- 公告由管理员发布，按组织或课程范围投递。
- 同一业务事件 5 分钟内默认不重复发送同类通知。

## 6. 核心数据结构

### 6.1 工作区文件节点

```java
public record WorkspaceFileNode(
    String path,
    String kind,
    String language,
    String content,
    String hash,
    Boolean readonly
) {}
```

### 6.2 试运行任务载荷

```java
public record RunJobPayload(
    String runId,
    String workspaceId,
    String taskId,
    String userId,
    String languageProfileId,
    String stdin,
    List<WorkspaceFilePayload> files,
    ResourceLimitPayload limits
) {}
```

### 6.3 正式评测任务载荷

```java
public record JudgeJobPayload(
    String judgeRunId,
    String submissionId,
    String snapshotId,
    String languageProfileId,
    List<String> testcaseIds,
    Boolean useCompileCache
) {}
```

### 6.4 归一化测试点结果

```java
public record NormalizedCaseResult(
    String testcaseId,
    String verdict,
    BigDecimal score,
    Integer timeMs,
    Integer memoryKb,
    String stdoutPreview,
    String stderrPreview
) {}
```

## 7. 状态机设计

### 7.1 工作区保存状态机

| 当前状态 | 事件 | 下一状态 |
| --- | --- | --- |
| `ready` | 编辑文件 | `dirty` |
| `dirty` | 开始保存 | `saving` |
| `saving` | 保存成功 | `ready` |
| `saving` | 保存失败 | `save_failed` |
| `save_failed` | 用户重试 | `saving` |

### 7.2 运行会话状态机

| 当前状态 | 事件 | 下一状态 |
| --- | --- | --- |
| `queued` | Worker 开始执行 | `running` |
| `running` | 运行成功 | `success` |
| `running` | 超时 | `timeout` |
| `running` | 编译失败 / 运行失败 / 系统失败 | `failed` |

### 7.3 提交状态机

| 当前状态 | 事件 | 下一状态 |
| --- | --- | --- |
| `accepted` | 投递评测队列 | `queued` |
| `queued` | 开始评测 | `evaluating` |
| `evaluating` | 评测成功 | `evaluated` |
| `evaluating` | 评测超时 / 失败 | `failed` |
| `failed` | 重新评测 | `queued` |

### 7.4 成绩状态机

| 当前状态 | 事件 | 下一状态 |
| --- | --- | --- |
| `pending` | 生成成绩 | `unpublished` |
| `unpublished` | 发布 | `published` |
| `published` | 撤回 | `withdrawn` |
| `withdrawn` | 再次发布 | `published` |

## 8. 异常处理设计

| 异常场景 | 处理策略 |
| --- | --- |
| 登录失败次数超限 | 锁定账号，返回统一错误码，写入审计 |
| 工作区自动保存失败 | 保留最近成功版本，前端提示用户手动保存或重试 |
| 提交超时或超过次数 | 拒绝受理，不创建正式提交记录 |
| 对象存储快照写入失败 | 回滚事务并返回可重试错误 |
| Redis Stream 投递失败 | 写入告警并由补偿任务重试 |
| `go-judge` 返回编译 / 运行错误 | 归一化为运行结果或评测结果，不抛给前端原始沙箱字段 |
| 编译缓存清理失败 | 记录告警并由后台清理任务补偿 |
| 成绩发布时批改缺失 | 阻止发布并提示缺少人工评分或权重配置 |

## 9. 定时任务与异步任务

| 任务 | 触发方式 | 作用 |
| --- | --- | --- |
| 任务自动关闭 | `@Scheduled` | 到达截止时间后关闭任务 |
| 工作区草稿压缩 | `@Scheduled` | 清理旧版本草稿，保留最近可恢复版本 |
| 在线运行消费 | Redis Stream 消费组 | 消费试运行队列并写回 `sandbox_runs` |
| 正式评测消费 | Redis Stream 消费组 | 消费提交队列并写回 `judge_runs` |
| 缓存文件清理 | `@Scheduled` | 清理 `go-judge` 缓存产物和过期文件 |
| 通知补发 | `@Scheduled` | 补发失败通知 |
| 数据归档 | `@Scheduled` | 清理过期通知、归档历史日志 |

## 10. 日志与审计点

- 登录、退出、失败登录、密码修改
- 用户导入、角色调整、平台配置发布
- 课程创建、任务发布、语言配置变更、任务关闭
- 工作区运行、正式提交、重评、成绩发布、成绩撤回
- 导出成绩、导出提交、导出审计日志

## 11. 与编码直接相关的约束

- 所有接口 DTO 必须独立定义，禁止直接暴露 Entity。
- 所有状态流转必须通过 Application Service 或 Domain Service 封装，不允许在 Controller 中直接改状态。
- Mapper 仅负责持久化，不承载业务判断。
- 文件上传和快照固化统一走对象存储适配器，禁止业务模块直接访问本地磁盘。
- 所有 `go-judge` 原始响应必须先归一化，再返回给前端或写入正式结果表。
- 正式提交一旦创建，其对应快照不得被修改或覆盖。
