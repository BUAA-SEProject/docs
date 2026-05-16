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
| 前端静态验证 | 已完成 | 已完成 lint、typecheck、unit test、build 基线；本轮真实后端 Playwright E2E `17/17` 通过 |
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
| 真实 Playwright | `AUBB_E2E_REAL_BACKEND=1 npm run test:e2e` | `17` 个 Chromium 用例全部通过 |
| 浏览器点验 | Playwright MCP 打开 `http://127.0.0.1:3000` | 登录失败/成功/退出、管理员导航与搜索、教师课程公告、学生作业/成绩、未授权跳转已验证 |

## 4. 关键修复清单

| 文件 / 模块 | 问题 | 修复方式 | 验证 |
| --- | --- | --- | --- |
| `server/scripts/api-tests/permission/e2e_permission_realrun.py` | 后端在课程任课/成员权限变更后会撤销受影响用户旧会话，脚本继续复用旧 `U-TA1` token 导致真实 API 脚本在成员列表接口收到 `401` | fixture 收尾刷新受课程权限授予影响的教师、助教、学生账号 token | `e2e_permission_realrun_test.py` 通过；真实权限 API `22/22` 通过 |
| `web/src/app/(teacher)/teacher/courses/[offeringId]/announcements/page.tsx` | 教师公告空标题/正文点击“发布”会静默无反馈 | 改为真实 `<form>`，标题和正文添加 `required` 与可访问标签，编辑弹窗同样走 submit 校验 | 新增 Playwright 用例；真实 E2E `17/17` 通过；浏览器点验返回原生必填提示 |
| `web/src/app/(admin)/admin/users/page.tsx`、`web/src/shared/ui/file-upload-field.tsx` | 用户管理顶部“批量导入”按钮没有触发隐藏文件选择器 | `FileUploadField` 增加 `triggerRef`，用户页顶部按钮通过 ref 打开 CSV 文件选择器 | `file-upload-field.test.tsx` 通过；真实 filechooser E2E 通过；完整真实 E2E `17/17` 通过 |
| `web/src/shared/api/download/index.ts`、`web/src/tests/unit/api/download.contract.test.ts` | 下载按钮只通过 API 拉取 blob，没有创建浏览器下载 | `downloadBinary` 解析文件名、创建 object URL、点击隐藏 anchor 并释放 URL，同时返回 blob 元数据 | 新增单测 1/1 通过；完整前端单元测试 11 个文件 / 24 个测试通过 |
| `web/src/app/(teacher)/teacher/courses/[offeringId]/resources/page.tsx`、`web/src/tests/e2e/teacher-course.spec.ts` | 课程资源 E2E 首次失败，后端未启用对象存储时上传 API 返回 `COURSE_RESOURCE_STORAGE_DISABLED`；资源标题字段也缺少稳定 label 关联 | 补资源页 label/id；E2E 等待上传 POST 并断言响应 OK；后端联调启动启用本地 MinIO | 资源上传、改名、下载、删除目标 E2E 1/1 通过；完整真实 E2E `17/17` 通过 |
| `web/src/tests/e2e/auth.spec.ts` | 退出登录菜单项真实 role 为 `menuitem`，测试按 `button` 查询导致误报失败 | 改用 `getByRole("menuitem", { name: "退出登录" })` | 单用例通过；完整真实 E2E 通过 |
| `web/src/shared/api/generated/openapi.ts` | 前端生成类型落后于运行时后端契约 | 从真实后端 `/v3/api-docs` 重新生成 | 生成命令通过；后续 typecheck/build 覆盖 |
| `web/src/app/(student)/student/assignments/page.tsx`、`web/src/app/(student)/student/courses/[classId]/page.tsx`、`web/src/app/(student)/student/labs/page.tsx` | 运行时 OpenAPI 中 `MyCourseClassView` 不包含 `features`，学生端仍读取不存在字段导致 typecheck 失败 | 去除学生端对不存在 `features` 字段的依赖，入口按当前 `/me/courses` 合约默认可见，内容与权限仍由后端接口控制 | `npm run typecheck`、`npm run build`、真实 E2E `17/17` 通过 |
| `server/src/test/java/com/aubb/server/integration/AuthzOpenApiAccessRegistry.java` | OpenAPI 权限登记表仍包含已删除成绩申诉 / 发布批次路径，且缺少部分 PUT/DELETE 路径 | 移除旧路径，补齐学期、课程、公告、资源等当前路径权限映射 | 后端全量测试基线通过 |
| `server/src/test/java/com/aubb/server/integration/*IntegrationTests.java` | 固定 2026 时间窗和旧申诉通知导致测试漂移 | 改为动态时间窗，旧申诉通知改为当前实验报告通知 | 后端全量测试基线通过 |
| `web/src/shared/ui/layout/topbar.tsx` | 顶栏全局搜索输入可输入但缺少有效跳转 | 新增全局搜索路由匹配，Enter 跳到首个可访问目标 | 前端单元测试和真实浏览器点验通过 |
| `web/docs/backend/**`、`server/docs/**`、`docs/**` | 多处把 V48 已删除能力写成当前能力 | 更新 API、数据模型、权限、产品规格和顶层文档 | 残留扫描仅剩“V48 已删除/不再提供”的说明性命中 |

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
