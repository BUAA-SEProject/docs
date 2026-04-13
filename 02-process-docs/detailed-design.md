# 软件详细设计说明书

## 1. 文档信息

- 文档名称：在线教学与实训平台软件详细设计说明书
- 版本：v1.1
- 状态：设计基线
- 更新日期：2026-04-13
- 编写依据：SRS v4.1、概要设计说明书 v1.1、模块地图、API 设计草案
- 参考标准：IEEE 1016-2009

## 2. 代码仓与目录建议

```text
seproject/
  apps/
    platform-web/
    platform-api/
    judge-worker/
  packages/
    shared-types/
    shared-config/
  infra/
    docker/
    sql/
    grafana/
    gojudge/
  docs/
```

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

### 4.1 模块划分

| 模块 | Controller | Service | Repository / Adapter |
| --- | --- | --- | --- |
| Auth | `AuthController` | `AuthService` | `UserRepo`, `SessionRepo`, `OidcAdapter` |
| Admin | `PlatformController`, `UserController`, `OrgController` | `PlatformService`, `UserService`, `OrgService` | `PlatformRepo`, `OrgRepo`, `AuditRepo` |
| Course | `CourseController`, `CourseMemberController`, `ResourceController` | `CourseService`, `MemberService`, `ResourceService` | `CourseRepo`, `MemberRepo`, `StorageAdapter` |
| Task | `TaskController`, `TaskCaseController`, `TaskLanguageController`, `RubricController` | `TaskService`, `RuleService`, `LanguageProfileService` | `TaskRepo`, `LanguageRepo`, `RubricRepo` |
| IDE Workspace | `IdeWorkspaceController`, `IdeRunController` | `WorkspaceService`, `RunService` | `WorkspaceRepo`, `SnapshotRepo`, `QueueAdapter` |
| Submission | `SubmissionController` | `SubmissionService` | `SubmissionRepo`, `SnapshotRepo`, `StorageAdapter`, `QueueAdapter` |
| Judge | `JudgeAdminController` | `JudgeDispatchService`, `JudgeResultService` | `GoJudgeAdapter`, `JudgeRunRepo` |
| Review | `ReviewController`, `GradeController` | `ReviewService`, `GradeService` | `ReviewRepo`, `GradeRepo` |
| Notification | `NotificationController`, `AnnouncementController` | `NotificationService` | `NotificationRepo`, `MessageAdapter` |
| Analytics | `DashboardController`, `AuditController` | `DashboardService`, `AuditService` | `MetricsRepo`, `AuditRepo` |

### 4.2 权限检查

- 平台级权限：管理员、运维角色访问 `/admin/*`。
- 课程级权限：教师、助教、学员通过 `course_members` 判定课程内角色。
- 资源级权限：工作区、提交、成绩、通知等对象必须再次检查所属课程与操作者关系。
- 工作区级权限：`ide_workspaces` 仅所属学员本人和具备查看权限的教师 / 助教可访问只读快照。

## 5. 关键模块详细设计

### 5.1 认证与会话

- 登录流程：用户名 / 学号 + 密码 -> 校验账号状态 -> 生成会话 -> 写入审计日志。
- 会话存储：Redis 持久化会话索引，Cookie 保存会话 ID。
- 若启用 Keycloak，则由 OIDC 适配器完成 code exchange，并回填平台内用户映射。

### 5.2 任务与语言配置

- 任务状态：`draft`、`published`、`closed`
- 每个编程任务至少配置一个 `task_language_profile`，描述语言、编译命令、运行命令、入口文件、时间 / 内存限制。
- 模板工程通过 `task_starter_files` 保存，可包含多文件目录结构。
- 测试用例分为公开样例和隐藏用例，公开样例可被在线运行复用。

### 5.3 IDE 工作区

- 学员首次进入 IDE 时，系统按 `task_starter_files` 初始化 `ide_workspaces` 和 `ide_workspace_files`。
- 工作区文件操作支持新建、编辑、删除、重命名、恢复模板文件。
- 每次成功保存都会递增工作区版本号，并更新 `last_saved_at`。
- 工作区仅保存“当前草稿”，不直接作为正式提交依据。

### 5.4 在线运行

- 学员点击运行后，API 创建 `sandbox_runs` 记录，状态置为 `queued`。
- Worker 从队列读取当前工作区快照，构造 `go-judge` 运行请求并下发至 `/run`。
- 试运行默认只允许使用公开样例或学员自定义输入，不读取隐藏用例。
- 运行结果仅写入 `sandbox_runs`，不生成成绩、不变更 `submissions`。

### 5.5 正式提交

- 提交前先检查课程成员、任务状态、截止时间、提交次数和文件大小。
- 提交时先将工作区固化为 `workspace_snapshots`，再写入 `submissions`。
- 提交快照中的文件写入对象存储；`submission_files` 保存文件路径、对象键、哈希和大小。
- 自动评测任务在事务提交后发布 `submission.accepted` 事件。

### 5.6 判题中心

- Worker 消费 `submission.accepted` 事件，读取提交快照与语言配置。
- 对编译型语言，先发起一次编译请求，通过 `copyOutCached` 取得编译产物 `fileId`。
- 隐藏用例执行阶段复用编译产物 `fileId`，逐个下发运行请求，减少重复编译开销。
- 评测完成后主动删除临时缓存文件，避免 `fileId` 泄漏占用共享内存。
- 结果归一化字段包括：编译状态、运行状态、总分、每个测试点结果、标准输出摘要、错误摘要、时间和内存峰值。
- 重评逻辑不覆盖历史结果，而是追加新的 `judge_runs` 并更新当前有效结果引用。

### 5.7 批改与成绩

- 人工批改记录以追加方式保存，成绩表保留当前有效成绩。
- 混合评分 = 自动评测分 * 自动权重 + 人工评分 * 人工权重。
- 成绩发布与撤回均写入审计日志和通知事件。
- 复核记录不直接修改原始批改记录，而是追加 `grade_rechecks` 并触发重新确认。

## 6. 核心数据结构

### 6.1 工作区文件节点

```ts
type WorkspaceFileNode = {
  path: string;
  kind: 'file' | 'dir';
  language?: string;
  content?: string;
  hash?: string;
  readonly?: boolean;
};
```

### 6.2 试运行任务载荷

```ts
type RunJobPayload = {
  runId: string;
  workspaceId: string;
  taskId: string;
  userId: string;
  languageProfileId: string;
  stdin: string;
  files: Array<{ path: string; content: string }>;
  limits: {
    cpuTimeMs: number;
    clockTimeMs: number;
    memoryMb: number;
    outputKb: number;
  };
};
```

### 6.3 正式评测任务载荷

```ts
type JudgeJobPayload = {
  judgeRunId: string;
  submissionId: string;
  snapshotId: string;
  languageProfileId: string;
  testcaseIds: string[];
  useCompileCache: boolean;
};
```

### 6.4 归一化测试点结果

```ts
type NormalizedCaseResult = {
  testcaseId: string;
  verdict:
    | 'accepted'
    | 'wrong_answer'
    | 'compile_error'
    | 'runtime_error'
    | 'time_limit_exceeded'
    | 'memory_limit_exceeded'
    | 'output_limit_exceeded'
    | 'system_error';
  score: number;
  timeMs: number;
  memoryKb: number;
  stdoutPreview?: string;
  stderrPreview?: string;
};
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
| `go-judge` 返回编译 / 运行错误 | 归一化为运行结果或评测结果，不抛给前端原始沙箱字段 |
| 编译缓存清理失败 | 记录告警并由后台清理任务补偿 |
| 成绩发布时批改缺失 | 阻止发布并提示缺少人工评分或权重配置 |

## 9. 定时任务与异步任务

| 任务 | 触发方式 | 作用 |
| --- | --- | --- |
| 任务自动关闭 | 定时任务 | 到达截止时间后关闭任务 |
| 工作区草稿压缩 | 定时任务 | 清理旧版本草稿，保留最近可恢复版本 |
| 在线运行消费 | Worker 调度 | 消费试运行队列并写回 `sandbox_runs` |
| 正式评测消费 | Worker 调度 | 消费提交队列并写回 `judge_runs` |
| 缓存文件清理 | 定时任务 | 清理 `go-judge` 缓存产物和过期文件 |
| 通知补发 | 重试队列 | 补发失败通知 |
| 数据归档 | 定时任务 | 清理过期通知、归档历史日志 |

## 10. 日志与审计点

- 登录、退出、失败登录、密码修改
- 用户导入、角色调整、平台配置发布
- 课程创建、任务发布、语言配置变更、任务关闭
- 工作区运行、正式提交、重评、成绩发布、成绩撤回
- 导出成绩、导出提交、导出审计日志

## 11. 与编码直接相关的约束

- 所有接口 DTO 必须独立定义，禁止直接暴露 ORM 实体。
- 所有状态流转必须通过服务层方法封装，不允许在控制器中直接改状态。
- 文件上传和快照固化统一走对象存储适配器，禁止业务模块直接访问本地磁盘。
- 所有 `go-judge` 原始响应必须先归一化，再返回给前端或写入正式结果表。
- 正式提交一旦创建，其对应快照不得被修改或覆盖。
