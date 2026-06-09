# AUBB 完整产品验收报告

## 1. 验收元信息

- 验收时间：2026-06-09 16:10 CST 起
- 工作区：`/Users/moorefoss/Code/AUBB`
- 前端地址：`http://127.0.0.1:3000`
- 后端地址：`http://127.0.0.1:18080`
- 测试账号：管理员 `U-SA1`、教师/助教 `U-TA1`、学生 `U-ST1`；密码来自 `env/e2e.env`，报告不记录凭据值
- 执行人：Codex
- Playwright MCP：已作为用户可见功能主证据，产出 28 张截图
- 初始 `just status` 摘要：2026-06-09 16:08 CST，`server/`、`web/`、`docs/` 均在 `main...origin/main`，dirty entries 均为 0；根目录不是 git 仓库
- 最终 `just status` 摘要：2026-06-09 16:52 CST，`server/`、`web/` dirty entries 均为 0；`docs/` 仅 staged 新增验收报告、证据索引和 28 张截图，共 30 entries；根目录不是 git 仓库

## 2. 验收结论

- 总结论：有条件通过
- 主要依据：本地真实环境、后端/前端/文档非浏览器门禁均通过；`just e2e-real` 50 个真实浏览器用例中 48 个通过；Playwright MCP 复核三角色主页面、越权跳转和关键响应式页面可用。
- P0/P1 摘要：未发现 P0；发现 2 个 P1，分别为学生作业列表主操作文案与 E2E 契约不一致，以及管理员跨学院开课 UI 无法选择共同管理学院。
- 是否建议进入修复阶段：建议先进入修复阶段，优先处理 2 个 P1。
- 是否建议进入演示或答辩彩排：不建议直接进入正式演示彩排；可在说明风险的前提下做内部讲解预演。

## 3. 输入缺失与环境阻塞

- 强制输入文件检查：
  - `goal-test.md`：存在，已阅读。
  - `AGENTS.md`、`AGENTS-shared.md`、`web/AGENTS.md`、`server/AGENTS.md`、`docs/AGENTS.md`：存在，已阅读。
  - `docs/06-testing-and-ops/acceptance-checklist.md`：存在，已阅读。
  - `docs/04-development/frontend-design.md`：存在，已开始检查。
  - `server/docs/stable-api.md`：存在，已阅读稳定接口范围。
  - `server/docs/product-specs/`：存在，包含 assignment、course、grading、judge、lab、notification、permission、platform、submission 等规格。
  - `server/docs/generated/db-schema.md`：存在，待细读。
  - `web/docs/backend-requests.md`：存在，当前无待处理后端工单。
  - `web/src/shared/routing/nav-config.ts`、`web/src/shared/routing/route-access.ts`：存在，已阅读导航与角色区域配置。
  - `web/src/tests/e2e/README.md`：存在，已阅读真实 E2E 环境与账号变量要求。
  - `env/e2e.example`：存在，已阅读。
- `env/e2e.env`：存在，必要变量均有设置标记；未记录任何密码、token 或连接串值。
- 当前环境阻塞：无。仅保留两个产品验收 P1。

## 4. 命令门禁结果

| 命令 | 目的 | 结果 | 关键输出或失败原因 |
| --- | --- | --- | --- |
| `just status` | 初始工作区状态 | 通过 | 三个子仓库均 clean；根目录不是 git 仓库 |
| `just --list` | 统一入口可用性 | 通过 | 可用：`dev-up`、`dev-down`、`healthcheck`、`healthcheck-strict`、`seed-fixtures`、`e2e-real`、`verify`、`verify-full`、`docs-build` |
| `just dev-up` | 启动真实本地依赖、后端和前端 | 通过 | Docker 依赖 `postgres`、`rabbitmq`、`redis`、`minio`、`go-judge` 均 Running；后端 18080、前端 3000 已监听并复用 |
| `just healthcheck-strict` | 严格环境健康检查 | 通过 | `just`、`docker`、`java`、`npm`、`curl` 可用；`env/e2e.env` 存在且严格 E2E 变量已设置；后端 readiness/OpenAPI 与前端 login 均 OK |
| `server/scripts/ops/e2e-residual-cleanup.sh` | E2E/MCP/FULLRUN 前缀残留 dry-run | 通过 | 默认 dry-run，PostgreSQL 命中 0，MinIO object key 0；未执行删除 |
| `just seed-fixtures` | 准备或刷新验收/E2E 数据 | 通过 | 权限/E2E fixture 22/22 passed；`bootstrap=3`、`api=6`、`sql=1`、`reused=46`、`reset=6` |
| `just e2e-real` | 真实前后端 Playwright E2E | 失败 | 50 个用例中 48 passed、2 failed，退出码 1。失败：学生全部作业列表未出现测试期待的“开始做题”链接；完整组织结构跨学院开课 UI 在“共同管理学院”选择处超时 |
| `just verify` | 快速门禁 | 通过 | 后端 quick tests：356 tests，0 failures/errors/skipped，BUILD SUCCESS；web lint 通过；web typecheck 通过；docs VitePress build 通过 |
| `just verify-full` | 完整非浏览器门禁 | 通过 | 后端 verify：356 tests，0 failures/errors/skipped，BUILD SUCCESS；web lint/typecheck 通过；web unit tests：70 files、266 tests 全通过；web `next build` 通过并生成 31 个 app route；docs VitePress build 通过 |
| `cd docs && npm run docs:build` | 文档站构建 | 通过 | VitePress build complete in 3.40s；仅有 Rollup chunk size warning，无构建失败 |

## 5. 产品验收矩阵

| 编号 | 模块 | 验收项 | 状态 | 证据 | 关联问题 |
| --- | --- | --- | --- | --- | --- |
| DOC-01 | 文档 | 计划书、需求、概要设计、详细设计、测试报告、部署文档、用户手册齐全 | 通过 | `docs/02-process-docs/` 下必需交付文档存在；`cd docs && npm run docs:build` 通过 | - |
| DOC-02 | 文档 | API、数据库、前端、后端、判题、LLM 使用说明与系统行为一致 | 失败 | API、数据库、产品规格、前端设计文档存在且可构建；但学生作业列表与跨学院开课行为存在验收偏差 | P1-001、P1-002 |
| ENV-01 | 环境 | 本地前端、后端、数据库、队列、对象存储、缓存、判题服务可启动或阻塞明确 | 通过 | `just dev-up`、`just healthcheck-strict`、`just verify-full` 通过 | - |
| ENV-02 | 数据 | 演示账号、课程、班级、作业、题目、提交、成绩、审计数据可用 | 通过 | `just seed-fixtures` 22/22 passed；MCP 截图覆盖三角色数据页；E2E full coverage 记录课程、作业、提交、成绩、审计数据 | - |
| AUTH-01 | 公共 | 登录、退出、角色路由、无权限跳转和 profile-required 行为正确 | 通过 | `auth.spec.ts` 真实 E2E 覆盖三角色登录、退出、学生越权；MCP 复核教师/学生访问管理端显示“权限不足” | - |
| AUTHZ-01 | 权限 | 管理员、教师、开课助教、班级助教、学生之间权限边界清楚 | 失败 | 越权跳转和后端 401/403 通过；但跨学院开课共同管理学院选择失败，导致作用域授权闭环不完整 | P1-002 |
| ADMIN-01 | 管理员 | 管理员首页能呈现治理状态和关键待办 | 通过 | MCP 截图 `mcp-01-admin-home.png` | - |
| ADMIN-02 | 管理员 | 用户、组织、身份授权、课程、开课、教学班治理可操作 | 失败 | `just e2e-real` 中多数管理员治理用例通过，但 `full-organization-structure.spec.ts` 在新增开课弹窗选择“共同管理学院”时 180s 超时 | P1-002 |
| ADMIN-03 | 管理员 | 权限解释、审计日志、平台配置可访问且可理解 | 通过 | MCP 截图 `mcp-05-admin-auth-explain.png`、`mcp-06-admin-audit-logs.png`、`mcp-07-admin-platform-config.png`；E2E 记录权限解释允许/拒绝/错误输入、审计筛选、平台配置保存恢复 | - |
| TEACHER-01 | 教师 | 教师首页、课程工作区、成员、资源、公告、讨论能支撑教学巡检 | 通过 | MCP 截图 `mcp-08` 到 `mcp-15`；E2E 记录课程成员、资源、公告、讨论移动端与桌面验收 | - |
| TEACHER-02 | 教师 | 题库至少覆盖单选、多选、填空、简答、编程或文件类题目的查看/编辑 | 通过 | `just e2e-real` full coverage 记录单选、多选、简答、文件、编程题创建/筛选/编辑/归档；MCP 截图 `mcp-13-teacher-question-bank.png` | - |
| TEACHER-03 | 教师 | 判题环境、作业创建、编辑、发布、撤回或重新发布语义清楚 | 通过 | E2E 记录判题环境创建/编辑/归档、结构化作业创建/编辑/替换/发布/关闭；MCP 截图 `mcp-10-teacher-assignments.png` | - |
| TEACHER-04 | 教师 | 提交列表、批改、调分、成绩册、发布成绩、导出能形成闭环 | 通过 | E2E 记录提交列表、人工评分、重判、成绩册报告/导出/调分/导入/发布；MCP 截图 `mcp-11-teacher-submissions.png`、`mcp-12-teacher-gradebook.png` | - |
| STUDENT-01 | 学生 | 学生首页、课程、作业、通知、成绩摘要信息一致 | 通过 | MCP 截图 `mcp-17-student-home.png`、`mcp-18-student-courses.png`、`mcp-19-student-assignments.png`、`mcp-22-student-grades.png`、`mcp-24-student-notifications.png` | - |
| STUDENT-02 | 学生 | 作业详情、结构化答题、附件上传、保存草稿和正式提交可完成 | 失败 | `just e2e-real` 中 `full-assignment-judge.spec.ts` 的结构化题/附件/提交闭环通过，但 `assignment-submission.spec.ts` 的学生全部作业列表期待“开始做题”链接失败；页面实际展示“继续作答” | P1-001 |
| STUDENT-03 | 学生 | WebIDE 打开、编辑、保存、运行/提交、返回作业详情行为清楚 | 通过 | `webide-real-flow.spec.ts` 记录教师创建发布 Python3 编程题，学生完成 WebIDE 编辑/保存/历史恢复/重置/样例运行/提交判题并 ACCEPTED | - |
| STUDENT-04 | 学生 | 成绩、提交详情、教师反馈、通知中心对学生可理解 | 通过 | E2E 记录学生成绩查询/导出、提交详情、判题结果、通知已读；MCP 截图 `mcp-22`、`mcp-24` | - |
| TA-01 | 助教 | 开课助教与班级助教的可见范围、可操作范围和禁止动作反馈正确 | 失败 | E2E 权限矩阵与导航越权通过，但跨学院开课失败导致助教跨学院作用域授权链路未能完整 UI 验收 | P1-002 |
| RUNTIME-01 | 运行时 | MinIO 上传下载、RabbitMQ 判题队列、Redis/SSE 通知、PostgreSQL 数据回写可验证 | 通过 | healthcheck 严格通过；E2E 记录附件上传下载、判题队列、SSE notification、成绩/提交/实验数据回写；后端 verify 356 tests 通过 | - |
| LAB-01 | 实验 | 实验列表、实验详情、终端或运行环境、报告提交的可用性或阻塞原因明确 | 通过 | E2E 记录实验创建/发布/关闭、学生报告上传保存提交、教师评阅发布；MCP 截图 `mcp-14-teacher-labs.png`、`mcp-23-student-labs.png` | - |
| NFR-01 | 质量 | 核心流程无明显 5xx、未处理异常、控制台错误或网络错误 | 失败 | `just e2e-real` 有 2 个真实浏览器失败；MCP 控制台仅观察到未登录态预期 401，无新增 5xx 或 pageerror | P1-001、P1-002 |
| NFR-02 | 质量 | 1280x800、1440x900 和一个窄屏视口下关键页面可用 | 通过 | MCP 截图 `mcp-26-responsive-admin-users-1280.png`、`mcp-29-responsive-teacher-labs-1440.png`、`mcp-28-responsive-student-assignments-mobile.png`；E2E `GAP-RESP-01` 通过 | - |
| DEMO-01 | 演示 | 演示账号、演示数据、讲解顺序、故障预案和彩排状态明确 | 未覆盖 | 演示账号和数据可用，但本轮未执行 3 次完整讲解彩排，也未验证讲解顺序和故障预案 | - |

## 6. 文档验收

- 交付文档齐全：`software-development-plan.md`、`software-requirements-specification.md`、`high-level-design.md`、`detailed-design.md`、`test-report.md`、`deployment-guide.md`、`user-manual.md`、`llm-usage.md` 均存在。
- 开发与 API 文档齐全：`docs/04-development/` 包含前端、后端、数据库、架构、判题与沙箱说明；`docs/05-api/` 覆盖认证、平台管理、课程、作业、成绩、通知等 API 文档。
- 后端权威输入齐全：`server/docs/stable-api.md`、`server/docs/generated/db-schema.md`、`server/docs/product-specs/` 均存在；数据库文档列出 52 个迁移及核心业务表。
- 文档站构建通过，但 DOC-02 仍标为失败，因为验收实际行为存在 P1-001 与 P1-002 两处产品/契约偏差。

## 7. 环境、数据与运行时验收

- `just dev-up` 证据：本地 Docker 依赖均为 Running；后端 `http://127.0.0.1:18080` 和前端 `http://127.0.0.1:3000` 已监听。
- `just healthcheck-strict` 证据：工具、compose、env、端口、后端 readiness、后端 OpenAPI、前端 login 均通过。
- 残留数据 dry-run：`server/scripts/ops/e2e-residual-cleanup.sh` 默认 dry-run 显示 `E2E-`、`MCP-`、`FULLRUN-` 等前缀在 PostgreSQL 与 MinIO object key 的命中均为 0，未执行删除。
- 数据准备：`just seed-fixtures` 返回 `status=passed`，22 个权限/E2E fixture 用例全通过，复用并重置本地演示/E2E 基线数据。

## 8. 公共、登录与权限验收

- 登录：`auth.spec.ts` 真实 E2E 覆盖管理员、教师、学生分别登录到对应工作台；MCP 复核三角色主工作台截图。
- 退出：`auth.spec.ts` 覆盖教师打开用户菜单并退出后返回登录页。
- 越权：MCP 复核教师访问 `/admin/users` 和学生访问 `/admin` 均显示“权限不足”；E2E 同时验证学生/教师越权 API 403、无 token API 401。
- 未登录控制台：MCP 清理会话访问登录页时出现 `/auth/me` 与 `/auth/refresh` 的 401 探测，属于未登录态预期，不计为缺陷。

## 9. 学生业务闭环验收

- `just e2e-real` 辅助证据显示结构化作业创建、发布、学生提交、附件下载、编程工作区、样例运行、正式判题、教师评分与重判等 full suite 用例通过。
- 阻塞点：学生“全部作业”聚合页主操作文案与 E2E 契约不一致，导致学生作业列表验收用例失败，详见 `P1-001`。

## 10. 教师业务闭环验收

- MCP 复核教师工作台、我的课程、全部作业、全部提交、成绩册、题库中心、实验中心、通知中心页面均可打开。
- `just e2e-real` full coverage 记录教师完成课程成员、资源、讨论、题库、判题环境、作业创建与发布、提交批改、成绩册导出与发布、实验评阅等闭环。

## 11. 管理员业务闭环验收

- `just e2e-real` 辅助证据显示平台配置、组织树子组织创建、用户治理、学期、课程模板、开课创建/筛选/编辑/详情、审计、权限解释等多项管理员能力通过。
- 阻塞点：完整组织结构跨学院开课 UI 在新增开课弹窗中无法选择共同管理学院，导致跨学院开课与作用域成员管理的完整 UI 闭环未通过，详见 `P1-002`。

## 12. 助教与授权范围验收

- 已通过部分：导航权限、后端 401/403、教师/学生越权、课程成员与助教相关权限测试在 E2E 记录中通过。
- 未通过部分：跨学院共同管理学院无法选择，导致开课助教/班级助教在跨学院作用域下的 UI 闭环不能完整确认，归入 P1-002。

## 13. 判题、文件、通知、实验能力验收

- 判题：`WEBIDE-REAL-01` 记录 Python3 编程作业从教师创建发布到学生 WebIDE 样例运行、正式提交、判题 ACCEPTED 的完整闭环。
- 文件：E2E 记录学生/教师附件上传下载、课程资源上传下载删除、实验报告附件下载。
- 通知：E2E 记录通知列表、未读数、单条已读、全部已读；实验报告流程中观察到 SSE connected + notification。
- 实验：E2E 记录实验创建/编辑/发布/关闭、学生报告保存提交、教师评阅发布；MCP 复核教师和学生实验聚合页。

## 14. 非功能与前端质量验收

- 构建质量：`just verify-full` 中 web lint、typecheck、unit tests、Next build 全通过。
- 响应式：MCP 复核 1280x800 管理员用户页、1440x900 教师实验页、390x844 学生作业页；E2E 另覆盖多个学生/教师 390px 移动端页面。
- 控制台：MCP 当前错误仅为未登录态 `/auth/me`、`/auth/refresh` 401 探测；未观察到 5xx、未处理 pageerror 或核心页面空白。
- 质量扣分：`just e2e-real` 仍有 2 个真实浏览器失败，因此 NFR-01 标为失败。

## 15. 演示与答辩准备验收

- 演示账号与数据：`U-SA1`、`U-TA1`、`U-ST1` 可登录；`just seed-fixtures` 与 MCP 截图证明基础演示数据可用。
- 未覆盖：本轮未执行 `acceptance-checklist.md` 要求的至少 3 次完整讲解彩排，未形成讲解顺序和故障预案的实测记录。
- 风险：两个 P1 会影响演示稳定性，尤其是跨学院开课/助教权限闭环。

## 16. 缺陷详情

### P1-001 学生全部作业列表操作文案与 E2E 契约不一致

- 严重级别：P1
- 验收编号：STUDENT-02
- 模块：学生作业
- 角色：学生
- 页面或对象：`/student/assignments`
- 业务步骤：
  1. 使用真实后端 E2E 学生账号登录。
  2. 打开 fixture 已发布作业详情，确认详情页和提交历史可见。
  3. 返回学生“全部作业”聚合页。
- 实际表现：页面显示已发布作业卡片，主操作是“继续作答”；`assignment-submission.spec.ts` 期待可见链接名匹配“开始做题”，15 秒内未找到并失败。
- 期望表现：学生作业列表的主操作文案、可访问名称和测试契约应一致；对于可开始或继续的作业，应给出清楚且稳定的操作入口。
- 影响说明：完整结构化提交闭环在 full suite 中通过，但学生聚合页主操作契约不稳定，会影响演示脚本、自动验收和用户对“首次开始 / 继续作答”的理解。
- 证据：
  - 截图：`product-acceptance-screenshots/mcp-19-student-assignments.png`、`mcp-20-student-assignment-detail.png`。
  - Playwright MCP 观察：学生 `U-ST1` 的“全部作业”页可见多个已发布作业，主按钮为“继续作答”，未见“开始做题”；截图抽查确认该页面不是空白或错误页。
  - 命令/API/日志/数据：`just e2e-real` 失败，`assignment-submission.spec.ts:38`，页面快照显示两个作业卡片主操作均为“继续作答”，未出现“开始做题”；trace 位于 `web/test-results/assignment-submission-assi-04c46-or-the-active-fixture-class-chromium/trace.zip`。
- 是否阻塞后续测试：否
- 修复建议方向：统一学生作业列表主操作的业务语义和 accessible name；若“继续作答”是正确行为，则同步 E2E 契约并明确首次/继续状态。
- 修复状态：待修复

### P1-002 管理员跨学院开课 UI 无法选择共同管理学院

- 严重级别：P1
- 验收编号：ADMIN-02、AUTHZ-01、TA-01
- 模块：管理员课程治理 / 权限作用域
- 角色：管理员
- 页面或对象：`/admin/course-offerings` 新增开课弹窗
- 业务步骤：
  1. 使用管理员真实 E2E 流程创建学校组织、主学院、共同管理学院、课程模板和相关教师用户。
  2. 打开“开课管理”并点击“新增开课”。
  3. 选择课程模板、学期，填写开课名称与编码。
  4. 在“共同管理学院”组中选择新建的共同管理学院。
- 实际表现：Playwright 等待 `共同管理学院` 组内名称为 `E2EMQ6D7CEE2U5C3IORG-共管学院` 的按钮，直到 180 秒测试超时；完整跨学院开课和 scoped member management UI 闭环失败。
- 期望表现：共同管理学院候选应出现在弹窗中，并可被管理员选择，用于创建跨学院开课和后续作用域成员管理。
- 影响说明：跨学院开课是管理员治理、权限边界和助教授权范围的重要演示链路；失败会导致跨学院协作、班级/开课作用域授权无法形成完整 UI 验收闭环。
- 证据：
  - 截图：`product-acceptance-screenshots/mcp-04-admin-course-offerings.png`。
  - Playwright MCP 观察：管理员“开课管理”页面本身可打开并显示开课列表；失败发生在 E2E 新增开课弹窗的“共同管理学院”候选选择步骤，当前 MCP 截图作为页面可达性证据，失败细节以 E2E trace/error-context 为准。
  - 命令/API/日志/数据：`just e2e-real` 失败，`full-organization-structure.spec.ts:322`，等待共同管理学院按钮超时；trace 位于 `web/test-results/full-organization-structur-753bf-ember-management-through-UI-chromium/trace.zip`。
- 是否阻塞后续测试：否
- 修复建议方向：检查新增开课弹窗中共同管理学院候选数据源、搜索/分页加载、组织筛选和 Radix selector accessible name；确保新建学院能被立即检索和选择。
- 修复状态：待修复

## 17. 未覆盖范围与原因

- `DEMO-01`：未执行 3 次完整讲解彩排，未验证讲解顺序和故障预案。
- `profile-required`：本轮没有专门构造缺少教师/学生档案但已有课程身份的账号进行页面级复核；该行为仅从路由代码和既有测试间接覆盖。
- WebIDE 当前截图：默认学生账号当前未在 MCP 页面中直接发现工作区入口；WebIDE 完整闭环由 `webide-real-flow.spec.ts` 的真实 UI E2E 作为辅助证据。

## 18. 修复优先级建议

1. P1-002：优先修复跨学院开课共同管理学院候选加载/选择问题；它影响管理员治理、权限作用域与助教演示链路。
2. P1-001：统一学生作业聚合页主操作文案、accessible name 与 E2E 契约；明确“首次开始”和“继续作答”的业务语义。
3. DEMO-01：修复 P1 后按 `acceptance-checklist.md` 执行 3 次完整演示彩排，并补充讲解顺序、故障预案和录屏/截图证据。

## 19. 验收阶段最终状态

- 报告完成时间：2026-06-09 16:50 CST
- 本轮未修改应用代码；仅新增验收报告、截图和证据索引。
- 证据目录：`docs/06-testing-and-ops/artifacts/product-acceptance-screenshots/`，共 28 张 PNG。
- 额外证据：`docs/06-testing-and-ops/artifacts/product-acceptance-evidence/evidence-index.md`。
- 最终 `just status`：提交前 `server/`、`web/` 均为 clean；`docs/` 仅包含本轮 staged 验收产物 30 entries。由于 `docs/06-testing-and-ops/artifacts/` 被 `.gitignore` 忽略，本轮验收产物已通过 `git add -f` 强制纳入 docs 提交。
