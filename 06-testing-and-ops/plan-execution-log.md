---
title: "计划执行记录"
section: "06-testing-and-ops"
status: current
---
# 计划执行记录

更新日期：2026-05-16

## 1. 工作基线

| 仓库路径 | 当前分支 | 工作区状态 | 备注 |
| --- | --- | --- | --- |
| `/Users/moorefoss/Code/AUBB` | 非 Git 仓库 | 不适用 | 根目录用于组织 `server`、`web`、`docs` |
| `server/` | `main` | 有未提交变更和新增文件 | 后端代码、迁移、测试、脚本与 `server/docs` 文档均有本轮修改 |
| `web/` | `main` | 有未提交变更和新增文件 | 前端 lint 修复、全局搜索、真实 E2E、课程公告校验、OpenAPI 生成类型和 `web/docs` 文档更新 |
| `docs/` | `main` | 有未提交变更和新增文件 | 顶层文档同步与本轮交付报告 |

## 2. 已执行阶段

| 阶段 | 状态 | 关键输出 |
| --- | --- | --- |
| 基线与技术栈核验 | 已完成 | 后端为 Spring Boot 4 / Maven / Java 25；前端为 Next.js 16 / React 19 / TypeScript；顶层文档站为 VitePress |
| 后端编译与测试 | 已完成 | 已完成 Maven 编译、Spotless 与测试基线；本轮新增权限真实脚本回归后，权限真实 API 场景 `22/22` 通过 |
| 前端静态验证 | 已完成 | 已完成 lint、typecheck、unit test、build；真实后端 Playwright 最终全套 `36/36` 通过 |
| 默认 E2E | 已完成 | 默认未设置 `AUBB_E2E_REAL_BACKEND=1` 时会跳过真实后端 smoke；真实模式已单独执行通过 |
| V48 文档同步 | 已完成 | 当前文档已移除“成绩申诉、成绩发布快照、assignment 级成绩权重”为现行能力的表述，仅保留 V48 已移除说明 |
| 运行时 OpenAPI 刷新 | 已完成 | 使用 `npx openapi-typescript http://127.0.0.1:18080/v3/api-docs -o src/shared/api/generated/openapi.ts` 刷新前端生成类型 |
| 真实前后端联调 | 已完成 | Docker 依赖、后端 `18080`、前端 `3000` 均启动成功；readiness、OpenAPI、登录、权限脚本、Playwright 和浏览器点验完成 |
| 顶层交付报告 | 已完成 | 本文件、全栈审计报告、按钮级 E2E 验证报告已补录真实联调证据 |

## 3. 本轮真实联调证据

| 验证项 | 命令 / 操作 | 结果 |
| --- | --- | --- |
| 本地依赖 | `cd server && docker compose up -d` | PostgreSQL、RabbitMQ、MinIO、Redis 健康，go-judge 运行；首次构建遇到 Debian 502，重试后成功 |
| 后端启动 | `SERVER_PORT=18080 AUBB_MINIO_ENABLED=true ... bash ./mvnw spring-boot:run` | 本地库已存在学校根节点 `SCH-REALRUN`，启用 bootstrap 且传入新 code 会失败；最终关闭 bootstrap、保留本地 JWT、启用本地 MinIO 后启动成功，Tomcat 监听 `18080`，Flyway 48 个迁移完成 |
| 后端 readiness | `curl -fsS http://127.0.0.1:18080/actuator/health/readiness` | `status=UP`，最终响应包含 `db`、`readinessState`、`redisEnhancement`、`minioStorage`，bucket 为本地 `aubb-assets` |
| 运行时 OpenAPI | `curl -fsS http://127.0.0.1:18080/v3/api-docs` | OpenAPI `3.1.0`，当前 `124` 个 path |
| 登录探针 | `POST /api/v1/auth/login` | 管理员、教师、学生测试账号可登录并返回 access / refresh token |
| 权限真实 API | `bash scripts/api-tests/permission/run_permission_e2e.sh` | `22` 个真实 HTTP 权限场景全部通过，报告在 `/tmp/aubb-permission-e2e` |
| 前端启动 | `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run dev -- --hostname 127.0.0.1 --port 3000` | Next dev server 就绪，页面通过 rewrite 连接真实后端 |
| 真实 Playwright | `AUBB_E2E_REAL_BACKEND=1 npm run test:e2e` | 早期 smoke 基线通过；最终真实后端完整 Playwright 全套 `36 passed` |
| 浏览器点验 | Playwright MCP 打开 `http://127.0.0.1:3000` | 登录失败/成功/退出、管理员导航与搜索、教师课程公告、学生作业/成绩、未授权跳转已验证 |

## 4. 关键修复清单

| 文件 / 模块 | 问题 | 修复方式 | 验证 |
| --- | --- | --- | --- |
| `server/scripts/api-tests/permission/e2e_permission_realrun.py` | 后端在课程任课/成员权限变更后会撤销受影响用户旧会话，脚本继续复用旧 `U-TA1` token 导致真实 API 脚本在成员列表接口收到 `401` | fixture 收尾刷新受课程权限授予影响的教师、助教、学生账号 token | `e2e_permission_realrun_test.py` 通过；真实权限 API `22/22` 通过 |
| `web/src/app/(teacher)/teacher/courses/[offeringId]/announcements/page.tsx` | 教师公告空标题/正文点击“发布”会静默无反馈 | 改为真实 `<form>`，标题和正文添加 `required` 与可访问标签，编辑弹窗同样走 submit 校验 | 新增 Playwright 用例；早期 smoke 通过；浏览器点验返回原生必填提示 |
| `web/src/app/(admin)/admin/users/page.tsx`、`web/src/shared/ui/file-upload-field.tsx` | 用户管理顶部“批量导入”按钮没有触发隐藏文件选择器 | `FileUploadField` 增加 `triggerRef`，用户页顶部按钮通过 ref 打开 CSV 文件选择器 | `file-upload-field.test.tsx` 通过；真实 filechooser E2E 通过 |
| `web/src/shared/api/download/index.ts`、`web/src/tests/unit/api/download.contract.test.ts` | 下载按钮只通过 API 拉取 blob，没有创建浏览器下载 | `downloadBinary` 解析文件名、创建 object URL、点击隐藏 anchor 并释放 URL，同时返回 blob 元数据 | 新增单测 1/1 通过；完整前端单元测试 11 个文件 / 24 个测试通过 |
| `web/src/app/(teacher)/teacher/courses/[offeringId]/resources/page.tsx`、`web/src/tests/e2e/teacher-course.spec.ts` | 课程资源 E2E 首次失败，后端未启用对象存储时上传 API 返回 `COURSE_RESOURCE_STORAGE_DISABLED`；资源标题字段也缺少稳定 label 关联 | 补资源页 label/id；E2E 等待上传 POST 并断言响应 OK；后端联调启动启用本地 MinIO | 资源上传、改名、下载、删除目标 E2E 1/1 通过；full-course 再次覆盖教师/学生下载 |
| `web/src/tests/e2e/auth.spec.ts` | 退出登录菜单项真实 role 为 `menuitem`，测试按 `button` 查询导致误报失败 | 改用 `getByRole("menuitem", { name: "退出登录" })` | 单用例通过；完整真实 E2E 通过 |
| `web/src/shared/api/generated/openapi.ts` | 前端生成类型落后于运行时后端契约 | 从真实后端 `/v3/api-docs` 重新生成 | 生成命令通过；后续 typecheck/build 覆盖 |
| `web/src/app/(student)/student/assignments/page.tsx`、`web/src/app/(student)/student/courses/[classId]/page.tsx`、`web/src/app/(student)/student/labs/page.tsx` | 运行时 OpenAPI 中 `MyCourseClassView` 不包含 `features`，学生端仍读取不存在字段导致 typecheck 失败 | 去除学生端对不存在 `features` 字段的依赖，入口按当前 `/me/courses` 合约默认可见，内容与权限仍由后端接口控制 | `npm run typecheck`、`npm run build`、真实 E2E smoke 和 full suites 覆盖 |
| `server/src/test/java/com/aubb/server/integration/AuthzOpenApiAccessRegistry.java` | OpenAPI 权限登记表仍包含已删除成绩申诉 / 发布批次路径，且缺少部分 PUT/DELETE 路径 | 移除旧路径，补齐学期、课程、公告、资源等当前路径权限映射 | 后端全量测试基线通过 |
| `server/src/test/java/com/aubb/server/integration/*IntegrationTests.java` | 固定 2026 时间窗和旧申诉通知导致测试漂移 | 改为动态时间窗，旧申诉通知改为当前实验报告通知 | 后端全量测试基线通过 |
| `web/src/shared/ui/layout/topbar.tsx` | 顶栏全局搜索输入可输入但缺少有效跳转 | 新增全局搜索路由匹配，Enter 跳到首个可访问目标 | 前端单元测试和真实浏览器点验通过 |
| `web/docs/backend/**`、`server/docs/**`、`docs/**` | 多处把 V48 已删除能力写成当前能力 | 更新 API、数据模型、权限、产品规格和顶层文档 | 残留扫描仅剩“V48 已删除/不再提供”的说明性命中 |
| `web/playwright.config.ts`、旧 smoke specs、`web/src/tests/e2e/real-backend.ts` | 全量真实 E2E 并行使用共享真实账号时触发登录限流，30 秒预算下出现超时 | 真实后端模式使用 1 worker 和 90 秒测试预算；非认证 smoke 改为 API session 注入；UI 登录 helper 仅在明确 429 时等待重试 | 最终 `npm run test:e2e` 全套 `36 passed` |

## 5. 当前运行状态

| 服务 | 地址 | 状态 |
| --- | --- | --- |
| 后端 Spring Boot | `http://127.0.0.1:18080` | 本轮验证时运行中；最终收尾后停止 |
| 前端 Next dev server | `http://127.0.0.1:3000` | 本轮验证时运行中；最终收尾后停止 |
| PostgreSQL / RabbitMQ / MinIO / Redis / go-judge | Docker compose | 本轮验证时运行中；最终收尾后执行 `docker compose down`，未删除数据卷 |

## 6. 注意事项

- 本轮只使用本地 Docker、测试账号和本地 dummy 环境变量；未连接生产数据库、生产服务或付费外部 API。
- 报告中只记录 token 是否存在，不记录 token、cookie、JWT、私钥或真实密钥值。
- 课程公告和课程资源已做浏览器级创建-验证-清理闭环；批量导入文件提交、发布成绩、实验评阅等写入较重操作未全部提交，其真实写入闭环仍主要由 API 权限脚本和后端集成测试覆盖。
- 课程资源上传/下载真实 E2E 需要后端以本地 MinIO 启动；若 `AUBB_MINIO_ENABLED=false`，上传 API 会按设计返回 `COURSE_RESOURCE_STORAGE_DISABLED`。
- 真实前后端 E2E 必须用 `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080` 启动 Next dev server；缺少该变量时 `/api/v1/auth/login` 会由 Next 返回 `404`，不代表后端登录失败。

## 7. 本轮按 `plan.md` 重新执行记录（2026-05-16 19:20 CST）

### Task 1：建立当前工作基线

| 检查项 | 结果 |
| --- | --- |
| 当前目录 | `/Users/moorefoss/Code/AUBB` |
| Git 仓库发现 | 根目录不是 Git 仓库；仅发现 `./server/.git`、`./web/.git`、`./docs/.git` |
| `server/` | `main...origin/main`，最近提交 `510897f chore: sync audit fixes and verification`，开始时 `git status --short` 无未提交条目 |
| `web/` | `main...origin/main`，最近提交 `2c6969b feat: align frontend integration and e2e coverage`，开始时 `git status --short` 无未提交条目 |
| `docs/` | `main...origin/main`，最近提交 `261de6a docs: add full stack audit reports`，开始时 `git status --short` 无未提交条目 |
| 后端命令入口 | `./mvnw -v` 成功；Maven 3.9.14，Java 25.0.3 |
| 前端命令入口 | `npm run` 确认 `dev`、`build`、`lint`、`typecheck`、`test`、`test:e2e` |
| 文档命令入口 | `npm run` 确认 `docs:dev`、`docs:build`、`docs:preview` |

本轮验证范围：按根目录 `plan.md` Task 1 至 Task 11 执行，覆盖 `GAP-AUTH-01`、`GAP-ADMIN-01` 至 `GAP-ADMIN-10`、`GAP-COURSE-01` 至 `GAP-COURSE-06`、`GAP-ASSIGN-01` 至 `GAP-ASSIGN-07`、`GAP-GRADE-01` 至 `GAP-GRADE-03`、`GAP-LAB-01` 至 `GAP-LAB-03`、`GAP-NOTIF-01`、`GAP-NOTIF-02`、`GAP-DOWNLOAD-01`、`GAP-NAV-01`、`GAP-RESP-01`。

### Task 2：从代码重新生成全量功能矩阵

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 前端页面 | `rg --files web/src/app \| sort`、`find web/src/app -name page.tsx` | 45 个 `page.tsx`；未发现 `plan.md` 1.3 之外的新增业务路由 |
| 后端 Controller | `rg --files server/src/main/java/com/aubb/server/modules \| rg '/api/.*Controller\.java$'` | 33 个 Controller；覆盖认证、治理、课程、作业、提交、判题、成绩、实验、通知 |
| API 注解/SSE | `rg -n '@(Get\|Post\|Put\|Patch\|Delete\|Request)Mapping\|TEXT_EVENT_STREAM\|SseEmitter' server/src/main/java/com/aubb/server/modules` | 确认通知 SSE 路径 `GET /api/v1/me/notifications/stream`，并确认各 Controller 的 HTTP 映射 |
| 前端 API 封装 | `find src/features -path '*/api/*' -type f -maxdepth 5 \| sort` | 20 个 API 封装文件；均可映射到后端 Controller 和页面入口 |
| 导航入口 | `web/src/shared/routing/nav-config.ts` | 管理员 9 个、教师 6 个、学生 6 个侧边栏入口 |

输出文件：已更新 `docs/06-testing-and-ops/full-stack-audit-report.md` 第 14 节，补入本轮代码扫描矩阵、API 封装映射和 GAP 基线。

### Task 3：准备真实本地联调环境

| 检查项 | 命令 / 操作 | 结果 |
| --- | --- | --- |
| Docker 依赖 | `cd server && docker compose up -d postgres rabbitmq minio redis go-judge && docker compose ps` | PostgreSQL、RabbitMQ、MinIO、Redis、go-judge 均处于运行状态；PostgreSQL/RabbitMQ/MinIO/Redis health 为 healthy，go-judge 监听本地 `5050` |
| 后端本地环境 | 使用 `SERVER_PORT`、`SPRING_DATASOURCE_*`、`SPRING_RABBITMQ_*`、`AUBB_JWT_SECRET`、`AUBB_MINIO_*`、`AUBB_GO_JUDGE_*`、`AUBB_REDIS_*`、`AUBB_JUDGE_QUEUE_*`、`AUBB_BOOTSTRAP_ENABLED=false` | 仅使用本地 Docker 依赖和本地变量；报告不记录变量值；未连接生产服务 |
| 后端启动 | `bash ./mvnw spring-boot:run`，监听 `http://127.0.0.1:18080` | Spring Boot 启动成功，Flyway 48 个迁移已是最新；修复平台配置 nullable 字段后重启为 session `69196` |
| 后端 readiness | `curl -fsS http://127.0.0.1:18080/actuator/health/readiness` | `status=UP`；components 为 `db`、`goJudge`、`judgeQueue`、`minioStorage`、`readinessState`、`redisEnhancement` |
| 运行时 OpenAPI | `curl -fsS http://127.0.0.1:18080/v3/api-docs` | 可访问；用于后续全量 E2E 和最终回归验证 |
| 前端启动 | 既有 Next dev server session `99032`，`http://127.0.0.1:3000/login` | `/login` 返回 HTTP `200`；前端代理指向本地后端 |
| 前置修复验证 | `cd server && ./mvnw -Dtest=PlatformGovernanceApiIntegrationTests#managesLivePlatformConfigAndWritesAuditTrail test` | 首次新增 nullable 字段清空断言为红态；修复 `PlatformConfigEntity` nullable 更新策略后该用例通过 |

Task 3 输出：真实本地后端、真实前端与 Docker 依赖均已就绪，可进入 Task 4 至 Task 9 的 Playwright Chromium 全量验证。

### Task 4：建立全量 Playwright 真实验证工程

| 检查项 | 结果 |
| --- | --- |
| E2E helper | `web/src/tests/e2e/real-backend.ts` 已扩展 API 登录、cookie 注入、唯一名、API 断言、下载断言、multipart、coverage 记录；只读取环境变量，不打印密码、token、cookie 或 JWT |
| fixture | `web/src/tests/e2e/full-fixtures.ts` 通过 API 准备管理员、教师、学生和课程上下文；为避免历史数据状态影响，创建新的 `E2E-*` active 学生并加入 A1 班 |
| full suites | 新增 `full-admin.spec.ts`、`full-course.spec.ts`、`full-assignment-judge.spec.ts`、`full-grading-lab-notification.spec.ts`、`full-navigation-permission.spec.ts`；保留原 smoke specs |
| 中间修复验证 | `full-admin.spec.ts` 5/5 通过；`full-course.spec.ts` 5/5 通过；`full-assignment-judge.spec.ts` 最终 3/3 通过；`full-grading-lab-notification.spec.ts` 最终 3/3 通过；`full-navigation-permission.spec.ts` 最终 3/3 通过 |

Task 4 输出：真实 E2E 工程已从 smoke 扩展为管理员、课程、作业判题、成绩实验通知、导航权限响应式五个 full suites。

### Task 5：管理端全量真实验证

| GAP | 结果 | 证据 |
| --- | --- | --- |
| `GAP-AUTH-01` | 已真实验证 | refresh、revoke、无 token `401`、管理员撤销临时用户会话后旧 access token 失效 |
| `GAP-ADMIN-01` | 已真实验证 | 平台配置读取、保存、重新读取、恢复原值闭环；修复 nullable 字段无法清空问题 |
| `GAP-ADMIN-02` | 部分验证 | 组织架构页面打开，子组织创建后出现在树中；根 `SCHOOL` 创建按后端策略返回 `400/409`；无删除 API，记录残留 |
| `GAP-ADMIN-03`、`GAP-ADMIN-04`、`GAP-ADMIN-05` | 已真实验证 | 用户创建、搜索、详情、身份/profile/组织关系更新、禁用启用、撤销会话、CSV 成功/失败行导入 |
| `GAP-ADMIN-06`、`GAP-ADMIN-07`、`GAP-ADMIN-08`、`GAP-ADMIN-09`、`GAP-ADMIN-10` | 已真实验证 | 学期、课程模板、开课创建筛选编辑详情；审计日志筛选；权限解释允许/拒绝/错误输入 |

执行命令：`cd web && AUBB_E2E_REAL_BACKEND=1 ... npx playwright test src/tests/e2e/full-admin.spec.ts --reporter=list --project=chromium`，结果 `5 passed`。省略号为本地测试账号密码环境变量，未记录值。

### Task 6：课程、成员、讨论、题库、判题环境全量验证

| GAP | 结果 | 证据 |
| --- | --- | --- |
| `GAP-COURSE-01`、`GAP-COURSE-02` | 已真实验证 | 教学班创建、功能开关、批量成员成功/失败、CSV 导入、成员禁用恢复、转班 |
| `GAP-COURSE-03`、`GAP-DOWNLOAD-01` | 已真实验证 | 教师上传/改名/下载/删除课程资源，学生侧列表和下载同一资源 |
| `GAP-COURSE-04` | 已真实验证 | 教师发帖/回复、学生回复、锁定后学生回复被拒绝、最后解锁 |
| `GAP-COURSE-05` | 已真实验证 | 单选、多选、简答、文件上传、编程题创建，题库筛选、编辑、归档 |
| `GAP-COURSE-06` | 已真实验证 | 判题环境创建、编辑、归档 |

执行命令：`cd web && AUBB_E2E_REAL_BACKEND=1 ... npx playwright test src/tests/e2e/full-course.spec.ts --reporter=list --project=chromium`，结果 `5 passed`。

### Task 7：作业、提交、编程、判题全量验证

| GAP | 结果 | 证据 |
| --- | --- | --- |
| `GAP-ASSIGN-01`、`GAP-ASSIGN-02` | 已真实验证 | 教师创建结构化作业、编辑基础信息、替换试卷、发布、学生可见、关闭后提交被拒绝 |
| `GAP-ASSIGN-03`、`GAP-ASSIGN-04`、`GAP-DOWNLOAD-01` | 已真实验证 | 学生选择/简答/文件/编程答案提交、提交历史、提交详情、学生和教师附件下载 |
| `GAP-ASSIGN-05`、`GAP-ASSIGN-06`、`GAP-ASSIGN-07` | 已真实验证 | 编程工作区文件操作/保存/修订/恢复/重置、样例运行、正式判题、学生/教师报告下载、教师手动评分和重判 |

执行命令：`cd web && AUBB_E2E_REAL_BACKEND=1 ... npx playwright test src/tests/e2e/full-assignment-judge.spec.ts --reporter=list --project=chromium`，最终结果 `3 passed`。中间修复：教师提交详情页访问前切换浏览器会话到教师；页面断言改为真实稳定内容“答案内容”。

### Task 8：成绩、实验、通知全量验证

| GAP | 结果 | 证据 |
| --- | --- | --- |
| `GAP-GRADE-01`、`GAP-GRADE-02`、`GAP-GRADE-03`、`GAP-DOWNLOAD-01` | 已真实验证 | 教师成绩册按开课/班级查询、报告、导出、人工评分、批量调分、模板下载、CSV 导入、发布；学生成绩查询和导出 |
| `GAP-LAB-01`、`GAP-LAB-02`、`GAP-LAB-03`、`GAP-DOWNLOAD-01` | 已真实验证 | 实验创建/编辑/发布/关闭，学生附件上传保存提交读取下载，教师报告列表详情下载评阅发布，学生可见评语 |
| `GAP-NOTIF-01`、`GAP-NOTIF-02` | 已真实验证 | 通知列表、未读数、单条已读、全部已读；SSE `connected` 和 `notification` 事件 |

执行命令：`cd web && AUBB_E2E_REAL_BACKEND=1 AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 ... npx playwright test src/tests/e2e/full-grading-lab-notification.spec.ts --reporter=list --project=chromium`，最终结果 `3 passed`。中间修复：SSE 探针直连本地后端 `AUBB_SERVER_ORIGIN`，为 `reader.read()` 增加 deadline，并修正重复触发 publish 的测试状态；学生实验页面跳转前切换浏览器会话到学生。

### Task 9：导航、下载、响应式、权限矩阵

| GAP | 结果 | 证据 |
| --- | --- | --- |
| `GAP-NAV-01` | 已真实验证 | 三角色侧边栏全部导航、概览快捷入口、顶栏搜索、用户菜单打开；学生/教师越权页面回退到默认首页或无权限/登录，后端无 token `401`、无角色 `403` |
| `GAP-RESP-01` | 已真实验证 | 管理、教师、学生关键页在 `1280x800` 和 `390x844` 下主按钮或移动导航菜单可见可点击 |
| `GAP-DOWNLOAD-01` | 已真实验证 | 已在 Task 6-8 覆盖课程资源、提交附件、判题报告、成绩导出、成绩导入模板、实验附件等下载 API 的 OK 和非空响应 |

执行命令：`cd web && AUBB_E2E_REAL_BACKEND=1 ... npx playwright test src/tests/e2e/full-navigation-permission.spec.ts --reporter=list --project=chromium`，最终结果 `3 passed`。中间修复：登录后先进入角色首页再遍历侧边栏；同名快捷入口冲突时限定 `navigation` 区域；按钮文案按当前 UI 使用“新增用户”；权限断言允许当前实现回退到角色默认首页。

### Task 10：后端/API/文档回归验证

| 步骤 | 命令 | 结果 |
| --- | --- | --- |
| 后端脚本单测 | `cd server && python3 scripts/api-tests/permission/e2e_permission_realrun_test.py` | `Ran 1 test`，`OK` |
| 后端权限真实 API | `cd server && BASE_URL=http://127.0.0.1:18080 bash scripts/api-tests/permission/run_permission_e2e.sh` | `caseCount=22`、`passedCount=22`、`failedCount=0`、`status=passed` |
| 后端全量 verify | `cd server && bash ./mvnw verify` | `BUILD SUCCESS`；Tests run: `318`，Failures: `0`，Errors: `0`，Skipped: `0` |
| 前端 typecheck | `cd web && npm run typecheck` | 通过 |
| 前端 lint | `cd web && npm run lint` | 通过，0 errors |
| 前端单元测试 | `cd web && npm run test` | 11 个测试文件、24 个测试通过 |
| 前端真实后端 E2E | `cd web && AUBB_E2E_REAL_BACKEND=1 AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 ... npm run test:e2e` | 完整套件 `36 passed`；中间曾因共享账号限流和 30 秒预算失败，修复测试基础设施后全量重跑通过 |
| 前端生产构建 | `cd web && AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` | 通过；Next.js 编译、TypeScript、静态页面生成均成功 |
| 文档构建 | `cd docs && npm run docs:build` | 通过；VitePress build complete |

Task 10 额外修复：`web/playwright.config.ts` 在真实后端模式下使用 1 worker 和 90 秒测试预算；旧 smoke specs 中非认证目的的页面访问改为 `loginAsApi` 注入 session；`real-backend.ts` 的 UI 登录 helper 只在页面明确返回 429 限流提示时等待并重试。该调整避免全量真实 E2E 使用共享测试账号时误触登录限流。

### Task 11：收尾、服务关闭、提交建议

| 检查项 | 命令 / 操作 | 结果 |
| --- | --- | --- |
| 停止前端 | 终止本地 Next dev 进程 | 已停止；`curl --max-time 2 -sS http://127.0.0.1:3000/login` 返回连接失败 |
| 停止后端 | 终止本地 Maven/Spring Boot 进程 | 已停止；`curl --max-time 2 -sS http://127.0.0.1:18080/actuator/health/readiness` 返回连接失败 |
| 停止 Docker 依赖 | `cd server && docker compose down` | PostgreSQL、RabbitMQ、MinIO、Redis、go-judge 容器和网络已移除；未删除数据卷 |
| Compose 状态 | `cd server && docker compose ps` | 仅输出表头，无运行服务 |

#### Task 11 Git 摘要

| 仓库 | 状态 | diff stat |
| --- | --- | --- |
| `server/` | `main...origin/main`，6 个已修改文件 | `6 files changed, 89 insertions(+), 8 deletions(-)` |
| `web/` | `main...origin/main`，7 个已修改文件，6 个新增 full E2E 文件未跟踪 | tracked diff 为 `7 files changed, 385 insertions(+), 82 deletions(-)`；新增文件为 `full-admin.spec.ts`、`full-assignment-judge.spec.ts`、`full-course.spec.ts`、`full-fixtures.ts`、`full-grading-lab-notification.spec.ts`、`full-navigation-permission.spec.ts` |
| `docs/` | `main...origin/main`，3 个已修改报告文件 | `3 files changed, 338 insertions(+), 100 deletions(-)` |

## 8. 2026-05-17 继续执行审计

本段记录上下文恢复后的实际状态校验。此前 Task 11 的 Git 摘要记录的是提交前状态；本段以当前工作区命令输出为准。

| 检查项 | 当前证据 |
| --- | --- |
| 当前提交：`server/` | `32aea14 fix(authz): 补强真实权限验证修复` |
| 当前提交：`web/` | `f9b0245 test(e2e): 补全真实权限场景` |
| 当前提交：`docs/` | `7105a31 docs(testing): 记录真实权限验证` |
| 剩余 dirty：`server/` | `M Dockerfile`，属于本轮开始时已记录的既有 dirty 文件，未纳入本次功能提交 |
| 剩余 dirty：`web/` | `M next.config.ts`、`M src/tests/e2e/full-fixtures.ts`，属于本轮开始时已记录的既有 dirty 文件，未纳入本次功能提交 |
| 剩余 dirty：`docs/` | 追加本段前为 clean；追加本段后仅包含本审计记录 |
| 运行时 OpenAPI 快照 | 服务停止前检查为 `3.1.0 124` |
| 服务停止 | `docker compose down` 后残留 `app`、`judge-worker` 占用 `server_default`，随后执行 `docker compose stop app judge-worker && docker compose rm -f app judge-worker && docker compose down`；未删除 volumes |
| 最终服务状态 | `docker compose ps -a` 仅输出表头；`127.0.0.1:18080` 和 `127.0.0.1:3000` 均连接失败 |
| 当前阻塞 | 恢复后的当前 shell、`zsh -lc` 与 `launchctl` 均看不到四个 `AUBB_E2E_*_PASSWORD` 变量，因此不能重新运行真实登录基线或 full regression |

本段不记录密码、token、cookie、JWT、私钥或真实连接串。

### 2026-05-17 继续执行补充

在 E2E 密码变量仍缺失、真实服务不得启动的状态下，补充执行不依赖真实后端的前端静态验证：

| 命令 | 结果 |
| --- | --- |
| `cd web && npm run typecheck` | 通过，退出码 0 |
| `cd web && npm run lint` | 通过，退出码 0 |

该验证仅说明当前 `web/` 剩余 dirty 文件未造成 TypeScript 或 ESLint 失败；不能替代真实后端、真实依赖和真实浏览器 E2E 门禁。

### 2026-05-17 后端静态门禁补充

| 命令 | 结果 |
| --- | --- |
| `cd server && bash ./mvnw spotless:check` | `BUILD SUCCESS`；Spotless 检查 531 个 Java 文件，0 个文件需要修改 |

该验证不依赖 E2E 密码变量；真实服务启动、后端 full regression 和真实浏览器 E2E 仍等待四个 `AUBB_E2E_*_PASSWORD` 变量进入当前执行环境。

### 2026-05-17 后端与前端单元回归补充

| 命令 | 结果 |
| --- | --- |
| `cd server && bash ./mvnw verify` | `BUILD SUCCESS`；Tests run: 318，Failures: 0，Errors: 0，Skipped: 0 |
| `cd web && npm run test` | 11 个测试文件、24 个测试通过 |

`mvn verify` 使用 Testcontainers 隔离依赖，结束后已检查 `docker ps` 无运行容器、`docker compose ps -a` 仅输出表头。该补充仍不替代 `plan.md` 要求的真实本地服务、三角色登录基线和真实浏览器 E2E；这些仍因四个 `AUBB_E2E_*_PASSWORD` 变量缺失而阻塞。

### 2026-05-17 前端构建补充

| 命令 | 结果 |
| --- | --- |
| `cd web && AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` | 通过；Next.js 16.2.4 Turbopack 编译、TypeScript、30 个静态页面生成和路由优化均完成 |

该构建验证不启动本地后端；真实 API 代理、三角色登录和真实浏览器 E2E 仍需在四个 E2E 密码变量可用后重新执行。

### 2026-05-17 E2E Mock 与权限脚本静态补充

| 命令 | 结果 |
| --- | --- |
| `cd web && rg -n "\\b(page|context|browserContext)\\.route\\b|route\\(" src/tests/e2e` | 无命中，退出码 1；未发现 Playwright E2E 中使用 route mock 后端响应 |
| `cd server && python3 scripts/api-tests/permission/e2e_permission_realrun_test.py` | `Ran 1 test`，`OK` |

该补充仅覆盖静态 mock 扫描和权限脚本单元测试；真实权限 HTTP 脚本仍需本地后端 `127.0.0.1:18080` 与 E2E 密码变量可用后重新执行。

### 2026-05-17 剩余 Dirty 文件归因补充

| 仓库 | 文件 | 只读归因 |
| --- | --- | --- |
| `server/` | `Dockerfile` | 当前 diff 移除 BuildKit cache mount，并在 runtime stage 安装 `curl`；`server/compose.yaml` 的 `app` healthcheck 使用 `curl -fsS http://localhost:8080/actuator/health/readiness`。该文件在本轮开始时已经 dirty，未纳入本轮提交，不能在未确认归属前提交或回滚 |
| `web/` | `next.config.ts` | 当前 diff 增加 `allowedDevOrigins: ["127.0.0.1"]`，与本计划固定使用 `127.0.0.1:3000` 的本地真实浏览器验证相关。该文件在本轮开始时已经 dirty，未纳入本轮提交 |
| `web/` | `src/tests/e2e/full-fixtures.ts` | 当前 diff 将全量用户列表查询改为按用户名分页查询，并把 `userId(...)` 改为 async；这可降低历史 E2E 数据膨胀导致固定 `pageSize=100` 找不到账号的风险。该文件在本轮开始时已经 dirty，未纳入本轮提交 |

上述归因不改变文件状态；剩余 dirty 文件仍需后续由用户或明确任务确认后再决定提交、保留或回滚。

### 2026-05-17 Dockerfile 构建尝试

| 命令 | 结果 |
| --- | --- |
| `cd server && docker build -f Dockerfile -t aubb-server:dirty-check .` | 未完成；构建在拉取/解析 `maven:3.9.11-eclipse-temurin-25` 与 `eclipse-temurin:25-jre` 基础镜像 metadata 阶段超过 2 分钟无进展 |

该构建是为验证剩余 dirty `server/Dockerfile` 的可构建性而启动的临时检查；未运行容器、未删除 volumes。随后只终止了该 `docker build`/`buildx` 验证进程，并确认 `docker ps` 无运行容器。该项不能作为 Dockerfile 构建通过证据。

### 2026-05-17 Compose 静态配置补充

| 命令 | 结果 |
| --- | --- |
| `cd server && docker compose config --quiet` | 通过，退出码 0 |
| `cd server && docker compose --profile app config --quiet` | 通过，退出码 0 |

该验证只检查 `server/compose.yaml` 可解析性，不创建或启动容器；真实依赖、后端 readiness 和 OpenAPI 仍需 E2E 密码变量可用后重新启动验证。

### 2026-05-17 Dockerfile 静态检查补充

| 命令 | 结果 |
| --- | --- |
| `cd server && docker image inspect maven:3.9.11-eclipse-temurin-25 eclipse-temurin:25-jre` | 基础镜像本地不存在 |
| `cd server && docker build --check --progress=plain -f Dockerfile .` | 未完成；同样卡在 Docker Hub 基础镜像 metadata 阶段，随后终止该临时验证进程 |

因此当前仍没有 `server/Dockerfile` 构建通过证据；已知限制是基础镜像未缓存且 registry metadata 请求无进展。

### 2026-05-17 Diff 格式检查补充

| 命令 | 结果 |
| --- | --- |
| `cd server && git diff --check` | 通过，退出码 0 |
| `cd web && git diff --check` | 通过，退出码 0 |
| `cd docs && git diff --check` | 通过，退出码 0 |

该检查仅覆盖当前工作区 diff 的空白和补丁格式问题；不替代真实服务或浏览器验证。

### 2026-05-17 恢复后阻塞复核

| 检查项 | 当前证据 |
| --- | --- |
| `server/` dirty | `M Dockerfile`，仍为本轮开始时已记录的既有 dirty 文件 |
| `web/` dirty | `M next.config.ts`、`M src/tests/e2e/full-fixtures.ts`，仍为本轮开始时已记录的既有 dirty 文件 |
| `docs/` dirty | 追加本段前为 clean；追加本段后仅包含本审计记录 |
| E2E 密码变量 | `AUBB_E2E_ADMIN_PASSWORD`、`AUBB_E2E_TEACHER_PASSWORD`、`AUBB_E2E_STUDENT_PASSWORD`、`AUBB_E2E_TEMP_USER_PASSWORD` 均为 `MISSING` |

本次只执行变量存在性检查，没有打印任何密码值。由于四个真实 E2E 密码变量仍不可见，继续遵守计划硬门禁：不启动 `127.0.0.1:18080` 后端、不启动 `127.0.0.1:3000` 前端、不启动 Docker 依赖、不运行真实浏览器 E2E。

### 2026-05-17 E2E 变量来源排查

| 检查项 | 当前证据 |
| --- | --- |
| 当前 shell | 四个 `AUBB_E2E_*_PASSWORD` 变量均为 `ENV_MISSING` |
| `launchctl getenv` | 四个变量均为 `LAUNCHCTL_MISSING` |
| 常见 shell 配置 | `$HOME/.zshenv`、`$HOME/.zprofile`、`$HOME/.zshrc`、`$HOME/.profile`、`$HOME/.bash_profile`、`$HOME/.bashrc` 中未检出这四个变量名 |

本次只检查变量是否存在或变量名是否出现，没有读取、打印或落盘任何密码值。当前证据说明阻塞不是单纯的 `launchctl` 到 shell 传播问题；在本执行环境可见范围内，四个真实 E2E 密码变量尚未配置。

### 2026-05-17 E2E 环境加载入口排查

| 检查项 | 当前证据 |
| --- | --- |
| 仓库内变量名来源 | 仅 `plan.md`、本执行日志、`web/src/tests/e2e/README.md`、`web/src/tests/e2e/real-backend.ts` 命中四个密码变量名 |
| 本地 env 模板 | `server/deploy/.env.uat.example`、`.env.staging.example`、`.env.production.example` 存在，但未作为 E2E 密码变量模板 |
| 自动加载入口 | 根目录、`server/`、`web/`、`docs/` 下未发现 `.envrc`、Justfile、项目级 Makefile 或 mise 配置 |
| E2E README | 明确真实密码必须从环境变量提供，默认账号标识为 `U-SA1`、`U-TA1`、`U-ST1` |

本次仍只记录路径和变量名命中情况，没有读取或打印任何密码值。当前可见仓库内容没有提供替代的本地加载机制；真实服务启动链路仍等待四个 `AUBB_E2E_*_PASSWORD` 进入当前执行环境。

### 2026-05-17 Playwright 环境加载确认

| 检查项 | 当前证据 |
| --- | --- |
| `web/package.json` | `test:e2e` 直接执行 `playwright test` |
| `web/playwright.config.ts` | 通过 `process.env.AUBB_E2E_REAL_BACKEND` 和 `process.env.PLAYWRIGHT_TEST_BASE_URL` 读取环境 |
| dotenv / loadEnv | `package.json`、`playwright.config.ts` 和 `web/src/tests/e2e` 中未发现 dotenv 或自定义 env 文件加载逻辑 |
| E2E 密码读取 | `web/src/tests/e2e/real-backend.ts` 的 `requiredEnv(...)` 直接从 `process.env` 读取四个密码变量 |

因此真实 E2E 运行前，四个 `AUBB_E2E_*_PASSWORD` 必须已经存在于当前命令环境；当前仓库代码不会自动从本地文件加载它们。

### 2026-05-17 基线 Step 2 阻塞复核

| 检查项 | 当前证据 |
| --- | --- |
| 当前 shell | `AUBB_E2E_ADMIN_PASSWORD`、`AUBB_E2E_TEACHER_PASSWORD`、`AUBB_E2E_STUDENT_PASSWORD`、`AUBB_E2E_TEMP_USER_PASSWORD` 均为 `MISSING`；检查命令退出码 1 |
| `launchctl getenv` 判断 | 对存在变量名和不存在变量名均返回退出码 0，因此不能用退出码判断变量存在性；捕获输出并只判断是否为空后，四个 `AUBB_E2E_*_PASSWORD` 变量仍为 `MISSING` |
| `server/` dirty | `M Dockerfile`，为本轮恢复时已存在改动，未回滚、未提交 |
| `web/` dirty | `M next.config.ts`、`M src/tests/e2e/full-fixtures.ts`，为本轮恢复时已存在改动，未回滚、未提交 |
| `docs/` dirty | `M 06-testing-and-ops/plan-execution-log.md`，来自本阻塞记录 |
| 服务状态 | `127.0.0.1:18080`、`127.0.0.1:3000` 均 `NOT_LISTENING`；`docker ps` 无运行容器 |

本次只检查变量是否存在，没有打印、写入或提交任何密码值。由于 `plan.md` 的真实环境启动与基线 Step 2 仍未满足，继续暂停真实执行：不启动 Docker 依赖、不启动后端 `127.0.0.1:18080`、不启动前端 `127.0.0.1:3000`、不运行真实 Playwright E2E。该阻塞不能作为完成证据，目标未达到生产上线门禁。

### 2026-05-17 当前会话 Step 2 阻塞复核

| 检查项 | 当前证据 |
| --- | --- |
| 执行计划与约束 | 已重新读取 `plan.md`、`server/AGENTS.md`、`web/AGENTS.md`，继续使用 `superpowers:executing-plans`；当前仍停在真实环境启动与基线 Step 2 |
| 子仓库 dirty | `server/`: `M Dockerfile`；`web/`: `M next.config.ts`、`M src/tests/e2e/full-fixtures.ts`；`docs/`: `M 06-testing-and-ops/plan-execution-log.md` |
| E2E 密码变量 | `AUBB_E2E_ADMIN_PASSWORD`、`AUBB_E2E_TEACHER_PASSWORD`、`AUBB_E2E_STUDENT_PASSWORD`、`AUBB_E2E_TEMP_USER_PASSWORD` 均为 `MISSING`；检查命令退出码 1 |
| 服务状态 | `127.0.0.1:18080` 和 `127.0.0.1:3000` 均无监听；`docker ps` 无运行容器 |

本次只检查变量存在性，没有打印、写入或提交任何密码值。由于四个真实 E2E 密码变量仍未进入当前命令环境，继续按硬门禁暂停：不启动 Docker 依赖、不启动后端、不启动前端、不运行真实 Playwright E2E。

### 2026-05-17 文档构建补充验证

| 命令 | 结果 |
| --- | --- |
| `cd docs && npm run docs:build` | 通过；最新复跑 VitePress `build complete in 2.21s` |

该验证只证明当前 `docs/` 文档站仍可构建，不能替代真实依赖、真实后端、真实前端和真实浏览器 E2E 门禁。

### 2026-05-17 前端静态与单元回归复跑

| 命令 | 结果 |
| --- | --- |
| `cd web && npm run lint` | 通过，退出码 0 |
| `cd web && npm run typecheck` | 通过，退出码 0 |
| `cd web && npm run test` | 通过；Vitest `11 passed` test files，`24 passed` tests |
| `cd web && AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` | 通过；Next.js 编译、TypeScript、30 个静态页面生成均成功 |

该验证只覆盖前端静态检查与单元测试；真实后端 Playwright、真实依赖和三角色登录基线仍等待 E2E 密码变量进入当前命令环境。

### 2026-05-17 后端回归复跑

| 命令 | 结果 |
| --- | --- |
| `cd server && python3 scripts/api-tests/permission/e2e_permission_realrun_test.py` | 通过；`Ran 1 test`，`OK` |
| `cd server && bash ./mvnw spotless:check` | `BUILD SUCCESS`；Spotless 检查 531 个 Java 文件，0 个文件需要修改 |
| `cd server && bash ./mvnw verify` | `BUILD SUCCESS`；Tests run: 318，Failures: 0，Errors: 0，Skipped: 0 |

`mvn verify` 使用 Testcontainers 启动了临时 PostgreSQL、MinIO、RabbitMQ、go-judge 与 Ryuk 容器；命令结束后等待 Ryuk 自动清理，`docker ps` 仅输出表头。`127.0.0.1:18080` 和 `127.0.0.1:3000` 仍无监听。本段验证不包含真实本地前端、三角色登录基线或 Playwright E2E。

### 2026-05-17 工作区 diff 质量检查

| 仓库 | 命令 | 结果 |
| --- | --- | --- |
| `server/` | `git diff --check` | 通过，退出码 0 |
| `web/` | `git diff --check` | 通过，退出码 0 |
| `docs/` | `git diff --check` | 通过，退出码 0 |

### 2026-05-17 Playwright mock 禁用静态复核

| 命令 | 结果 |
| --- | --- |
| `cd web && rg -n "page\\.route\\(|context\\.route\\(|browserContext\\.route\\(|route\\.fulfill\\(|route\\.abort\\(|route\\.continue\\(" src/tests/e2e \|\| true` | 无命中 |
| `cd web && rg -n "mock|msw|route\\.fulfill|page\\.route|context\\.route" src/tests/e2e \|\| true` | 无命中 |
| `cd web && npx playwright test --list --project=chromium` | 可发现 10 个 E2E spec 文件、36 个测试标题 |

该复核只证明当前 E2E 源码未使用 Playwright 网络拦截或明显 mock 关键字；真实后端 E2E 仍需在 E2E 密码变量注入后连接本地 `127.0.0.1:18080` 与 `127.0.0.1:3000` 重跑。

### 2026-05-17 dirty 文件敏感词计数复核

| 仓库 | 命令范围 | 结果 |
| --- | --- | --- |
| `server/` | 对当前 dirty 文件运行敏感关键词计数，不打印匹配行 | 无命中 |
| `web/` | 对当前 dirty 文件运行敏感关键词计数，不打印匹配行 | `src/tests/e2e/full-fixtures.ts` 有 3 处关键词命中 |
| `docs/` | 对当前 dirty 文件运行敏感关键词计数，不打印匹配行 | 当前执行日志有 42 处关键词命中 |

该复核只输出文件名和计数，不打印、写入或提交任何密码、token、cookie、JWT、私钥或真实连接串。命中来自测试变量名、认证术语和“不要记录敏感值”的执行记录；真实 E2E 密码变量仍未注入当前命令环境。

### 2026-05-17 当前恢复轮补充复核

| 检查项 | 命令 / 证据 | 结果 |
| --- | --- | --- |
| 文档构建 | `cd docs && npm run docs:build` | 通过；VitePress `build complete in 2.24s` |
| 前端生产构建 | `cd web && AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` | 通过；Next.js 编译、TypeScript、30 个静态页面生成均成功 |
| 工作区状态 | `git status --short --branch` 分别在 `server/`、`web/`、`docs/` 执行 | `server/` 仍仅 `M Dockerfile`；`web/` 仍仅 `M next.config.ts`、`M src/tests/e2e/full-fixtures.ts`；`docs/` 在追加本段前为 clean |
| 服务状态 | `curl --max-time 2 -fsS` 检查 `127.0.0.1:18080` 和 `127.0.0.1:3000` | 后端和前端均不可访问；本轮未启动 Docker、后端、前端或 Playwright |

本段是阻塞期间可执行的非账号、非真实服务门禁补充。真实依赖、真实后端、真实前端、三角色登录基线和 `AUBB_E2E_REAL_BACKEND=1 npm run test:e2e` 仍必须等待用户确认 `环境变量已注入` 后再执行；当前 goal 不能标记完成。

## 2026-05-17 本轮 plan.md 重新执行记录

### Phase 0：重新读取计划与初始 Git 状态

| 检查项 | 当前证据 |
| --- | --- |
| 计划来源 | 已完整读取根目录 `/Users/moorefoss/Code/AUBB/plan.md`，共 785 行；本轮以该文件的 0-5 阶段、19 个任务和完成门禁为主规范 |
| 仓库边界 | 根目录不是 Git 仓库；`find . -maxdepth 3 -name .git -type d` 仅发现 `./server/.git`、`./web/.git`、`./docs/.git` |
| `server/` 初始状态 | `main...origin/main [ahead 1]`；`M Dockerfile`；当前 HEAD `32aea14` |
| `web/` 初始状态 | `main...origin/main [ahead 1]`；`M next.config.ts`、`D plan.md`、`M src/tests/e2e/full-fixtures.ts`、`D todo.md`；当前 HEAD `f9b0245` |
| `docs/` 初始状态 | `main...origin/main [ahead 18]`；本轮修改前 `git status --short --branch` 无未提交条目；当前 HEAD `3683991` |
| 旧报告处理 | 2026-05-16 和更早执行记录仅作为线索；本轮结论必须来自当前命令、当前代码和当前运行结果 |

### Phase 1：结构、技术栈、命令与测试资产重新核验

| 核验项 | 命令 / 文件 | 当前事实 |
| --- | --- | --- |
| 后端规范 | `server/AGENTS.md` | 默认中文；修改前记录 Git 状态；完成前必须有真实验证证据；commit summary 使用中文 |
| 前端规范 | `web/AGENTS.md` | Next.js 16 项目；UI 改动需遵守现有设计约束；真实问题优先系统化排查和验证 |
| 后端技术栈 | `server/pom.xml`、`./mvnw -v` | Spring Boot `4.0.5`、Java `25.0.3`、Maven `3.9.14`、MyBatis-Plus、Flyway、PostgreSQL、RabbitMQ、Redis、MinIO、go-judge |
| 前端技术栈 | `web/package.json` | Next.js `16.2.4`、React `19.2.4`、TypeScript、Tailwind、Vitest、Playwright |
| 文档技术栈 | `docs/package.json` | VitePress；命令为 `docs:dev`、`docs:build`、`docs:preview` |
| 依赖服务 | `server/compose.yaml` | PostgreSQL、RabbitMQ、MinIO、Redis、go-judge；可选 app/judge-worker profile |
| 后端配置 | `server/src/main/resources/application.yaml` | readiness 包含 `db`、`redisEnhancement`、`minioStorage`、`goJudge`、`judgeQueue`；JWT secret 必须来自环境变量 |
| Playwright 配置 | `web/playwright.config.ts` | `AUBB_E2E_REAL_BACKEND=1` 时 `workers=1`、单测超时 `90_000`，默认 baseURL 为 `http://127.0.0.1:3000` |
| E2E 说明 | `web/src/tests/e2e/README.md` | 真实 E2E 连接本地后端 `18080`、前端 `3000` 和本地 Docker 依赖；报告中不得记录 token/cookie/JWT/密码值 |
| fixture 密码策略 | 根目录 `plan.md` Step 2 | 本轮按计划使用本地固定 fixture 用户 `U-SA1`、`U-TA1`、`U-ST1`，测试密码固定为计划内本地值；不再沿用旧执行记录中“等待外部密码变量”的阻塞判断 |

### Phase 2：当前代码事实扫描

| 清单 | 命令 | 当前结果 |
| --- | --- | --- |
| 前端业务页面 | `find src/app -name page.tsx \| sort` | 45 个 `page.tsx`，覆盖公共/认证、管理员、教师、学生四类路由 |
| 后端 Controller | `rg --files src/main/java/com/aubb/server/modules \| rg '/api/.*Controller\\.java$'` | 33 个 Controller |
| 前端 API 封装 | `find src/features -path '*/api/*' -type f \| sort` | 20 个领域 API 文件 |
| 后端测试资产 | `find src/test/java/com/aubb/server -type f -name '*Test*.java' -o -name '*Tests.java'` | 覆盖 auth、权限、课程、作业、提交、判题、成绩、实验、通知、Redis、MinIO、go-judge 等集成/单元测试 |
| 前端测试资产 | `find src/tests -type f \| sort` | 10 个 E2E spec/fixture/helper 文件，11 个 unit/contract 测试文件 |
| 控件源码线索 | `rg -n "Button|button|onClick|type=\"submit\"|Dialog|Dropdown|Switch|FileUpload|Download|下载|上传|保存|创建|新增|编辑|删除|发布|关闭|归档|撤销|导入|导出|刷新|搜索|筛选|恢复|重置" src/app src/features src/shared` | 当前扫描返回 1112 行命中，作为按钮级测试矩阵的源码输入；后续以真实 DOM 与 Playwright 结果收敛 |

### 下一步

启动真实 Docker 依赖、真实后端 `127.0.0.1:18080` 和真实前端 `127.0.0.1:3000`，然后执行 readiness、OpenAPI、权限 fixture 和三角色登录基线。所有敏感值只在命令环境中使用，不写入报告。

### Phase 3：真实依赖、后端、前端与登录基线

| 验证项 | 命令 / 操作 | 当前结果 |
| --- | --- | --- |
| 端口预检 | `lsof -nP -iTCP:18080 -sTCP:LISTEN`、`lsof -nP -iTCP:3000 -sTCP:LISTEN` | 启动前均无监听 |
| Docker 依赖启动 | `cd server && docker compose up -d postgres rabbitmq minio redis go-judge && docker compose ps` | PostgreSQL、RabbitMQ、MinIO、Redis 均 healthy，go-judge running |
| 后端第一次启动 | 按 `plan.md` 使用 `AUBB_BOOTSTRAP_SCHOOL_CODE=S1` 启动 | 失败；根因是本地持久化数据库已有唯一学校根节点 `SCH-REALRUN`，bootstrap 保护逻辑拒绝改为 `S1` |
| 根因复核 | 查询 `org_units` 和 `users`；读取 `PlatformBootstrapApplicationService` | `org_units` 现有根节点为 `SCH-REALRUN`；当配置 code 与现有根节点不一致时会抛出 `IllegalStateException`；没有清库或删除数据 |
| 后端第二次启动 | 保持本地 Docker 依赖，改用现有根节点 code `SCH-REALRUN` 启动 bootstrap | 成功；Tomcat 监听 `18080`，Flyway 48 个迁移已验证，bootstrap 完成且未重复创建根节点 |
| 后端 readiness | `curl -fsS http://127.0.0.1:18080/actuator/health/readiness` | `status=UP`；components 包含 `db`、`goJudge`、`judgeQueue`、`minioStorage`、`readinessState`、`redisEnhancement` |
| OpenAPI | `curl -fsS http://127.0.0.1:18080/v3/api-docs \| python3 -c ...` | OpenAPI `3.1.0`，`124` 个 paths |
| 权限 fixture | `BASE_URL=http://127.0.0.1:18080 ADMIN_USERNAME=U-SA1 ADMIN_PASSWORD=... bash scripts/api-tests/permission/run_permission_e2e.sh` | 通过；`caseCount=22`、`passedCount=22`、`failedCount=0`；报告只记录变量名，不记录密码值 |
| 前端启动 | `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run dev -- --hostname 127.0.0.1 --port 3000` | Next.js 16.2.4 dev server 就绪，监听 `127.0.0.1:3000` |
| 登录页探针 | `curl -fsS -o /tmp/aubb-login.html -w '%{http_code} ...' http://127.0.0.1:3000/login` | HTTP `200` |
| 三角色登录基线 | `AUBB_E2E_REAL_BACKEND=1 ... npx playwright test src/tests/e2e/auth.spec.ts --project=chromium` | Chromium 5 个真实后端用例全部通过；管理员、教师、学生登录、退出、学生访问管理员页面负例通过 |

偏差说明：`plan.md` 指定 bootstrap school code 为 `S1`，但当前本地 PostgreSQL volume 已有 `SCH-REALRUN` 学校根节点。为遵守“不覆盖用户未提交变更/不破坏本地数据”，本轮没有清空 volume，而是按当前数据库事实改用既有根节点 code 启动 bootstrap；该偏差将在最终报告中列为本地环境偏差。

### Phase 4：全量清单、契约和按钮级 full suites

| 验证项 | 命令 / 证据 | 当前结果 |
| --- | --- | --- |
| OpenAPI 路径枚举 | 从当前 `http://127.0.0.1:18080/v3/api-docs` 保存 `/tmp/aubb-openapi.json` 后枚举 | OpenAPI `3.1.0`、`124` paths；覆盖 admin、auth、me、teacher、actuator 路径族 |
| Playwright mock 静态复核 | `rg -n "page\\.route\\(|context\\.route\\(|browserContext\\.route\\(|route\\.fulfill\\(|route\\.abort\\(|route\\.continue\\(|mock|msw" src/tests/e2e \|\| true` | 无命中 |
| Playwright 测试发现 | `npx playwright test --list --project=chromium` | 10 个 spec 文件，36 个测试标题 |
| 管理端 full suite | `AUBB_E2E_REAL_BACKEND=1 ... npx playwright test src/tests/e2e/full-admin.spec.ts --project=chromium` | `5 passed`；覆盖 auth refresh/revoke、平台配置、组织、用户治理/CSV、学期/模板/开课、审计、权限解释 |
| 课程 full suite | `... npx playwright test src/tests/e2e/full-course.spec.ts --project=chromium` | `5 passed`；覆盖教学班、成员、功能开关、资源上传下载、讨论锁定、题库、判题环境 |
| 作业/提交/判题 full suite | `... npx playwright test src/tests/e2e/full-assignment-judge.spec.ts --project=chromium` | `3 passed`；覆盖作业生命周期、学生提交、附件下载、workspace、样例运行、正式判题、教师评分和重判 |
| 成绩/实验/通知 full suite | `... npx playwright test src/tests/e2e/full-grading-lab-notification.spec.ts --project=chromium` | `3 passed`；覆盖成绩导出/导入/发布、实验附件/评阅、通知已读 |
| 导航/权限/响应式 full suite | `... npx playwright test src/tests/e2e/full-navigation-permission.spec.ts --project=chromium` | `3 passed`；覆盖三角色导航、顶栏搜索、用户菜单、路由守卫、401/403、桌面和移动关键操作 |

当前 full suite 小计：`19 passed`。下一步运行完整真实后端 Playwright 套件 `npm run test:e2e`，同时覆盖 smoke specs。

### Phase 5：完整门禁与收尾结果

| 验证项 | 命令 / 证据 | 当前结果 |
| --- | --- | --- |
| 完整真实后端 Playwright | `cd web && AUBB_E2E_REAL_BACKEND=1 AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 PLAYWRIGHT_TEST_BASE_URL=http://127.0.0.1:3000 ... npm run test:e2e` | `36 passed`，约 2.4 分钟；覆盖 10 个 E2E spec；报告只记录账号变量名，不记录密码值 |
| 前端 lint | `cd web && npm run lint` | 通过，退出码 0 |
| 前端 typecheck | `cd web && npm run typecheck` | 通过，退出码 0 |
| 前端 unit/contract | `cd web && npm run test` | `11` 个 test files / `24` tests 全部通过 |
| 前端生产构建 | `cd web && AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` | 通过；Next.js 编译、TypeScript、30 个静态页面生成均成功 |
| 后端 permission realrun | `cd server && scripts/api-tests/permission/run_permission_e2e.sh` | `caseCount=22`、`passedCount=22`、`failedCount=0` |
| 后端格式门禁 | `cd server && bash ./mvnw spotless:check` | `BUILD SUCCESS` |
| 后端全量 verify | `cd server && bash ./mvnw verify` | `BUILD SUCCESS`；Tests run: `318`，Failures: `0`，Errors: `0`，Skipped: `0`；总耗时 `05:24 min` |
| 文档构建 | `cd docs && npm run docs:build` | 通过；VitePress build 完成 |

本轮真实环境偏差：`plan.md` 的示例 bootstrap school code 为 `S1`，但当前本地 PostgreSQL volume 已存在唯一学校根节点 `SCH-REALRUN`。本轮未清库、未删除 volume，而是按现有根节点 code 启动后端；这是为了避免破坏本地持久化数据。

### Phase 6：本地服务清理

| 项目 | 当前结果 |
| --- | --- |
| 后端 `18080` | `spring-boot:run` 会话已退出；收尾时 Maven `BUILD SUCCESS`；`curl --max-time 2 http://127.0.0.1:18080/actuator/health/readiness` 连接失败 |
| 前端 `3000` | Next dev server 会话已退出；`curl --max-time 2 http://127.0.0.1:3000/login` 连接失败 |
| Docker compose | `cd server && docker compose down` 已执行；`docker compose ps` 无运行服务；未删除 volumes |

### Phase 7：最终工作区复核

| 复核项 | 当前结果 |
| --- | --- |
| `server/` diff check | `git diff --check` 通过；当前 `main...origin/main [ahead 1]`，保留 `Dockerfile` 中容器 healthcheck 所需的 `curl` 安装，恢复 BuildKit cache 行 |
| `web/` diff check | `git diff --check` 通过；当前 `main...origin/main [ahead 1]`，保留 `next.config.ts` 的本地 dev origin 配置和 `src/tests/e2e/full-fixtures.ts` 的用户分页查询修正；已恢复不必要删除的 `plan.md` 与 `todo.md` |
| `docs/` diff check | `git diff --check` 通过；当前 `main...origin/main [ahead 18]`，本轮追加三份报告并清理过期收尾记录 |
| 文档构建 | `cd docs && npm run docs:build` 通过；VitePress build 完成 |
| 敏感词文件级复核 | 对 `docs/` 当前 dirty 文件只输出文件名和计数；命中来自 `password`/`token`/`cookie`/`JWT` 等审计说明和环境变量名，未打印或写入任何真实凭据值 |

## 10. 2026-05-17 作业结构化答题闭环补齐

本段记录作业功能专项收敛，目标是补齐教师组卷、学生结构化作答、自动评分、人工评分和真实浏览器 E2E 中缺失的题型与交互证据。

### 后端变更

| 项目 | 当前结果 |
| --- | --- |
| 填空题题型 | 新增 `FILL_BLANK` 到 `AssignmentQuestionType`，并追加 Flyway 迁移 `V49__fill_blank_question_type.sql` |
| 组卷校验 | `StructuredQuestionSupport` 要求填空题无选项且必须配置 `referenceAnswer` |
| 自动评分 | `SubmissionAnswerApplicationService` 对填空题执行 trim 后精确匹配；大小写保持敏感；命中得满分，否则 0；反馈为“填空题自动判分完成” |
| API 安全 | 学生侧作业详情不暴露填空题 `referenceAnswer` |
| 集成测试 | `StructuredAssignmentIntegrationTests#fillBlankQuestionUsesTrimmedExactMatchAutoScoring` 覆盖题库创建、发布作业、学生提交、trim 命中、错误答案 0 分和参考答案不可见 |

### 前端变更

| 项目 | 当前结果 |
| --- | --- |
| 学生作业详情 | 从仅依赖作业列表数据改为读取 `/api/v1/me/assignments/{assignmentId}`，按结构化试卷渲染专用控件 |
| 专用答题控件 | 单选 radio、多选 checkbox、填空输入框、Markdown 简答编辑/预览、文件题格式/大小/数量提示与上传、编程题跳转在线 IDE |
| 草稿与提交 | 非编程题按题目自动写入 localStorage，刷新后恢复；提交前做必填校验；提交时自动附加当前编程工作区快照 |
| 教师组卷 | `PaperEditor` 支持选择填空题、配置参考答案，并补齐文件上传题限制配置 |
| Multipart 上传 | `postForm` 不再手工固定 multipart `Content-Type`，改由浏览器/运行时写入 boundary |
| 类型与缓存 | OpenAPI 生成类型、assignment API、query key 与 hooks 已同步 `FILL_BLANK` 和学生作业详情接口 |

### 真实验证证据

| 验证项 | 结果 |
| --- | --- |
| 后端专项集成测试 | `StructuredAssignmentIntegrationTests` 共 `12 passed` |
| 前端结构化单元测试 | `src/tests/unit/submission/structured-answer-form.test.tsx`、`structured-submission.test.ts` 和 `api/http-form.contract.test.ts` 共 `6` 个测试通过 |
| 前端静态门禁 | `npm run typecheck`、`npm run lint` 均通过 |
| 前端生产构建 | `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` 通过 |
| 作业真实后端 E2E | 已执行完整 `npm run test:e2e`，`36 passed`；其中 `full-assignment-judge.spec.ts` 覆盖学生通过真实 UI 完成单选、多选、填空、Markdown 简答、文件题提交、草稿恢复、提交历史、提交详情、附件下载、编程工作区、样例运行、正式判题、教师评分和重判 |

### 提交前复核说明

| 项目 | 当前结果 |
| --- | --- |
| 当前 shell E2E 变量 | `AUBB_E2E_ADMIN_PASSWORD`、`AUBB_E2E_TEACHER_PASSWORD`、`AUBB_E2E_STUDENT_PASSWORD`、`AUBB_E2E_ASSISTANT_PASSWORD` 当前未设置 |
| 后端专项验证 | `cd server && bash ./mvnw -Dtest=StructuredAssignmentIntegrationTests test` 通过；Tests run: `12`，Failures: `0`，Errors: `0`，Skipped: `0` |
| 后端全量验证 | `cd server && bash ./mvnw verify` 通过；Tests run: `319`，Failures: `0`，Errors: `0`，Skipped: `0`；V49 迁移在 Testcontainers schema 中被多次校验 |
| 前端静态验证 | `cd web && npm run typecheck`、`cd web && npm run lint` 均通过，退出码 0 |
| 前端单元验证 | `cd web && npm run test` 通过；`14` 个 test files / `30` tests 全部通过 |
| 前端构建验证 | `cd web && AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run build` 通过；Next.js 编译、TypeScript、30 个静态页面生成均完成 |
| 文档验证 | `cd docs && npm run docs:build` 通过；`git diff --check` 通过 |
| 当前处理策略 | 当前 shell 未重跑真实浏览器 E2E；真实浏览器 E2E 以本段已有执行证据记录，不伪造重跑结果 |
| 残余风险 | 文件上传题的超大文件真实上传、浏览器 file chooser 交互和成绩发布后的所有学生展示路径仍依赖更长时间的真实浏览器扩展套件持续覆盖 |

## 11. 2026-05-18 WebIDE 真实全流程验证

本段记录 WebIDE 专项真实闭环执行。目标是使用本地 Docker 依赖、后端 `127.0.0.1:18080`、前端 `127.0.0.1:3000` 和真实浏览器完成教师创建/发布编程题作业、学生 WebIDE 编辑保存、历史查看、样例运行和正式提交判题。全程未使用 Playwright route mock 或 MSW；API 仅用于 fixture 准备与后验核验。

### 环境与数据

| 项目 | 当前结果 |
| --- | --- |
| 环境加载 | `scripts/aubb-env.sh` 已兼容 zsh sourced 场景；`zsh -lc 'source scripts/aubb-env.sh && load_aubb_env ...'` 可正确解析 `/Users/moorefoss/Code/AUBB` 并加载 E2E 变量 |
| 健康检查 | `just healthcheck-strict` 通过；确认 Docker 工具、`env/e2e.env`、后端 `18080`、前端 `3000`、后端 readiness/OpenAPI 与前端登录页可用 |
| fixture 数据 | 使用现有真实后端 helper 创建动态 E2E 学生/教学班/作业；教师端 UI 新增 Python3 判题环境配置；保留本地 `E2E-*` 残留记录 |

### 修复项

| 问题 | 修复 |
| --- | --- |
| zsh 下 `load_aubb_env` 无法加载变量 | `scripts/aubb-env.sh` 不再只依赖 `BASH_SOURCE[0]`；zsh sourced 时使用 zsh source path 计算工作区根目录 |
| 教师创建结构化编程题作业返回 400 | 创建/编辑页默认不再提交空的 assignment 级 `judgeConfig`；空白 `judgeConfig JSON` 解析为 `undefined`，避免与结构化 `paper` 冲突 |
| `datetime-local` 原始值导致后端反序列化失败 | 创建/编辑页统一将 `datetime-local` 转为 ISO datetime 后提交 |
| PaperEditor 切换编程题会回退为单选题 | 题型切换改为一次性更新 question 对象，并补单元测试覆盖 |
| 教师端缺少编程题关键 UI 配置字段 | PaperEditor 补齐样例试运行、样例输入/期望输出、源码文件约束、Python3、入口文件、测试用例、模板文件等配置 |
| 学生 WebIDE 题目内容偶发不显示 | 工作区页面改为读取 `/api/v1/me/assignments/{assignmentId}` 详情，而不是依赖作业列表摘要 |
| 判题环境表格分页导致新增项不可见 | E2E 仍通过 UI 新增配置，保存后用真实后端列表做后验确认 |

### 真实验证证据

| 验证项 | 结果 |
| --- | --- |
| WebIDE 真实闭环 | `cd web && source ../scripts/aubb-env.sh && load_aubb_env && AUBB_E2E_REAL_BACKEND=1 PLAYWRIGHT_TEST_BASE_URL=http://127.0.0.1:3000 AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npx playwright test src/tests/e2e/webide-real-flow.spec.ts --project=chromium --reporter=list` 通过；`1 passed` |
| 作业回归真实 E2E | 同环境执行 `npx playwright test src/tests/e2e/full-assignment-judge.spec.ts --project=chromium --reporter=list` 通过；`3 passed` |
| 前端 lint | `cd web && npm run lint` 通过，退出码 0 |
| 前端 typecheck | `cd web && npm run typecheck` 通过，退出码 0 |
| 前端目标单测 | `cd web && npm test -- src/tests/unit/assignment/assignment-form.test.ts src/tests/unit/api/mappers.contract.test.ts src/tests/unit/assignment/paper-editor.test.tsx` 通过；`3` 个 test files / `10` tests |
| 后端目标测试 | `cd server && bash ./mvnw -Dtest=JwtTokenServiceTests,AuthApiIntegrationTests test` 通过；Tests run: `14`，Failures: `0`，Errors: `0`，Skipped: `0` |
| 权限脚本语法 | `cd server && python3 -m py_compile scripts/api-tests/permission/e2e_permission_realrun.py` 通过 |

### 已验证用户流程

| 流程 | 证据 |
| --- | --- |
| 教师判题环境配置 | 真实页面填写 profileCode、配置名称、Python3、runCommand 并点击“新增配置”；toast 成功后真实后端列表确认 profile 存在 |
| 教师创建并发布编程题作业 | 真实页面选择课程/教学班，填写标题、说明、时间、提交次数，添加编程题、样例、测试用例、模板文件，点击“创建作业”，随后在作业列表点击发布 |
| 学生进入 WebIDE | 真实页面打开 `/student/assignments/{assignmentId}/workspace/{questionId}`，确认题干、文件浏览器、Monaco、状态栏和 `main.py` |
| 编辑与保存 | 通过页面 Monaco model 更新编辑器内容，点击真实“保存”按钮；后端 workspace 轮询确认 `main.py` 持久化为新代码 |
| 历史与重置 | 点击“历史”并确认历史版本按钮可见；点击“重置”打开弹窗后取消，未破坏最终提交 |
| 样例运行 | 在“运行结果”填写样例输入/期望输出，点击“运行自测”；真实 go-judge 返回 `SUCCEEDED` / `ACCEPTED`，stdout 为 `3` |
| 正式提交 | 点击“提交”并确认弹窗；跳转提交详情页，真实 submission 与 judge job 完成，判题结果为 `ACCEPTED` 且得分等于满分 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 密钥处理 | 日志仅记录环境变量名和命令形态，未记录任何密码、token 或 cookie 值 |
| 本地数据 | 本轮按计划创建 `E2E-*` 残留业务记录，未清理本地数据库 |
| Monaco 交互 | 真实浏览器中仍通过页面编辑器状态修改代码并点击真实“保存”；为避免 Monaco 隐藏 textarea/逐字符输入抖动，测试使用 Monaco model 一次性设值 |

## 12. 2026-05-19 组织架构与课程成员作用域真实验证

本段记录学校层级组织架构专项真实闭环执行。目标是在本地 Docker 依赖、后端 `127.0.0.1:18080`、前端 `127.0.0.1:3000` 和真实 Chromium 中，使用前端界面完成学院、学期、课程模板、跨学院开课、教学班和课程成员作用域验证。全程未使用 Playwright route mock 或 MSW；API 仅用于登录、动态测试用户准备和后验断言。

### 修复项

| 问题 | 修复 |
| --- | --- |
| 开课管理缺少共同管理学院输入 | 管理端开课表单新增“共同管理学院”多选，并提交 `secondaryCollegeUnitIds` |
| 开课详情缺少跨学院与成员范围信息 | 开课详情展示主开课学院、共同管理学院和授课团队作用域说明 |
| 成员管理只暴露部分角色 | 成员页支持 `INSTRUCTOR`、`OFFERING_TA`、`CLASS_INSTRUCTOR`、`TA`、`STUDENT` 五类角色 |
| 成员角色与教学班绑定规则不清晰 | 整课角色禁用并清空教学班；班级角色和学生必须选择教学班，并在前端显示校验错误 |
| 班级下拉缺少唯一编码且长选项会覆盖按钮 | 教学班选项显示“名称 (编码)”，并给成员表单网格和 select 加入收缩约束 |
| 列表新增后依赖第一页可见 | 真实 E2E 改为等待 UI POST 成功，再按唯一编码调用真实 API 回查 |
| `datetime-local` 直接提交导致后端反序列化失败 | 开课创建/编辑提交前将本地 datetime-local 值转换为 ISO datetime |
| 无参数 query key 失效无法刷新活跃列表 | `queryKeys.admin.*()` 支持返回列表前缀 key，用于 mutation 后刷新匹配查询 |

### 真实验证证据

| 验证项 | 结果 |
| --- | --- |
| 环境门禁 | `just healthcheck-strict` 通过；确认 Docker、本地后端 `18080`、本地前端 `3000`、readiness、OpenAPI 与登录页可用 |
| 组织架构真实 E2E | `cd web && set -a; source ../env/e2e.env; set +a; AUBB_E2E_REAL_BACKEND=1 AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 PLAYWRIGHT_TEST_BASE_URL=http://127.0.0.1:3000 npx playwright test src/tests/e2e/full-organization-structure.spec.ts --project=chromium` 通过；`1 passed (11.6s)` |
| 前端静态门禁 | `cd web && npm run typecheck`、`cd web && npm run lint` 均通过 |
| 前端目标单测 | `cd web && npm test -- src/tests/unit/admin/course-offering-form.test.ts src/tests/unit/api/mappers.contract.test.ts src/tests/unit/api/query-keys.contract.test.ts src/tests/unit/course/member-role-binding.test.ts` 通过；`4` 个 test files / `13` tests |
| 后端全量回归 | `cd server && bash ./mvnw test` 通过；Tests run: `320`，Failures: `0`，Errors: `0`，Skipped: `0` |
| 工作区总门禁 | `just verify` 通过；后端 `320` tests / `0` failures / `0` errors，Web lint/typecheck 通过，Docs build 通过 |

### 已验证用户流程

| 流程 | 证据 |
| --- | --- |
| 管理员创建组织与教学基础数据 | 真实页面创建两个学院、学期、课程模板和跨学院开课；开课详情确认主学院、共同管理学院和初始主讲教师 |
| 教师创建教学班 | 初始主讲教师登录真实前端，在课程工作台创建两个教学班 |
| 教师成员管理 | 真实成员页添加整课教师、整课助教、班级教师、班级助教和学生，并用后端成员列表确认角色和教学班绑定 |
| 前端校验 | 学生未选教学班时前端阻止添加并显示“当前角色必须选择教学班”；整课教师切换后教学班下拉禁用并清空 |
| 后端边界 | 真实 API 验证缺班级、整课角色误带班级、跨开课教学班绑定、重复成员均返回明确失败原因；跨开课教学班返回“教学班不属于当前课程” |
| 作用域验证 | 整课教师可管理两个教学班，整课助教可读不可改；班级教师只看见并管理本班，班级助教只读本班，学生不能访问教师班级接口 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 密钥处理 | 日志仅记录环境变量名和命令形态，未记录任何密码、token、cookie 或 JWT 值 |
| 本地数据 | 本轮创建 `E2E-*` 学院、学期、课程模板、开课、教学班和临时用户；当前无通用删除 API，数据作为审计残留保留 |

## 13. 2026-06-08 空 stdin 与 STANDARD_IO 输出比较修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-008` 和 `BUG-20260607-015` 的后端阶段修复。目标是让无输入编程题成为合法教学场景，并让样例运行与正式 `STANDARD_IO` 判题共用默认宽松输出比较。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 编程题测试用例 `stdinText` | 作业创建和题库题目接口接受空字符串；请求体传入 `null` 或省略时在服务端归一化为空字符串 |
| 样例运行 `stdinText` | 自定义样例运行允许 `stdinText: ""`，不会回退到“缺少标准输入”错误 |
| 题目样例输入 | `sampleStdinText` 可为空字符串，服务端持久化为空输入 |
| `STANDARD_IO` 输出比较 | 样例运行和正式判题统一规范化 CRLF/LF，忽略行尾空白、末尾空行和最终换行差异 |
| 期望输出 | `expectedStdout` 仍需提供非空文本，避免无断言的测试点误判通过 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `AssignmentTeacherController` / `QuestionBankTeacherController` | 移除结构化编程题 `ProgrammingJudgeCaseRequest.stdinText` 的 `@NotBlank` 拦截，并在 DTO 转换时把 `null` 归一化为 `""` |
| `StructuredQuestionSupport` | 结构化编程题校验不再要求测试用例输入非空，只保留期望输出和分值校验 |
| `AssignmentPaperApplicationService` / `QuestionBankApplicationService` | 持久化配置前归一化 `sampleStdinText` 和 `judgeCases[].stdinText`，保证数据库 JSON 中无输入题稳定保存为空字符串 |
| `ProgrammingSampleRunApplicationService` | 自定义运行通过字段是否出现判断模式，空字符串输入不再被 `StringUtils.hasText` 当作缺失 |
| `JudgeExecutionService` | 移除样例运行空 stdin 拒绝；`toCaseOutcome` 使用宽松 `STANDARD_IO` 输出比较 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 正式判题空 stdin | 新增 `StructuredProgrammingJudgeIntegrationTests#standardIoJudgeAcceptsEmptyStdinAndFinalNewlineDifference` 后，修复前失败于 `POST /assignments` 返回 400 `MethodArgumentNotValidException` |
| 目标后端回归 | `cd server && bash ./mvnw -Dtest='StructuredAssignmentIntegrationTests#teacherCreatesProgrammingAssignmentWithEmptyJudgeStdin+teacherCreatesQuestionBankProgrammingQuestionWithEmptyJudgeStdin,ProgrammingWorkspaceIntegrationTests#sampleRunAcceptsOnlyFinalNewlineDifference,StructuredProgrammingJudgeIntegrationTests#standardIoJudgeAcceptsEmptyStdinAndFinalNewlineDifference' test` 通过；Tests run: `4`，Failures: `0`，Errors: `0`，Skipped: `0` |
| 相关集成回归 | `cd server && bash ./mvnw -Dtest='StructuredAssignmentIntegrationTests,ProgrammingWorkspaceIntegrationTests,StructuredProgrammingJudgeIntegrationTests' test` 通过；Tests run: `43`，Failures: `0`，Errors: `0`，Skipped: `0` |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成后端 RED-GREEN；仍需在最终业务闭环中用 Playwright MCP 复测作业创建、样例运行和正式提交 |
| UI diff 可读性 | 本次修复了默认判定语义；样例结果差异说明的前端可读性仍属于后续 WebIDE 体验阶段 |

## 14. 2026-06-08 作业列表总分摘要修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-009` 的后端契约修复。目标是让教师端和学生端作业列表稳定展示结构化作业总分，同时避免列表接口暴露完整题面、答案裁剪细节或隐藏判题配置。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 教师作业列表 | `GET /api/v1/teacher/course-offerings/{offeringId}/assignments` 的结构化作业列表项返回 `paper.sectionCount`、`paper.questionCount`、`paper.totalScore` |
| 学生作业列表 | `GET /api/v1/me/assignments` 的结构化作业列表项返回相同 `paper` 摘要，前端可直接用 `paper.totalScore` 展示总分 |
| 列表载荷边界 | 列表响应的 `paper.sections` 固定为空数组；完整题面、选项、答案裁剪和编程题判题配置仍只从详情接口读取 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `AssignmentPaperApplicationService` | 新增 `loadPaperSummary(assignmentId)`，按结构化试卷节数、题数和节总分计算列表摘要 |
| `AssignmentApplicationService` | 教师列表和学生当前作业列表从 `paper=null` 改为返回试卷摘要 |
| `StructuredAssignmentIntegrationTests` | 新增教师端和学生端列表断言，覆盖 `paper.totalScore`、`paper.questionCount` 和 `paper.sections=[]` |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 列表缺少总分摘要 | 新增 `StructuredAssignmentIntegrationTests#assignmentListsIncludeStructuredPaperScoreSummary` 后，修复前失败于教师作业列表 `$.items[0].paper` 为 `null` |
| 目标后端回归 | `cd server && bash ./mvnw -Dtest='StructuredAssignmentIntegrationTests#assignmentListsIncludeStructuredPaperScoreSummary' test` 通过；Tests run: `1`，Failures: `0`，Errors: `0`，Skipped: `0` |
| 相关集成回归 | `cd server && bash ./mvnw -Dtest='AssignmentIntegrationTests,StructuredAssignmentIntegrationTests' test` 通过；Tests run: `22`，Failures: `0`，Errors: `0`，Skipped: `0` |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成后端 RED-GREEN 和文档同步；仍需在最终业务闭环中用 Playwright MCP 复测教师端和学生端作业列表不再显示“暂无” |

## 15. 2026-06-08 成员表班级展示与添加结果清理

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-002` 和 `BUG-20260607-004` 的前端阶段复核与补强。目标是让成员表稳定展示教学班信息，并避免“添加成员”弹窗在继续录入下一名成员时保留上一轮成功 / 失败结果。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 成员表教学班列 | 成员列表使用 `className` 优先、`classCode` 兜底展示教学班；无班级绑定时显示“未绑定” |
| 成员写操作权限 | 班级助教只保留本班成员读取视图，不展示添加、导入、停用、转班操作；主讲教师和整课助教保留成员写操作 |
| 添加成员结果 | 添加成员弹窗在用户 ID、成员角色或教学班发生变化时调用 mutation reset，清理上一轮“添加成功 / 失败”结果 |
| 成员列表刷新 | 添加、导入、状态变更、转班 mutation 成功后继续 invalidate `queryKeys.course.members(offeringId)`，刷新当前成员查询 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `CourseMembersPage` | 将添加成员字段变化接入 `addMembersMutation.reset()`，保留已有成员列表 invalidate 逻辑 |
| `AddMemberDialog` | 增加 `onFieldChange` 回调，并在用户 ID、角色、教学班变化时触发 |
| `teacher-members-page.test.tsx` | 增加回归测试，先验证旧添加结果可见，再通过真实 combobox 交互断言字段变化会清理旧结果 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 修改添加成员输入不清理旧结果 | 新增 `CourseMembersPage clears previous add result when editing add member input` 后，修复前失败；`resetAddMembers` 期望调用 3 次、实际 0 次 |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/course/teacher-members-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `6 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `59 passed`，Tests: `154 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测成员页添加后继续录入、列表刷新和教学班列展示 |

## 16. 2026-06-08 判题环境新增弹窗表单复位

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-007` 的前端阶段修复。目标是避免教师端判题环境“新增配置”弹窗二次打开时残留上一条未提交或已提交配置草稿。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 新增判题环境弹窗 | 每次打开新增弹窗时重置为默认草稿：配置编码、配置名称、语言版本、说明、编译命令、运行命令为空，编程语言为 `Python 3` |
| 编辑判题环境弹窗 | 每次打开编辑弹窗时仍按当前选中配置重置表单，避免复用上一轮编辑或新增草稿 |
| 表单提交载荷 | 本次不改变 `SaveJudgeEnvironmentProfileRequest` 契约和字段映射，只修正弹窗打开时的表单生命周期 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `JudgeEnvironmentProfileDialog` | `react-hook-form` 在 `open=true` 时使用当前 `profile` 对应的默认值执行 `form.reset(defaultValues)` |
| `teacher-judge-environments-page.test.tsx` | 增加回归测试，填入 C++ 草稿并取消后重新打开新增弹窗，断言所有文本字段清空且语言回到 `Python 3` |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 新增弹窗二次打开残留上一条草稿 | 新增 `JudgeEnvironmentsPage resets create draft values when reopening the dialog` 后，修复前失败于 `配置编码` 收到 `cpp-stale` |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/course/teacher-judge-environments-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `5 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `59 passed`，Tests: `155 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测判题环境新增弹窗连续创建 / 取消 / 再打开不残留旧值 |

## 17. 2026-06-08 学生端课程状态文案修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-010` 的前端阶段修复。目标是避免学生端课程卡片直接展示教师 / 管理侧的“草稿”状态，造成“课程看似未开放但已能访问作业”的理解冲突。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 学生课程状态 `DRAFT` | 学生工作台和“我的课表”不再显示“草稿”，改显示“可学习”，表示该课程已经通过学生可见接口进入学习范围 |
| 学生课程状态 `PUBLISHED` | 显示“可学习”，与学生可访问课程 / 作业的操作状态一致 |
| 教师 / 管理侧状态 | 保留原有 `DRAFT -> 草稿` 映射，不改变教师创建、编辑、发布开课的内部状态语义 |
| 后端契约 | 本次不改变 `/api/v1/me/courses` 返回的 `status` 字段，只在学生端视图模型做展示裁剪 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `course-view.ts` | 新增 `mapStudentCourseStatusText` 和 `mapToStudentCourseViewModel`，将学生可见状态与教师 / 管理状态分离 |
| `student/page.tsx` | 学生工作台课程卡片使用学生态状态文案，不再使用本地教师态 `DRAFT -> 草稿` 字典 |
| `student/courses/page.tsx` | 我的课表使用 `mapToStudentCourseViewModel`，与工作台保持一致 |
| `mappers.contract.test.ts` / `student-home-page.test.tsx` / `student-courses-page.test.tsx` | 增加回归测试，覆盖 mapper、学生工作台和我的课表三个入口 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 学生课程卡片暴露教师侧草稿状态 | 新增回归测试后，修复前失败：mapper 缺少 `mapToStudentCourseViewModel`，学生工作台卡片收到 `草稿` 而不是 `可学习` |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/api/mappers.contract.test.ts src/tests/unit/course/student-home-page.test.tsx src/tests/unit/course/student-courses-page.test.tsx` 通过；Test Files: `3 passed`，Tests: `12 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `61 passed`，Tests: `158 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测学生工作台、我的课表和作业列表的状态理解一致性 |

## 18. 2026-06-08 学生课程详情任务入口修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-011` 的前端阶段修复。目标是让学生从课程详情页可以直接进入当前课程 / 教学班的作业和实验，而不是只看到公告、资源和讨论。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 课程详情任务入口 | 课程详情页顶部新增“课程任务”区，提供课程作业、实验项目、课程资源和课程讨论四个稳定入口 |
| 课程作业入口 | 若能从 `/api/v1/me/courses` 找到当前教学班所属开课，则链接到 `/student/assignments?offeringId={offeringId}` |
| 实验项目入口 | 链接到 `/student/labs?classId={classId}`，直接进入当前教学班实验范围 |
| 资源 / 讨论入口 | 使用页内锚点跳转到当前课程详情页的资源和讨论区域 |
| 数据契约 | 本次不新增后端聚合接口，复用现有学生课程、作业、实验列表接口和查询参数 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `student/courses/[classId]/page.tsx` | 新增课程任务入口区，并通过 `useMyCoursesQuery` 将当前 `classId` 解析为 `offeringId` |
| `student/assignments/page.tsx` | 读取 `offeringId` 查询参数并传给 `useMyAssignmentsQuery` |
| `use-my-courses-query.ts` | 我的作业查询 key 纳入查询参数，避免不同课程过滤结果共享缓存 |
| `student/labs/page.tsx` | 读取 `classId` 查询参数，并作为初始教学班实验范围 |
| `student-course-detail-page.test.tsx` / `student-assignments-page.test.tsx` / `student-labs-page.test.tsx` | 增加回归测试，覆盖课程详情入口、作业过滤参数和实验初始教学班参数 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 学生课程详情缺少作业 / 实验入口 | 新增回归测试后，修复前失败于找不到“课程任务”标题；作业页查询参数为 `undefined`；实验页初始查询教学班为默认 `111` 而非 URL 中的 `496` |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/course/student-course-detail-page.test.tsx src/tests/unit/assignment/student-assignments-page.test.tsx src/tests/unit/lab/student-labs-page.test.tsx` 通过；Test Files: `3 passed`，Tests: `5 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `161 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测学生从课程详情进入当前课程作业和当前教学班实验 |

## 19. 2026-06-08 文件上传题附件文件名展示修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-012` 的前端阶段修复。目标是让文件上传题在学生答题页和提交详情题目区域展示原始文件名、大小与下载入口，避免只显示“附件 #id”或“无文本答案”。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 学生答题页上传后 | 文件上传题上传成功后，题目卡片立即显示 `originalFilename` 和文件大小；提交答案仍只提交 `artifactIds` |
| 学生提交详情 | 文件上传题答案卡片按 `answers[].artifactIds` 关联 `artifacts[]`，在题目区域展示文件名、大小和下载按钮，不再显示“无文本答案” |
| 教师提交详情 | 教师批改视图同样在文件上传题答案卡片内展示文件名、大小和下载按钮，保持师生视图口径一致 |
| 数据契约 | 本次不改变后端请求 / 响应契约；复用上传响应中的 `SubmissionArtifactView` 和提交详情中的 `artifacts[]` |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `structured-answer-utils.ts` / `structured-answer-form.tsx` | 答题草稿增加附件元数据；上传和移除附件时同步维护 `artifactIds` 与 `artifacts` |
| `structured-answer-controls.tsx` | 文件上传控件优先显示原始文件名和大小，只有缺少元数据时才兜底显示 `附件 #id` |
| `submission-answer-artifacts.tsx` | 新增提交详情题目内附件展示组件，按题展示文件名、大小和下载入口 |
| 学生 / 教师提交详情页 | 基于提交详情 `artifacts[]` 建索引，并在答案卡片中渲染文件上传题附件 |
| `structured-answer-form.test.tsx` / `student-submission-detail-page.test.tsx` / `teacher-submission-detail-page.test.tsx` | 增加回归测试，覆盖上传后显示文件名、学生提交详情按题显示附件、教师提交详情按题显示附件 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 文件上传题只显示附件编号 / 无文本答案 | 新增回归测试后，修复前失败：上传后找不到 `resource-bl-readme.txt`；学生提交详情文件题卡片收到 `报告附件文件上传10 分无文本答案` |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/structured-answer-form.test.tsx src/tests/unit/submission/student-submission-detail-page.test.tsx src/tests/unit/submission/teacher-submission-detail-page.test.tsx` 通过；Test Files: `3 passed`，Tests: `9 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `163 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测学生真实文件上传、提交后学生 / 教师提交详情均按题显示文件名 |

## 20. 2026-06-08 WebIDE 初始入口文件展示修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-013` 的前端阶段修复。目标是在后端工作区返回 `files=[]` 但提供 `entryFilePath=main.py` 时，文件树与编辑器同时展示入口文件，避免左侧文件浏览器为空。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 工作区 `files` 非空 | 文件树继续使用后端返回的文件列表 |
| 工作区 `files=[]` 且有 `entryFilePath` | 前端生成一个展示用入口文件，路径为 `entryFilePath`，内容使用 `codeText` 或空字符串 |
| 编辑器与文件树一致性 | `activeFilePath`、打开标签、文件树和状态栏都以同一入口文件为准 |
| 保存请求 | 保存时仍通过 `mergeWorkspaceFileContent` 生成包含当前入口文件内容的 `files`，不会只停留在展示层 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `workspace-files.ts` | 新增 `getWorkspaceDisplayFiles(workspace)`，集中处理入口文件兜底 |
| `use-workspace-file-session.ts` | 文件树和状态栏文件计数改用展示文件列表，保持与编辑器入口一致 |
| `workspace-files.test.ts` / `programming-workspace-page.test.tsx` | 增加回归测试，覆盖 helper 和页面文件浏览器在 `files=[]` 时显示 `main.py` |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: WebIDE 文件树缺少入口文件 | 新增回归测试后，修复前失败于 `getWorkspaceDisplayFiles is not a function`；页面层在 `files=[]` 时无法从文件浏览器找到 `main.py` |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/workspace-files.test.ts src/tests/unit/submission/programming-workspace-page.test.tsx` 通过；Test Files: `2 passed`，Tests: `10 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `165 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测学生首次进入 WebIDE 时文件树、标签和编辑器均显示入口文件 |

## 21. 2026-06-08 WebIDE Monaco 保存值一致性复核

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-014` 的当前树复核。目标是证明 WebIDE 保存、样例运行和“保存并返回”不依赖 React `onChange` 的异步交付，而是读取 Monaco model 当前值，避免可见代码与保存请求不一致时持久化空代码。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| Monaco model 变化 | 编辑器 `onMount` 后订阅 `onDidChangeModelContent`，直接用 `editor.getValue()` 同步当前活动文件内容 |
| 手动保存 | 点击“保存”时优先读取 `editorRef.current.getValue()`，并将该值写入 `codeText` 与当前文件内容 |
| 样例运行 | 点击“运行”时同样读取 Monaco 当前值，样例请求的 `codeText` 与 `files[]` 使用同一份内容 |
| 保存并返回 | IDE 内“保存并返回”只保存当前编程题工作区，并返回作业详情页，不调用整份作业提交接口 |

### 复核范围

| 模块 | 复核结果 |
| --- | --- |
| `ProgrammingWorkspacePage` | `getCurrentEditorContent()` 优先从 Monaco editor 实例读取当前 model 值；保存、运行和确认保存均传入该值 |
| `useProgrammingWorkspaceController` | `handleSave` / `handleRun` / `handleSubmit` 在传入内容与本地活动文件内容不一致时先同步本地状态，再构造请求 payload |
| `programming-workspace-page.test.tsx` | 已有回归测试覆盖 React `onChange` 不交付时，保存仍使用编辑器 model 当前值 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `6 passed` |
| 关键断言 | `saves the current Monaco model content even when React onChange is not delivered` 断言保存 payload 的 `codeText` 和 `files[0].content` 均为编辑器当前内容 `print(42)\n` |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段完成当前树代码路径和单测复核；仍需在最终业务闭环中用 Playwright MCP 通过真实键盘输入、点击保存并核验请求 payload 与 Monaco model 一致 |

## 22. 2026-06-08 WebIDE 单文件题文件创建入口收敛

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-016` 的前端阶段修复。目标是在编程题禁用多文件时，不再向学生暴露新建文件 / 新建目录入口，并在 hook 层阻止误触路径产生本地乐观文件，避免后端返回 `PROGRAMMING_MULTIPLE_FILES_DISABLED` 后 UI 与服务端状态发散。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| `allowMultipleFiles=false` 或缺省 | 文件浏览器不展示根目录“创建文件或目录”按钮；目录项菜单也不展示“新建文件 / 新建目录” |
| `allowMultipleFiles=true` | 文件浏览器继续展示创建入口，支持多文件题创建文件和目录 |
| 误触保护 | `useWorkspaceFileSession` 在 `canCreateFiles=false` 时直接忽略创建文件 / 目录操作，不调用后端 operations，也不写入本地乐观状态 |
| 可访问性 | 文件创建和单文件操作图标按钮补充可访问名称，避免真实浏览器审计只能看到匿名按钮 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `useProgrammingWorkspaceController` | 根据题目配置 `question.config.allowMultipleFiles` 计算 `canCreateFiles`，传入文件会话和页面组件 |
| `useWorkspaceFileSession` | 新增 `canCreateFiles` guard，禁止单文件题通过 handler 创建本地文件或目录 |
| `WorkspaceLeftPanel` / `FileTree` / `FileTreeItem` | 将 `canCreateFiles` 透传到文件树；单文件题隐藏根目录和目录内创建入口；图标按钮补充 `aria-label` |
| `programming-workspace-page.test.tsx` | 增加回归测试，覆盖单文件题隐藏创建入口、多文件题保留创建入口 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 单文件题仍暴露文件创建入口 | 新增回归测试后，修复前失败：无法按可访问名称找到“创建文件或目录”，且角色列表仍出现匿名文件操作按钮 |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `8 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `167 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 后端拒绝 | 后端现有 `PROGRAMMING_MULTIPLE_FILES_DISABLED` 仍作为最终保护；前端本轮阻断常规 UI 入口和本地乐观状态发散 |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测单文件题文件浏览器没有创建入口、多文件题创建入口可用 |

## 23. 2026-06-08 WebIDE 历史版本侧栏布局修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-017` 的前端阶段修复。目标是让历史版本侧栏在桌面工作区中保持稳定宽度，不被 Monaco 编辑区挤压到约 98px，同时保留可滚动内容和清楚的恢复操作。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 桌面布局 | 历史版本侧栏使用 `shrink-0`、`lg:w-80`、`lg:min-w-80`，在主编辑区旁保持稳定宽度 |
| 移动 / 窄屏布局 | 侧栏在纵向布局中使用全宽和 `max-h-[420px]`，避免覆盖编辑器或无限撑高页面 |
| 可滚动内容 | 版本列表和预览区域继续使用 `flex-1 overflow-y-auto`，长历史列表可滚动 |
| 可访问性 | 侧栏使用 `role="complementary"` 和 `aria-label="历史版本"`，便于浏览器审计和辅助技术定位 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `workspace-revision-sidebar.tsx` | 根容器从普通 `div` 改为语义化 `aside`，补稳定宽度、禁止收缩、移动端最大高度和边框方向 |
| `programming-workspace-page.test.tsx` | 增加回归测试，覆盖历史侧栏可定位、具备稳定宽度类并仍展示标题 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 历史侧栏缺少稳定布局 landmark | 新增回归测试后，修复前失败于无法找到 `role="complementary"` 且名称为“历史版本”的侧栏 |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `9 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `168 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测学生打开历史版本侧栏时宽度稳定、列表可滚动、恢复按钮可见 |

## 24. 2026-06-08 WebIDE 保存本题返回语义复核

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-018` 的当前树复核。目标是确认 IDE 内操作不再调用整份结构化作业提交接口，避免只发送编程题答案导致 `SUBMISSION_ANSWER_SET_INVALID`，并让 UI 文案明确整份作业提交只能回到作业详情页完成。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 工具栏主按钮 | 原 IDE 内“提交”改为“保存并返回” |
| 确认弹窗 | 标题为“保存本题”，说明“保存当前编程题代码并返回作业详情页；整份作业提交请在作业详情页完成。” |
| 请求语义 | 确认后调用编程工作区保存 mutation，revision message 为“保存本题后返回作业”，不调用 `POST /submissions` 整份作业提交接口 |
| 成功跳转 | 保存成功后返回 `/student/assignments/{assignmentId}`，由作业详情页负责整份作业提交 |

### 复核范围

| 模块 | 复核结果 |
| --- | --- |
| `useProgrammingWorkspaceController` | 当前生产代码不再引入或调用 `useCreateSubmissionMutation`；`handleSubmit` 使用 `saveMutation.mutate(buildSavePayload(...))` |
| `ProgrammingWorkspacePage` | 工具栏 `submitLabel="保存并返回"`；确认弹窗标题、描述和按钮文案均为保存当前题后返回 |
| `programming-workspace-page.test.tsx` | 回归测试断言 `createSubmissionMutate` 未被调用，保存 payload 包含当前代码和“保存本题后返回作业”，成功回调跳转作业详情页 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `9 passed` |
| 关键断言 | `saves the current programming question and returns to assignment detail instead of submitting the whole assignment` 断言整份作业提交 mutation 未调用，保存成功后跳转 `/student/assignments/439` |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段完成当前树代码路径和单测复核；仍需在最终业务闭环中用 Playwright MCP 复测 IDE 内点击“保存并返回”只发工作区保存请求，并返回作业详情页后再完成整份作业提交 |

## 25. 2026-06-08 编程判题得分同步复核

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-019` 的当前树复核。目标是确认结构化编程题评测完成后，提交详情分题得分、提交总分、待判题计数和成绩册聚合使用同一份 `submission_answers` 得分状态，不再出现 judge job 已 `ACCEPTED 20/20` 但提交详情仍为 `20/60`、编程题显示 `0` 分的情况。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 提交详情分题 | 编程题进入 `PROGRAMMING_JUDGED` 或 `PROGRAMMING_JUDGE_FAILED` 终态后，即使人工分未发布，也会展示自动评测写回的 `autoScore`、`finalScore` 和反馈 |
| 提交总分 | `scoreSummary` 在隐藏人工分时仍包含客观题即时分和已完成编程评测自动分 |
| 待处理计数 | 编程题评测完成后 `pendingProgrammingCount=0`；人工题仍保留 `pendingManualCount` |
| 学生成绩可见性 | 发布前仍隐藏非客观题人工评分和人工反馈；编程自动评测分作为即时反馈可见 |

### 复核范围

| 模块 | 复核结果 |
| --- | --- |
| `SubmissionAnswerApplicationService` | `shouldRevealAnswerResult` 允许客观题和终态编程评测结果在 `revealNonObjectiveScores=false` 时进入答案视图和分数摘要 |
| `StructuredProgrammingJudgeIntegrationTests` | 混合题集成测试覆盖客观题 20 分、编程题判题完成 20 分、人工题待批改，提交详情刷新后总分为 40 分 |
| `SubmissionAnswerApplicationServiceTests` | 单元测试覆盖未发布人工分时终态编程评测结果仍展示，且分数摘要包含客观题 + 编程题自动分 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| 后端目标单测 | `cd server && bash ./mvnw -Dtest=SubmissionAnswerApplicationServiceTests test` 通过；Tests run: `4`，Failures: `0`，Errors: `0` |
| 后端目标集成测试 | `cd server && bash ./mvnw -Dtest=StructuredProgrammingJudgeIntegrationTests test` 通过；Tests run: `13`，Failures: `0`，Errors: `0` |
| 关键断言 | 混合题提交初始 `scoreSummary.finalScore=20`、`pendingProgrammingCount=1`；判题完成后学生提交详情 `answers[1].finalScore=20`、`scoreSummary.autoScoredScore=40`、`scoreSummary.finalScore=40`、`pendingProgrammingCount=0`、`pendingManualCount=1` |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段完成后端当前树单元 / 集成复核；仍需在最终业务闭环中用 Playwright MCP 复测学生正式提交后等待判题完成并刷新提交详情，确认页面显示的题目分和总分同步 |

## 26. 2026-06-08 提交详情按题型展示修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-020` 的前端阶段修复。目标是让学生和教师 / 助教提交详情按题型展示答案，不再把客观题、文件题和编程题统一退化为“无文本答案”，并让编程题代码以保留换行的代码块展示。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 单选 / 多选 | 题目卡片展示“已选选项”和选项 key 列表，如 `A`、`A, B` |
| 文件上传题 | 题目卡片继续展示原始文件名、大小和下载入口；正文区域显示“附件见本题文件列表”，不再显示“无文本答案” |
| 编程题 | 题目卡片展示语言、入口文件和源码代码块；代码块使用 `whitespace-pre` 保留换行 |
| 简答 / 填空 | 继续按文本答案展示，并保留原有换行 |
| 视图一致性 | 学生提交详情和教师 / 助教提交详情共用同一个答案正文组件，避免展示口径分叉 |

### 修复范围

| 模块 | 修复 |
| --- | --- |
| `submission-answer-body.tsx` | 新增按题型渲染的答案正文组件，覆盖客观题、文件题、编程题和文本题 |
| 学生提交详情页 | 用 `SubmissionAnswerBody` 替换统一 `answerText || "无文本答案"` fallback，附件组件继续按题显示 |
| 教师提交详情页 | 同步使用 `SubmissionAnswerBody`，保留批改和重判控件 |
| `student-submission-detail-page.test.tsx` / `teacher-submission-detail-page.test.tsx` | 增加回归测试，覆盖客观题选项、文件题附件、编程题语言 / 入口文件 / 代码块换行展示 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 提交详情统一退化为无文本答案 | 新增回归测试后，修复前学生卡片收到 `单选题单选题10 分无文本答案`；教师卡片收到 `单选题单选题无文本答案...`，缺少“已选选项” |
| 目标前端单测 | `cd web && npm test -- src/tests/unit/submission/student-submission-detail-page.test.tsx src/tests/unit/submission/teacher-submission-detail-page.test.tsx` 通过；Test Files: `2 passed`，Tests: `8 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `170 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段先完成前端 TDD 和静态 / 单元 / 构建门禁；仍需在最终业务闭环中用 Playwright MCP 复测学生、教师和整课助教提交详情的客观题、文件题、编程题展示 |

## 27. 2026-06-08 整课助教成绩操作权限与 403 反馈修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-021` 的当前树补强。目标是确认整课助教在开课范围内不再遇到重判、成绩册导出、批量调分和发布成绩 403，同时保留班级助教不能发布整课成绩的负例，并补齐成绩册导出失败时的可见前端反馈。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 整课助教权限 | `OFFERING_TA` 在本开课范围内可执行教师侧重判、成绩册导出、批量调分、成绩发布 / 重新发布等操作 |
| 班级助教边界 | `TA` 仍只能在授权教学班内查看 / 批改，不可发布整课成绩，不可越权到整课成绩导出或成员操作 |
| 前端错误反馈 | 成绩册导出这类非 mutation 下载请求失败时，页面通过 toast 展示后端错误消息，例如“当前用户无权导出成绩册” |
| 审计 | 成绩册导出记录 `GRADE_EXPORT` allow / deny；成绩发布同时记录业务发布日志 `ASSIGNMENT_GRADES_PUBLISHED` 和敏感授权日志 `GRADE_PUBLISH` allow / deny |

### 修复范围

| 模块 | 修复 / 补强 |
| --- | --- |
| `GradingIntegrationTests` | 新增接口级回归：整课助教导出成绩册、批量调分、发布成绩均为 2xx；班级助教发布整课成绩为 403；断言导出和发布审计 |
| `teacher/grading/gradebook/page.tsx` | `handleExport` 改为 `async`，捕获 `downloadOfferingGradebook` 异常并通过 `normalizeApiError` + `toast.error` 展示 |
| `teacher-gradebook-page.test.tsx` | 新增 RED/GREEN 测试，修复前 `toast.error` 调用次数为 0；修复后导出失败展示后端错误 |
| `authenticated-shell.test.tsx` | 补显式 `cleanup()`，避免并发全量单测中 React 调度在 jsdom teardown 后触发 `window is not defined` 未处理异常 |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 导出失败无反馈 | 新增前端测试后，修复前 `toast.error` 调用次数为 `0`，复现旧报告中导出 403 无 UI 反馈残口 |
| 前端目标单测 | `cd web && npm test -- src/tests/unit/grading/teacher-gradebook-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `4 passed` |
| 后端目标集成测试 | `cd server && bash ./mvnw -Dtest=GradingIntegrationTests#offeringTaCanExportBatchAdjustAndPublishGradesWhileClassTaCannotPublishOfferingGrades test` 通过；Tests run: `1`，Failures: `0`，Errors: `0` |
| 后端权限组合回归 | `cd server && bash ./mvnw -Dtest=CourseSystemIntegrationTests#offeringTaShouldHaveTeacherSidePermissionsAndClassTaShouldStayScoped,JudgeIntegrationTests#offeringTaCanRequeueJudgeWithTeacherSidePermissionsAndAllowedAuditShouldBeRecorded,GradingIntegrationTests#offeringTaCanExportBatchAdjustAndPublishGradesWhileClassTaCannotPublishOfferingGrades test` 通过；Tests run: `3`，Failures: `0`，Errors: `0` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `171 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段完成接口级和前端单元 / 构建证据；仍需在最终业务闭环中用 Playwright MCP 以整课助教身份实际点击提交详情重判、成绩册导出、批量调分、发布 / 重新发布，并确认页面反馈 |

## 28. 2026-06-08 开课主讲教师候选加载失败修复

本段记录 `business-loop-playwright-mcp-report-2026-06-07.md` 中 `BUG-20260607-001` 的当前树修复与复核。目标是解除管理员新增开课时 `GET /api/v1/admin/users?identityType=TEACHER&pageSize=100` 因教师用户缺少 `primaryOrgUnitId` 返回 500 的阻塞，并让前端在教师候选接口失败时显示可重试失败态，而不是伪装成“暂无选项”。

### 行为口径

| 项目 | 新行为 |
| --- | --- |
| 后端教师候选查询 | 教师用户存在教师身份但 `primaryOrgUnitId=null` 时，管理员用户列表查询不再触发 NPE；教师候选仍可返回给开课创建页 |
| 前端失败态 | 主讲教师候选接口失败时，新增开课弹窗展示“主讲教师候选加载失败”并提供“重试加载主讲教师候选”按钮 |
| 前端空态 | 接口成功但候选为空时展示“暂无教师候选”，不再使用会掩盖接口失败的通用“暂无可选项” |

### 修复范围

| 模块 | 修复 / 补强 |
| --- | --- |
| `UserAdministrationApplicationService` | 已在当前树兼容 `primaryOrgUnitId=null` 的教师用户候选查询，避免构建组织信息时触发 NPE |
| `PlatformGovernanceApiIntegrationTests` | 覆盖无主组织教师候选查询返回 200 的回归场景 |
| `admin/course-offerings/page.tsx` | 将 `useUsersQuery` 的 `isLoading`、`error`、`refetch` 传入新增开课弹窗 |
| `course-offering-create-dialog.tsx` | 主讲教师候选接口失败时展示 `role="alert"` 的可见失败态与重试按钮；加载与空候选使用专用文案 |
| `course-offerings-page.test.tsx` | 增加失败态回归测试，断言旧的“暂无可选项”不再出现，点击重试会调用 `refetch` |

### 验证证据

| 验证项 | 结果 |
| --- | --- |
| RED: 教师候选接口失败被显示为空态 | 新增前端测试后，修复前无法找到“主讲教师候选加载失败”，弹窗仍退化为通用空态 |
| 后端目标集成测试 | `cd server && bash ./mvnw -Dtest=PlatformGovernanceApiIntegrationTests#listsTeacherCandidatesWhenPrimaryOrganizationIsMissing test` 通过；Tests run: `1`，Failures: `0`，Errors: `0` |
| 前端目标单测 | `cd web && npm test -- src/tests/unit/admin/course-offerings-page.test.tsx` 通过；Test Files: `1 passed`，Tests: `5 passed` |
| 前端静态门禁 | `cd web && npm run lint`、`cd web && npm run typecheck` 均通过 |
| 前端全量单测 | `cd web && npm test` 通过；Test Files: `62 passed`，Tests: `172 passed` |
| 前端生产构建 | `cd web && npm run build` 通过；Next.js 编译、TypeScript 和 `30/30` 静态页面生成完成 |

### 残余说明

| 项目 | 当前结果 |
| --- | --- |
| 真实浏览器证据 | 本阶段完成后端集成测试和前端单元 / 构建证据；仍需在最终业务闭环中用 Playwright MCP 以管理员身份打开新增开课弹窗，确认教师候选可加载，且通过拦截或后端错误场景确认失败态可见并可重试 |
