# 后端文档

## 1. 当前技术基线

- 运行时：Spring Boot 4 + Java 25
- 持久化：PostgreSQL + Flyway + MyBatis-Plus
- 认证：Spring Security + JWT Bearer access token + opaque refresh token
- 消息队列：RabbitMQ（评测队列第一阶段）
- 对象存储：MinIO
- 评测执行：go-judge（集成在应用内）
- 测试：JUnit 5 + MockMvc + Testcontainers

## 2. 当前推荐包结构

```text
com.aubb.server
  ├─ modules
  │   ├─ identityaccess
  │   │   ├─ api
  │   │   ├─ application
  │   │   ├─ domain
  │   │   └─ infrastructure
  │   ├─ course
  │   ├─ assignment
  │   ├─ submission
  │   ├─ grading
  │   ├─ judge
  │   ├─ lab
  │   ├─ notification
  │   ├─ organization
  │   ├─ platformconfig
  │   └─ audit
  ├─ common
  ├─ config
  ├─ infrastructure
  │   └─ persistence
```

## 3. 分层职责

| 层次 | 职责 |
| --- | --- |
| `modules.<module>.api` | 协议适配、参数校验、权限入口、响应输出 |
| `modules.<module>.application` | 业务编排、事务控制、作用域授权、审计协同 |
| `modules.<module>.domain` | 规则校验、层级约束、密码策略、角色策略 |
| `modules.<module>.infrastructure` | 模块内 Mapper、Entity、外部适配 |
| `common / config / infrastructure.persistence` | 跨模块共享模型、框架配置和持久化公共适配 |

## 4. 当前核心模块

- `identityaccess`：登录、退出、当前用户、JWT、用户创建/导入/查询/详情/状态管理、教务画像与组织成员关系、平台治理身份、密码策略、作用域授权
- `course`：学期、课程模板、开课实例、教学班、课程成员、班级功能开关
- `assignment`：作业创建、列表、详情、状态流转、题库管理、结构化试卷快照、脚本型自动评测配置
- `submission`：正式提交受理、分题答案与评分摘要、提交附件上传/关联/下载
- `grading`：人工批改、成绩发布、学生侧人工评分可见性控制、教师侧与学生侧成绩册、申诉
- `judge`：评测作业入队、go-judge 适配、RabbitMQ 队列、评测结果回写、评测报告、教师重排队
- `lab`：教学班级实验定义、实验报告草稿/提交/评阅/发布、实验报告附件
- `notification`：站内通知入箱、收件状态与未读数、关键教学事件 fan-out
- `organization`：学校/学院/课程/班级组织树维护与查询
- `platformconfig`：单份即时生效的平台配置读取与更新
- `audit`：关键治理动作审计写入与查询

## 5. 认证与授权约定

- 当前后端使用 JWT Bearer access token，受保护请求除验签外还会按 `sid` 回查 `auth_sessions` 与当前用户状态。
- refresh token 使用 opaque token，仅保存 hash。
- 平台治理身份使用作用域模型：
  - `SCHOOL_ADMIN`
  - `COLLEGE_ADMIN`
  - `COURSE_ADMIN`
  - `CLASS_ADMIN`
- 教师在平台治理阶段仍可临时映射为 `CLASS_ADMIN`。
- 课程成员角色已在课程域单独建模（`course_members`），不与平台治理身份混用。
- `logout`、`/api/v1/auth/revoke`、管理员强制失效和账号停用都会让旧会话即时失效。

## 6. 用户系统边界

当前用户系统由三部分组成：

1. 用户基础资料（`users`）：登录标识、显示名、邮箱、手机号、默认归属组织、账号生命周期字段。
2. 教务画像（`academic_profiles`）：学号/工号、真实姓名、画像状态与身份类型。
3. 组织成员关系（`user_org_memberships`）：业务成员归属。
4. 平台治理身份（`user_scope_roles`）：按组织作用域分配的管理员身份。
5. 课程成员角色（`course_members`）：教师、助教、学员等课程域角色。

## 7. 横切实现约束

- 权限粗拦截放在 `@PreAuthorize` 或安全配置中。
- 数据作用域校验必须在应用层执行，不能只依赖接口层 authority。
- 列表接口默认分页，禁止无界查询。
- 审计记录由应用层统一写入，不散落在 Controller。
- 数据库结构变化只通过 Flyway 迁移进入仓库。

## 8. 默认验证命令

- `./mvnw spotless:apply`
- `./mvnw test`
- `./mvnw verify`
