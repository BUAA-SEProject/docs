# 工程规范

## 1. 适用范围

本规范适用于 AUBB 当前代码仓库中的后端、文档与接口设计工作，目标是保证实现、测试、文档与需求口径长期一致。

## 2. 基本原则

1. 先锁范围再写代码，默认只交付当前阶段的 `MUST` 需求。
2. 默认采用 TDD：先写失败测试，再做最小实现，再在测试通过后重构。
3. 代码、测试、文档必须同轮更新，禁止“先实现、后补文档”。
4. 平台治理身份与课程成员角色分开建模，避免过早耦合课程域。
5. 全局文档只保留长期有效资产，不在 `docs/` 根目录保留过程性内容。

## 3. 分支与提交

- `main`：稳定演示与交付基线
- `dev`：日常集成分支
- `feature/*`：功能开发
- `fix/*`：缺陷修复
- `docs/*`：文档专项修改

提交信息建议采用 Conventional Commits 风格，例如：

- `feat: add scoped user detail api`
- `fix: enforce expired account login rejection`
- `docs: align user system workflow`

## 4. 代码规范

- 当前后端以 Java 25 + Spring Boot 4 为基线。
- 包结构默认采用“模块优先、模块内分层”：`modules.<module>.{api,application,domain,infrastructure}`，共享能力仅保留在 `common`、`config` 和 `infrastructure.persistence`。
- DTO、Entity、View/VO 分离，不直接把数据库实体暴露给接口层。
- 复杂业务逻辑写在应用层或领域层，不写在 Controller。
- 非显而易见的实现应添加简洁中文注释，说明业务意图、边界条件或设计原因。

## 5. 格式化与静态约束

- Java 代码统一使用 `spotless` 格式化。
- 默认命令：
  - `./mvnw spotless:apply`
  - `./mvnw test`
  - `./mvnw verify`
- 提交前至少完成一次格式化与测试验证。

## 6. TDD 与测试门禁

- 领域规则、权限边界、账号状态、审计行为和关键 API 默认都要先写测试。
- 登录失败锁定、禁用/失效账号限制、默认会话时长等安全规则必须有自动化测试。
- 关键治理接口优先采用集成测试覆盖真实鉴权、Flyway 与数据库访问。
- 数据库相关验证优先使用 Testcontainers，而不是依赖本机手工环境。

## 7. Skills 与执行计划

- 多步骤或高风险任务必须建立执行计划，并记录目标、范围、风险、验证路径与关键决策。
- 推荐技能组合：
  - Spring Boot 功能开发：`springboot-patterns` + `springboot-tdd`
  - 安全与认证：`springboot-security`
  - 文档更新：`documentation-writer`
  - 架构决策：`architecture-decision-records`
- 过程性工作记忆保留在仓库根目录 `task_plan.md`、`findings.md`、`progress.md`，不进入 `docs/` 根目录。

## 8. 文档同步规则

- 架构边界变化：同步更新 `ARCHITECTURE.md`、设计文档与质量说明。
- 认证、权限、API、数据库变化：同步更新仓库文档与 `../docs/05-api`、`../docs/04-development`、`../docs/02-process-docs` 中对应内容。
- 若实现与系统级文档存在阶段性差异，必须写明“当前实现”和“后续扩展位”。

## 9. 数据库与安全

- 所有结构变更必须通过 Flyway。
- 密码必须采用强哈希算法存储。
- JWT 密钥、数据库口令、第三方令牌等敏感配置不得入库或提交到仓库。
- 导入、身份变更、账号状态变更、配置修改等治理动作必须写审计。
