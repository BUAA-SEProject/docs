# 后端文档

## 1. 模块目录建议

```text
src/
  modules/
    auth/
    admin/
    courses/
    tasks/
    ide/
    submissions/
    judge/
    grades/
    notifications/
    analytics/
  common/
    guards/
    interceptors/
    filters/
    decorators/
  prisma/
  queue/
  adapters/
```

## 2. 服务分层

| 层次 | 职责 |
| --- | --- |
| Controller | 参数校验、权限入口、响应组装 |
| Service | 业务规则、状态流转、事务协调 |
| Repository | 数据访问与查询封装 |
| Adapter | 对接 Redis、S3 存储、`go-judge`、OIDC、消息通道 |

## 3. 模块职责

- `auth`：登录、会话、密码修改、当前用户、OIDC 登录回调。
- `admin`：平台配置、组织、用户导入、角色与账号管理。
- `courses`：课程、成员、资源、邀请码、章节结构。
- `tasks`：任务、语言配置、测试用例、模板工程、Rubric、规则校验。
- `ide`：工作区初始化、文件保存、快照生成、试运行。
- `submissions`：正式提交创建、提交历史、提交快照和文件管理。
- `judge`：投递评测任务、调用 `go-judge`、接收结果、重评。
- `grades`：人工批改、成绩计算、发布、导出、复核。
- `notifications`：站内通知、公告、已读管理。
- `analytics`：平台概览、课程概览、审计查询。

## 4. 中间件与横切能力

| 能力 | 实现建议 |
| --- | --- |
| 认证 | 会话 Guard + OIDC 回调适配 |
| 平台角色授权 | `RolesGuard` |
| 课程角色授权 | 业务服务层 + 自定义 Decorator |
| 请求日志 | 全局 Interceptor 注入 `requestId` |
| 错误处理 | 全局 Exception Filter |
| DTO 校验 | `class-validator` / `zod` 统一校验 |

## 5. 事务与幂等

- 课程创建、任务发布、成绩发布等关键写操作必须走数据库事务。
- 工作区保存采用“文件级 upsert + 版本号递增”策略。
- 正式提交采用“快照固化成功后再创建提交”的两阶段处理。
- 提交创建成功后再异步投递评测，避免“队列有任务但数据库无记录”。
- 重新评测、导入用户等批处理接口应支持幂等键或去重规则。

## 6. 安全与审计

- 密码采用强哈希算法存储。
- 所有导出、角色变更、成绩发布、重评操作必须进入审计日志。
- 上传文件必须校验 MIME、后缀、大小和病毒扫描扩展点。
- `go-judge` 访问地址、认证令牌和存储密钥只允许从环境变量读取。
- IDE 工作区接口必须校验课程成员关系和任务开放窗口。

## 7. 查询与性能

- 列表接口默认分页，禁止无界查询。
- 课程概览、平台概览等统计接口优先使用聚合 SQL 或物化统计表。
- 高并发路径优先缓存只读元数据，如平台配置、课程基础信息和任务语言配置。
- 编译型语言在 Worker 内优先复用 `go-judge` 编译缓存，避免重复编译。
