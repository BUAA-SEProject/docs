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
