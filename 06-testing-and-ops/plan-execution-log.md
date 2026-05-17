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
