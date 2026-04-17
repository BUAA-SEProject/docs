# 后端文档

## 1. 当前技术基线

- 运行时：Spring Boot 4 + Java 25
- 持久化：PostgreSQL + Flyway + MyBatis-Plus
- 认证：Spring Security + JWT Resource Server
- 目标基础设施：RabbitMQ、Redis
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

- `identityaccess`：登录、退出、当前用户、JWT、用户、账号状态、平台治理身份、作用域授权
- `course`：学期、课程模板、开课实例、教学班、课程成员、班级功能开关
- `organization`：学校/学院/课程/班级组织树维护与查询
- `platformconfig`：单份平台配置读取与即时更新
- `audit`：关键治理动作审计写入与查询

## 5. 认证与授权约定

- 当前后端使用无状态 JWT，不再使用服务端 Session。
- 平台治理身份使用作用域模型：
  - `SCHOOL_ADMIN`
  - `COLLEGE_ADMIN`
  - `COURSE_ADMIN`
  - `CLASS_ADMIN`
- 教师在平台治理阶段仍可临时映射为 `CLASS_ADMIN`。
- 课程成员角色已在课程域单独建模，不与平台治理身份混用。

## 6. 用户系统边界

当前用户系统由三部分组成：

1. 用户基础资料：登录标识、显示名、邮箱、手机号、默认归属组织、账号生命周期字段。
2. 平台治理身份：按组织作用域分配的管理员身份。
3. 课程成员角色：由课程域承接教师、助教、学员关系。

当前管理接口应支持：

- 用户分页列表
- 用户详情
- 默认归属组织摘要
- 生命周期信息：启用、停用、锁定、失效、最近登录
- 治理身份查看与更新

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
