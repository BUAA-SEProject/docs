# 全栈功能、文档与联调审查报告

更新日期：2026-05-16

## 1. 审查范围

| 范围 | 核验对象 | 结论 |
| --- | --- | --- |
| 根目录 | `/Users/moorefoss/Code/AUBB`、`plan.md`、`CLAUDE.md` | 根目录不是 Git 仓库，作为 `server/`、`web/`、`docs/` 三个子仓库的工作区 |
| 后端 | `server/pom.xml`、`server/compose.yaml`、`server/src/main`、`server/src/test`、`server/src/main/resources/db/migration`、`server/docs`、`server/scripts/api-tests` | Spring Boot 4 / Java 25 / Maven；依赖 PostgreSQL、RabbitMQ、MinIO、Redis、go-judge；本地真实联调已启动验证 |
| 前端 | `web/package.json`、`web/next.config.ts`、`web/src/app`、`web/src/features`、`web/src/shared`、`web/src/tests`、`web/docs` | Next.js 16 / React 19 / TypeScript；前端通过 `AUBB_SERVER_ORIGIN` rewrite 连接真实后端 |
| 文档 | `docs/**`、`server/docs/**`、`web/docs/**`、各 README | 已同步 V48 成绩域简化事实，并补充真实启动、OpenAPI、E2E 和按钮级验证报告 |

## 2. 项目事实基线

| 项目 | 实际结论 | 依据文件 / 命令 |
| --- | --- | --- |
| 仓库结构 | `server/`、`web/`、`docs/` 各自是 Git 仓库，根目录不是 Git 仓库 | `find . -maxdepth 2 -type d -name .git` |
| 后端技术栈 | Spring Boot 4.0.5、Java 25、Maven wrapper、Flyway、MyBatis-Plus、PostgreSQL、RabbitMQ、MinIO、Redis、go-judge | `server/pom.xml`、`server/compose.yaml` |
| 前端技术栈 | Next.js 16.2.4、React 19.2.4、TypeScript、Tailwind/shadcn、Vitest、Playwright | `web/package.json`、`web/playwright.config.ts` |
| 文档站 | VitePress 文档站，侧边栏已包含本轮三份交付报告 | `docs/package.json`、`docs/SUMMARY.md`、`docs/06-testing-and-ops/index.md` |
| 前后端代理 | 前端 rewrite `/api/v1/*`、`/v3/api-docs`、`/swagger-ui/*` 到 `AUBB_SERVER_ORIGIN` | `web/next.config.ts` |
| 运行时契约 | 本地后端 `GET /v3/api-docs` 返回 OpenAPI `3.1.0`、`124` 个 path；启用本地 MinIO 后 readiness 包含 `minioStorage=UP` | `curl http://127.0.0.1:18080/v3/api-docs`、`curl http://127.0.0.1:18080/actuator/health/readiness` |
| 服务收尾 | 本轮验证结束后已停止前端、后端和 compose 容器，未删除数据卷 | `curl 127.0.0.1:3000/login`、`curl 127.0.0.1:18080/actuator/health/readiness` 返回不可连接；`docker compose ps` 为空 |

## 3. 前端功能清单

| 路由 / 区域 | 页面文件 | 页面用途 | 角色/权限 | 主要 API 调用 | 审查状态 |
| --- | --- | --- | --- | --- | --- |
| `/login` | `web/src/app/(auth)/login/page.tsx` | 登录入口、登录失败反馈 | 未登录 | `POST /api/v1/auth/login` | 已实现，真实登录成功/失败已验证 |
| `/admin` | `web/src/app/(admin)/admin/page.tsx` | 管理端工作台 | 管理员 | `GET /api/v1/auth/me` 等 | 已实现，真实 E2E 覆盖 |
| `/admin/platform-config` | `web/src/app/(admin)/admin/platform-config/page.tsx` | 平台配置查看/保存 | 管理员 | 平台配置 API | 已实现，必填校验已浏览器点验 |
| `/admin/users`、`/admin/academic-terms`、`/admin/course-catalogs`、`/admin/course-offerings` | `web/src/app/(admin)/admin/**` | 用户、学期、课程模板、开课治理 | 管理员 | 管理端治理 API | 页面可达，真实 E2E 覆盖页面 shell、导航和用户批量导入文件选择器 |
| `/teacher`、`/teacher/courses`、`/teacher/courses/[offeringId]` | `web/src/app/(teacher)/teacher/**` | 教师工作台、课程、成员和内容管理 | 教师 | 教师课程、成员、内容 API | 页面可达，真实 E2E 覆盖 |
| `/teacher/courses/[offeringId]/announcements` | `web/src/app/(teacher)/teacher/courses/[offeringId]/announcements/page.tsx` | 课程公告创建/编辑/删除 | 教师 | 教师公告 API | 已修复空提交静默问题并纳入 E2E |
| `/teacher/courses/[offeringId]/resources` | `web/src/app/(teacher)/teacher/courses/[offeringId]/resources/page.tsx` | 课程资源上传、改名、下载、删除 | 教师 | 教师资源 API、MinIO 对象存储 | 已补可访问标签，真实 E2E 覆盖上传、改名、下载和删除 |
| `/teacher/assignments`、`/teacher/submissions`、`/teacher/grading/gradebook`、`/teacher/labs` | `web/src/app/(teacher)/teacher/**` | 作业、提交、成绩册、实验管理 | 教师 | 作业、提交、成绩、实验 API | 页面可达，非破坏性路径已 E2E 覆盖 |
| `/student`、`/student/courses`、`/student/courses/[classId]` | `web/src/app/(student)/student/**` | 学生学习中心和课程主页 | 学生 | `GET /api/v1/me/courses`、课程内容 API | 已适配 `MyCourseClassView` 当前契约 |
| `/student/assignments`、`/student/assignments/[assignmentId]` | `web/src/app/(student)/student/assignments/**` | 学生作业列表、详情、提交入口 | 学生 | 学生作业和提交 API | 真实种子作业页面已验证 |
| `/student/labs`、`/student/grades`、`/student/notifications` | `web/src/app/(student)/student/**` | 实验、成绩、通知 | 学生 | 实验、成绩、通知 API | 页面可达，真实 E2E 覆盖 |
| 全局导航 / 顶栏 | `web/src/shared/ui/layout/topbar.tsx`、`web/src/shared/routing/global-search.ts` | 角色导航、搜索、用户菜单 | 登录用户 | 当前用户、通知 API | 已修复搜索无行为问题 |

## 4. 后端 API 清单

| API 组 | Controller / Handler | Service / 依赖 | 认证/权限 | 测试覆盖 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 认证与当前用户 | `server/src/main/java/com/aubb/server/modules/identityaccess/api` | 认证、会话、用户服务 | 登录、刷新、当前用户 | 集成测试、真实登录探针 | 已实现 |
| 管理治理 | `server/src/main/java/com/aubb/server/modules/*/api` 中 admin 相关 Controller | 用户、组织、学期、课程治理服务 | 管理员权限和服务层授权 | OpenAPI 权限注册表、集成测试 | 已实现 |
| 教师课程内容 | `CourseAnnouncementTeacherController`、`CourseResourceTeacherController`、讨论、题库、评测环境 Controller | 课程授权、内容、资源、讨论服务 | 教师/助教课程权限 | 集成测试、真实 E2E 页面覆盖 | 已实现，公告校验已补强 |
| 学生学习内容 | `MyCoursesController`、`MyCourseAnnouncementController`、资源、讨论 Controller | `CourseTeachingApplicationService`、内容服务 | 学生本人课程成员关系 | 运行时 OpenAPI、真实 E2E | 已实现，前端已按当前 DTO 适配 |
| 作业与提交 | assignment、submission、judge 相关 Controller | 作业、提交、go-judge、MinIO | 教师/学生角色和资源归属 | 集成测试、真实页面 smoke | 已实现 |
| 成绩与实验 | grading、lab 相关 Controller | 成绩册、实验报告服务 | 教师/学生权限和资源归属 | Maven 测试、页面 smoke | 已按 V48 简化后契约同步 |
| 权限脚本 | `server/scripts/api-tests/permission/run_permission_e2e.sh` | 真实 HTTP API、测试夹具 | 本地测试账号 | `22/22` 真实权限场景 | 已修复会话刷新问题 |

## 5. 文档覆盖情况

| 文档路径 | 主题 | 对应代码模块 | 是否过时 | 处理结果 |
| --- | --- | --- | --- | --- |
| `docs/04-development/*` | 架构、后端、数据库概览 | `server/`、`web/` | 有 V48 前旧描述 | 已同步摘要 |
| `docs/05-api/*` | API 总览、成绩 API | 后端 OpenAPI / Controller | 有成绩快照、申诉旧描述 | 已更新为当前能力 |
| `docs/06-testing-and-ops/*` | 测试、验收、联调报告 | 三仓库验证结果 | 缺少本轮真实证据 | 已新增三份报告并加入导航 |
| `server/docs/product-specs/*` | 服务端产品规格 | 后端模块和迁移 | 多处 V48 前能力 | 已修正 |
| `server/docs/generated/db-schema.md` | 数据库 Schema | Flyway 迁移 | 含已删除表字段 | 已修正 |
| `web/docs/backend/**` | 前端侧后端对接文档 | `web/src/features`、后端 API | 旧权限/成绩描述 | 已修正 |

## 6. 文档与实现差异

| 编号 | 类型 | 文档路径 | 代码依据 | 差异描述 | 处理方式 |
| --- | --- | --- | --- | --- | --- |
| D-01 | 文档过时 | `server/docs/product-specs/grading-system.md`、`web/docs/backend/api/teacher-grading-lab.md` | `server/src/main/resources/db/migration/V48__simplify_gradebook_remove_weight_snapshots_appeals.sql` | 仍把成绩申诉、成绩发布快照、assignment 级权重写成当前能力 | 改为 V48 简化后的当前能力和已删除说明 |
| D-02 | 数据模型不一致 | `server/docs/generated/db-schema.md` | Flyway V48、grading 相关 Java 类 | Schema 文档包含已移除表/字段 | 更新 Schema 文档 |
| D-03 | 权限描述不一致 | `web/docs/backend/05-auth-and-authorization.md`、`auth-permission-catalog.md` | 当前 Controller、`AuthzOpenApiAccessRegistry` | 文档描述不存在的旧权限入口 | 改为当前认证、服务层权限和 OpenAPI 注册表覆盖模型 |
| D-04 | 测试文档缺失 | `docs/06-testing-and-ops/*` | 本轮真实联调和 E2E 输出 | 缺少真实启动、权限脚本、按钮级 E2E 证据 | 新增执行记录、审计报告、按钮级报告 |

## 7. 前端问题清单

| 编号 | 分类 | 严重级别 | 文件路径 | 组件/函数 | 问题描述 | 修复状态 |
| --- | --- | --- | --- | --- | --- | --- |
| FE-01 | 无实际反馈 UI | P1 | `web/src/app/(teacher)/teacher/courses/[offeringId]/announcements/page.tsx` | 公告创建/编辑表单 | 空标题或正文点击发布静默 return，无用户反馈 | 已修复，`required` 表单校验并纳入 E2E |
| FE-02 | 测试与真实 UI role 不一致 | P2 | `web/src/tests/e2e/auth.spec.ts` | 退出登录 | 测试按 button 查找 Radix menuitem，导致误报 | 已修复 |
| FE-03 | 接口类型不一致 | P1 | `web/src/app/(student)/student/assignments/page.tsx`、`courses/[classId]/page.tsx`、`labs/page.tsx` | 学生班级功能开关 | 运行时 `MyCourseClassView` 不含 `features`，OpenAPI 刷新后 typecheck 失败 | 已修复，入口按当前 `/me/courses` DTO 默认可见 |
| FE-04 | 假功能风险 | P2 | `web/src/shared/ui/layout/topbar.tsx` | 全局搜索 | 输入框可输入但 Enter 不导航 | 已修复，新增搜索匹配和单元测试 |
| FE-05 | 静态检查阻断 | P2 | `web/src/app/(admin)/admin/academic-terms/page.tsx`、学生 workspace、paper editor | lint/typecheck | 未使用导入、hook 依赖、文案转义等静态问题 | 已修复 |
| FE-06 | 假按钮 | P2 | `web/src/app/(admin)/admin/users/page.tsx`、`web/src/shared/ui/file-upload-field.tsx` | 用户批量导入 | 顶部“批量导入”按钮没有触发隐藏文件选择器，页面下方虽有真实上传控件但顶部按钮无实际动作 | 已修复，`FileUploadField.triggerRef` 暴露选择器触发函数，并用单元测试和真实 filechooser E2E 覆盖 |
| FE-07 | 假下载风险 | P1 | `web/src/shared/api/download/index.ts` | `downloadBinary` | 下载按钮只拉取 blob，不创建浏览器下载，用户点击后不会得到文件 | 已修复，创建 object URL、隐藏 `<a>` 触发下载并释放 URL，新增单元测试 |
| FE-08 | 可访问性 / E2E 可测性 | P2 | `web/src/app/(teacher)/teacher/courses/[offeringId]/resources/page.tsx` | 课程资源上传和编辑弹窗 | 资源标题输入框缺少稳定 label 关联，真实 E2E 无法按 label 操作 | 已修复，上传和编辑字段补 `htmlFor` / `id` |

## 8. 后端问题清单

| 编号 | 分类 | 严重级别 | 文件路径 | 类/方法/API | 问题描述 | 修复状态 |
| --- | --- | --- | --- | --- | --- | --- |
| BE-01 | 真实脚本会话失效 | P1 | `server/scripts/api-tests/permission/e2e_permission_realrun.py` | fixture 登录态 | 课程任课/成员权限变更后后端撤销旧 session，脚本继续复用旧 token 导致 `401` | 已修复，刷新受影响账号登录态 |
| BE-02 | OpenAPI 权限登记漂移 | P1 | `server/src/test/java/com/aubb/server/integration/AuthzOpenApiAccessRegistry.java` | 权限路径注册 | 注册表含已删除路径且缺少当前 PUT/DELETE 路径 | 已修复 |
| BE-03 | 测试日期/业务漂移 | P2 | `server/src/test/java/com/aubb/server/integration/*IntegrationTests.java` | 多个集成测试 | 固定 2026 时间窗和旧申诉通知类型导致回归易漂移 | 已修复 |
| BE-04 | V48 旧能力残留 | P1 | grading 相关服务、视图、迁移、测试 | 成绩权重/快照/申诉 | V48 简化后仍有旧字段/测试/文档残留 | 已清理并通过后端测试基线 |

## 9. 前后端接口一致性问题

| 编号 | 前端文件 | 后端文件 / 契约 | 方法/路径 | 问题描述 | 修复状态 |
| --- | --- | --- | --- | --- | --- |
| API-01 | `web/src/shared/api/generated/openapi.ts` | `GET /v3/api-docs` | OpenAPI | 生成类型落后于运行时后端契约 | 已从真实后端重新生成 |
| API-02 | 学生作业/课程/实验页 | `MyCourseClassView.java` | `GET /api/v1/me/courses` | 前端读取不存在的 `features` 字段 | 已去除读取，typecheck/build/E2E 通过 |
| API-03 | `web/next.config.ts` 使用方式 | 后端 `POST /api/v1/auth/login` | rewrite | 真实 E2E 启动前端时必须设置 `AUBB_SERVER_ORIGIN`，否则 Next 返回 404 | 已在报告记录，重启后用无效登录探针确认后端 `401 INVALID_CREDENTIALS` |
| API-04 | 教师课程资源页 | `CourseResourceTeacherController`、对象存储配置 | `POST /api/v1/teacher/course-offerings/{offeringId}/resources` | 后端未启用 MinIO 时资源上传返回 `COURSE_RESOURCE_STORAGE_DISABLED`，按钮 E2E 只能验证失败路径 | 真实联调后端改用本地 MinIO 配置启动，readiness 显示 `minioStorage=UP`，资源上传/下载 E2E 通过 |

## 10. 测试覆盖现状

| 覆盖类型 | 命令 / 方式 | 结果 |
| --- | --- | --- |
| 后端 verify | `cd server && bash ./mvnw verify` | 基线通过 |
| 后端格式 | `cd server && bash ./mvnw spotless:check` | 基线通过 |
| 后端测试 | `cd server && bash ./mvnw test` | `317` tests，0 failures / 0 errors |
| 权限脚本单测 | `cd server && python3 scripts/api-tests/permission/e2e_permission_realrun_test.py` | 1 个脚本回归测试通过 |
| 真实权限 API | `cd server && BASE_URL=http://127.0.0.1:18080 ... bash scripts/api-tests/permission/run_permission_e2e.sh` | `22/22` 通过 |
| 前端 lint | `cd web && npm run lint` | 通过 |
| 前端类型检查 | `cd web && npm run typecheck` | 通过 |
| 前端单元测试 | `cd web && npm run test` | 11 个测试文件、24 个测试通过 |
| 前端构建 | `cd web && npm run build` | 通过 |
| 真实后端 Playwright | `cd web && AUBB_E2E_REAL_BACKEND=1 ... npm run test:e2e` | 17 个 Chromium 用例通过 |
| 文档构建 | `cd docs && npm run docs:build` | 通过 |

## 11. 修复计划

| 优先级 | 问题 | 处理结果 |
| --- | --- | --- |
| P1 | 权限真实脚本复用被撤销 token | 已修复并补脚本单测 |
| P1 | 运行时 OpenAPI 类型刷新后学生端 `features` 类型错误 | 已按当前契约适配 |
| P1 | V48 后文档/API/测试仍引用旧成绩能力 | 已同步文档、测试和代码残留 |
| P2 | 教师公告空提交静默 | 已修复并纳入真实 E2E |
| P2 | 顶栏搜索无实际导航 | 已修复并补单元测试 |
| P2 | 用户管理顶部“批量导入”假按钮 | 已修复并纳入单元测试与真实 filechooser E2E |
| P2 | 教师课程资源上传/下载缺少浏览器级闭环 | 已补 MinIO 真实启动条件、下载行为单测和课程资源上传/改名/下载/删除 E2E |
| P2 | E2E 退出登录 selector 不匹配 | 已修复 |

## 12. 真实联调测试计划

| 步骤 | 命令 / 操作 | 结果 |
| --- | --- | --- |
| 启动依赖 | `cd server && docker compose up -d` | PostgreSQL、RabbitMQ、MinIO、Redis、go-judge 已启动；首次 go-judge 构建遇到 Debian 502，重试成功 |
| 启动后端 | `SERVER_PORT=18080 ... bash ./mvnw spring-boot:run` | 本地库已存在学校根节点 `SCH-REALRUN`，启用 bootstrap 且传入新 code 会失败；最终关闭 bootstrap、保留本地 JWT 后启动成功，Tomcat 监听 `18080`，Flyway 48 个迁移完成 |
| 后端探针 | `curl /actuator/health/readiness`、`curl /v3/api-docs` | readiness `UP`，最终联调用本地 MinIO 启动后响应包含 `db`、`readinessState`、`redisEnhancement`、`minioStorage`；OpenAPI `3.1.0`、124 paths |
| 启动前端 | `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run dev -- --hostname 127.0.0.1 --port 3000` | 登录页可访问，API rewrite 生效 |
| 真实 E2E | Playwright Chromium 17 用例 | 登录、导航、权限、用户批量导入 filechooser、课程公告创建/编辑/删除、课程资源上传/改名/下载/删除、学生作业/成绩等通过 |
| 浏览器点验 | Playwright MCP | 管理员、教师、学生关键按钮和路由点验完成 |

## 13. 风险与遗留问题

| 风险 | 当前证据 | 原因 / 处理建议 |
| --- | --- | --- |
| 破坏性按钮未全部提交 | 按钮级报告列出未覆盖批量导入文件提交、禁用用户、发布成绩等写入重操作 | 为避免扩大本地数据副作用，当前只对课程公告和课程资源做创建-验证-清理闭环；后续在一次性数据库中补其余重写入流程 |
| 文件上传/下载覆盖仍不完整 | 课程资源已用本地 MinIO 完成上传、下载和删除闭环，但提交附件、实验附件、成绩导出等下载入口尚未逐一浏览器级覆盖 | 复用 `downloadBinary` 单元测试与课程资源 E2E 模式，逐步补齐其他文件入口 |
| 通知 SSE 增量未验证 | 当前页面可达，顶栏显示轮询模式 | 后续单独验证 EventSource、断线回退和未读增量 |
| 工作区大量未提交变更 | `server/`、`web/`、`docs/` 均非 clean | 提交前按子仓库复核 diff，避免混入无关变更 |
| 服务已停止 | 收尾后 `3000`、`18080` 不可连接，compose 无运行容器 | 这是收尾动作；需要复测时按本报告启动命令重新启动 |
