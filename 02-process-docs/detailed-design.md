# 软件详细设计说明书

## 1. 文档信息

- 文档名称：在线教学与实训平台软件详细设计说明书
- 版本：v1.0
- 状态：设计基线
- 更新日期：2026-04-13
- 编写依据：SRS v4.0、概要设计说明书 v1.0、模块地图、API 设计草案
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
    eslint-config/
  infra/
    docker/
    sql/
    grafana/
  docs/
```

## 3. 前端详细设计

### 3.1 路由结构

| 路由前缀 | 页面 | 权限 |
| --- | --- | --- |
| `/login` | 登录页 | 匿名 |
| `/student/courses` | 学员课程列表 | 学员 |
| `/student/courses/:courseId/tasks/:taskId` | 学员任务详情 / 提交页 | 学员 |
| `/teacher/courses` | 教师课程列表 | 教师/助教 |
| `/teacher/courses/:courseId/tasks/new` | 任务创建页 | 教师 |
| `/teacher/submissions/:submissionId` | 提交详情与批改页 | 教师/助教 |
| `/admin/config` | 平台配置 | 管理员 |
| `/admin/users` | 用户与组织管理 | 管理员 |
| `/admin/audit` | 审计日志 | 管理员/运维 |

### 3.2 状态管理模块

| Store | 负责状态 |
| --- | --- |
| `authStore` | 当前用户、角色、登录态、菜单权限 |
| `courseStore` | 课程列表、课程详情、成员、资源 |
| `taskStore` | 任务详情、提交规则、Rubric、用例配置 |
| `submissionStore` | 提交列表、当前提交、评测状态 |
| `gradeStore` | 批改记录、成绩单、复核状态 |
| `adminStore` | 平台配置、用户、组织、审计统计 |

### 3.3 页面交互规则

- 所有高风险写操作必须经过二次确认。
- 提交页必须显示截止时间、剩余次数、支持语言和文件限制。
- 批改页左侧显示提交信息与评测结果，右侧显示 Rubric 和评语编辑区。
- 平台概览页默认展示今日活跃用户、提交量、评测通过率和失败任务 TopN。

## 4. 后端详细设计

### 4.1 模块划分

| 模块 | Controller | Service | Repository / Adapter |
| --- | --- | --- | --- |
| Auth | `AuthController` | `AuthService` | `UserRepo`, `SessionRepo` |
| Admin | `PlatformController`, `UserController`, `OrgController` | `PlatformService`, `UserService`, `OrgService` | `PlatformRepo`, `OrgRepo`, `AuditRepo` |
| Course | `CourseController`, `CourseMemberController`, `ResourceController` | `CourseService`, `MemberService`, `ResourceService` | `CourseRepo`, `MemberRepo`, `FileAdapter` |
| Task | `TaskController`, `TaskCaseController`, `RubricController` | `TaskService`, `RuleService` | `TaskRepo`, `RubricRepo` |
| Submission | `SubmissionController` | `SubmissionService` | `SubmissionRepo`, `StorageAdapter`, `QueueAdapter` |
| Judge | `JudgeController` | `JudgeDispatchService`, `JudgeResultService` | `JudgeAdapter`, `JudgeRunRepo` |
| Review | `ReviewController`, `GradeController` | `ReviewService`, `GradeService` | `ReviewRepo`, `GradeRepo` |
| Notification | `NotificationController`, `AnnouncementController` | `NotificationService` | `NotificationRepo`, `MessageAdapter` |
| Analytics | `DashboardController`, `AuditController` | `DashboardService`, `AuditService` | `MetricsRepo`, `AuditRepo` |

### 4.2 权限检查

- 平台级权限：管理员、运维角色访问 `/admin/*`。
- 课程级权限：教师、助教、学员通过 `course_members` 判定课程内角色。
- 资源级权限：提交、成绩、通知等对象必须再次检查所属课程与操作者关系。

## 5. 关键模块详细设计

### 5.1 认证与会话

- 登录流程：用户名/学号 + 密码 -> 校验账号状态 -> 生成会话 -> 写入审计日志。
- 会话存储：Redis 持久化会话索引，Cookie 保存会话 ID。
- 权限中间件：先校验登录态，再校验平台角色，最后在业务服务层校验课程角色。

### 5.2 课程管理

- 课程状态：`draft`、`active`、`archived`
- 创建课程必须写入负责教师，并自动创建教师成员关系。
- 邀请码采用随机短码，具备生效时间和失效时间。

### 5.3 任务管理

- 任务状态：`draft`、`published`、`closed`
- 任务说明支持 Markdown，附件通过对象存储引用。
- 测试用例采用独立表保存，支持公开样例与隐藏用例。

### 5.4 提交中心

- 提交创建时先检查课程成员、任务状态、截止时间、次数和文件大小。
- 受理成功后写入 `submissions`，若含文件则写入 `submission_files`。
- 自动评测任务会在事务提交后发布 `submission.accepted` 事件。

### 5.5 判题中心

- Worker 消费 `submission.accepted` 事件，构造 Judge0 请求。
- 结果归一化字段包括：编译状态、运行状态、总分、每个测试点结果、标准输出摘要、错误摘要。
- 重评逻辑不覆盖历史结果，而是追加新的 `judge_runs` 并更新当前有效结果引用。

### 5.6 批改与成绩

- 人工批改记录以追加方式保存，成绩表保留当前有效成绩。
- 混合评分 = 自动评测分 * 自动权重 + 人工评分 * 人工权重。
- 成绩发布与撤回均写入审计日志和通知事件。

## 6. 状态机设计

### 6.1 提交状态机

| 当前状态 | 事件 | 下一状态 |
| --- | --- | --- |
| `accepted` | 开始评测 | `evaluating` |
| `evaluating` | 评测成功 | `evaluated` |
| `evaluating` | 评测超时/失败 | `failed` |
| `failed` | 重新评测 | `evaluating` |

### 6.2 成绩状态机

| 当前状态 | 事件 | 下一状态 |
| --- | --- | --- |
| `pending` | 生成成绩 | `unpublished` |
| `unpublished` | 发布 | `published` |
| `published` | 撤回 | `withdrawn` |
| `withdrawn` | 再次发布 | `published` |

## 7. 异常处理设计

| 异常场景 | 处理策略 |
| --- | --- |
| 登录失败次数超限 | 锁定账号，返回统一错误码，写入审计 |
| 提交超时或超过次数 | 拒绝受理，不创建提交记录 |
| 对象存储上传失败 | 终止事务，返回可重试错误 |
| Judge0 返回异常 | 标记 `judge_runs` 失败，可手动重评 |
| 成绩发布时批改缺失 | 阻止发布并提示缺少人工评分或权重配置 |

## 8. 定时任务与异步任务

| 任务 | 触发方式 | 作用 |
| --- | --- | --- |
| 任务自动关闭 | 定时任务 | 到达截止时间后关闭任务 |
| 评测结果轮询 | Worker 调度 | 拉取 Judge0 执行结果 |
| 通知补发 | 重试队列 | 补发失败通知 |
| 数据归档 | 定时任务 | 清理过期通知、归档历史日志 |

## 9. 日志与审计点

- 登录、退出、失败登录、密码修改
- 用户导入、角色调整、平台配置发布
- 课程创建、任务发布、任务关闭
- 提交创建、重评、成绩发布、成绩撤回
- 导出成绩、导出提交、导出审计日志

## 10. 与编码直接相关的约束

- 所有接口 DTO 必须独立定义，禁止直接暴露 ORM 实体。
- 所有状态流转必须通过服务层方法封装，不允许在控制器中直接改状态。
- 文件上传统一走对象存储适配器，禁止业务模块直接访问本地磁盘。
- 判题结果统一经过归一化，前端不直接依赖第三方判题原始字段。
