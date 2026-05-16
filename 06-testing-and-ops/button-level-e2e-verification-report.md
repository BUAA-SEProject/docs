# 按钮级 E2E 验证报告

更新日期：2026-05-16

## 1. 测试环境

| 项目 | 实际值 |
| --- | --- |
| 前端 | Next.js dev server，`http://127.0.0.1:3000` |
| 后端 | Spring Boot，`http://127.0.0.1:18080` |
| 依赖 | Docker compose 启动 PostgreSQL、RabbitMQ、MinIO、Redis、go-judge |
| 前端代理 | `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080` |
| 浏览器 | Playwright Chromium |
| 敏感信息处理 | 报告只记录账号标识，不记录 token、cookie、JWT、私钥或真实密钥 |
| 收尾状态 | 验证完成后执行停止前端、后端和 compose 容器，未删除数据卷 |

## 2. 启动方式

| 步骤 | 命令 / 操作 | 结果 |
| --- | --- | --- |
| 本地依赖 | `cd server && docker compose up -d` | PostgreSQL、RabbitMQ、MinIO、Redis、go-judge 已运行；首次 go-judge 构建遇到 Debian 502，重试成功 |
| 后端 | `SERVER_PORT=18080 AUBB_MINIO_ENABLED=true ... bash ./mvnw spring-boot:run` | 本地库已存在学校根节点 `SCH-REALRUN`，启用 bootstrap 且传入新 code 会失败；最终关闭 bootstrap 并启用本地 MinIO 后 `18080` 可访问，Flyway 48 个迁移完成，readiness 包含 `minioStorage=UP` |
| 前端 | `AUBB_SERVER_ORIGIN=http://127.0.0.1:18080 npm run dev -- --hostname 127.0.0.1 --port 3000` | `3000` 可访问，rewrite 到真实后端 |
| 代理探针 | 无效登录请求经 `http://127.0.0.1:3000/api/v1/auth/login` | 返回后端 `401 INVALID_CREDENTIALS`，确认不是 Next `404` |

## 3. 测试账号和测试数据

| 角色 | 账号标识 | 密码记录策略 | 测试数据 |
| --- | --- | --- | --- |
| 管理员 | `U-SA1` | 不在报告记录密码 | 管理端平台配置、用户、学期、课程模板、开课、审计日志 |
| 教师 | `U-TA1` | 不在报告记录密码 | 种子课程 `数据结构 2025 秋`、课程 ID `1`、公告/成员/资源/题库/作业入口 |
| 学生 | `U-ST1` | 不在报告记录密码 | 种子作业 `Task-A1-Closed`、`Task-Offering-Published`、`Task-A1-Published`、`Task-Programming-A1`，作业详情 ID `6` |

## 4. 自动化覆盖状态

| 验证项 | 命令 / 文件 | 结果 |
| --- | --- | --- |
| 前端单元测试 | `npm run test` | 11 个测试文件、24 个测试通过 |
| 顶栏全局搜索 | `web/src/tests/unit/shared/ui/topbar.test.tsx`、`web/src/tests/unit/shared/routing/*` | 覆盖搜索匹配与 Enter 导航 |
| 下载行为单测 | `web/src/tests/unit/api/download.contract.test.ts` | 覆盖 `downloadBinary` 拉取 blob 后触发浏览器下载 |
| 默认 Playwright E2E | `npm run test:e2e` | 未设置 `AUBB_E2E_REAL_BACKEND=1` 时跳过真实 smoke |
| 真实后端 Playwright E2E | `AUBB_E2E_REAL_BACKEND=1 npm run test:e2e` | `17` 个 Chromium 用例通过 |
| 真实权限 API E2E | `bash scripts/api-tests/permission/run_permission_e2e.sh` | `22` 个真实 HTTP 权限场景通过 |
| 前端构建 | `npm run build` | 通过 |

## 5. 按钮级真实测试矩阵

| 编号 | 角色 | 页面 | 按钮/操作 | 前置数据 | 操作步骤 | 预期结果 | 实际结果 | API/网络请求 | 是否通过 | 问题编号 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTN-001 | 未登录 | `/login` | 输入错误凭据并点击“立即登录” | 无效账号 | 填用户名/密码，提交 | 停留登录页并显示错误 | 显示“用户名或密码错误” | `POST /api/v1/auth/login` 返回 401 | 通过 | 无 |
| BTN-002 | 管理员 | `/login` | 点击“立即登录” | `U-SA1` | 登录 | 进入管理端 | 跳转 `/admin`，显示“管理端工作台” | `POST /api/v1/auth/login`、`GET /api/v1/auth/me` | 通过 | 无 |
| BTN-003 | 教师 | `/login` | 点击“立即登录” | `U-TA1` | 登录 | 进入教师端 | 跳转 `/teacher`，显示“教师工作台” | 登录和当前用户 API | 通过 | 无 |
| BTN-004 | 学生 | `/login` | 点击“立即登录” | `U-ST1` | 登录 | 进入学生端 | 跳转 `/student`，显示“学生学习中心” | 登录和当前用户 API | 通过 | 无 |
| BTN-005 | 登录用户 | 用户菜单 | 点击“退出登录” | 已登录教师 | 打开用户菜单，点退出 | 返回登录页，会话清除 | 返回 `/login` | 前端会话清理/登出流程 | 通过 | FE-02 |
| BTN-006 | 学生 | 直接访问 `/admin` | 越权访问 | 已登录学生 | 地址栏跳转 `/admin` | 跳转无权限页 | 跳转 `/unauthorized`，显示“权限不足” | 前端路由守卫和当前角色 cookie | 通过 | 无 |
| BTN-007 | 管理员 | `/admin/platform-config` | 清空平台名称后点“保存配置” | 已登录管理员 | 清空必填字段，点击保存 | 浏览器阻止提交并聚焦字段 | 未离开当前页，焦点停留在 `platformName` | 未提交成功写入 | 通过 | 无 |
| BTN-008 | 管理员 | 顶栏搜索 | 输入 `课程` 并按 Enter | 已登录管理员 | 顶栏搜索框输入并提交 | 跳转匹配的课程入口 | 跳转 `/admin/course-catalogs` | 前端路由跳转 | 通过 | FE-04 |
| BTN-009 | 管理员 | 侧边栏 | 点击“用户管理” | 已登录管理员 | 点击菜单项 | 到用户列表 | 标题为“用户管理” | 用户列表 API | 通过 | 无 |
| BTN-010 | 管理员 | 侧边栏 | 点击“学期管理” | 已登录管理员 | 点击菜单项 | 到学期列表 | 标题为“学期管理” | 学期 API | 通过 | 无 |
| BTN-011 | 管理员 | `/admin/users` | 点击顶部“批量导入” | 已登录管理员 | 点击页面头部批量导入按钮 | 打开 CSV 文件选择器且为单文件选择 | Playwright 捕获 `filechooser`，`isMultiple=false` | 前端触发隐藏文件 input，未提交文件 | 通过 | FE-06 |
| BTN-012 | 教师 | `/teacher/courses/1` | 打开课程详情 | 种子课程 ID `1` | 访问课程详情 | 显示课程内容入口 | 显示教学班、成员、公告、讨论、资源、实验、作业入口 | 教师课程/教学班 API | 通过 | 无 |
| BTN-013 | 教师 | `/teacher/courses/1/announcements` | 空表单点击“发布” | 已登录教师 | 不填标题/正文，点击发布 | 浏览器必填提示 | 标题输入框聚焦，`validationMessage=请填写此字段。` | 未提交成功写入 | 通过 | FE-01 |
| BTN-014 | 教师 | `/teacher/courses/1/announcements` | 创建、编辑、删除公告 | 已登录教师 | 使用唯一标记创建公告，编辑标题/正文，再删除 | 公告创建后可见，编辑后内容更新，删除后不可见 | `teacher can create edit and delete an announcement` 用例通过 | 教师公告 API | 通过 | FE-01 |
| BTN-015 | 教师 | `/teacher/courses/1/resources` | 上传资源 | 已登录教师、本地 MinIO 启用 | 选择内存文本文件，填写唯一标题，点击“开始上传” | POST 成功，资源出现在列表 | 用例等待上传 POST 且 `ok=true`，标题可见 | `POST /api/v1/teacher/course-offerings/1/resources` | 通过 | API-04 |
| BTN-016 | 教师 | `/teacher/courses/1/resources` | 编辑资源标题 | 已上传 E2E 资源 | 点击编辑按钮，修改标题，点击保存 | 标题更新后可见 | 编辑后唯一标题可见 | `PUT /api/v1/teacher/course-resources/{resourceId}` | 通过 | FE-08 |
| BTN-017 | 教师 | `/teacher/courses/1/resources` | 下载资源 | 已上传并改名的资源 | 点击“下载” | 下载请求成功并触发浏览器下载行为 | 下载 API 返回 OK；`downloadBinary` 单测覆盖 object URL + anchor click | `GET /api/v1/teacher/course-resources/{resourceId}/download` | 通过 | FE-07 |
| BTN-018 | 教师 | `/teacher/courses/1/resources` | 删除资源 | 已下载验证的 E2E 资源 | 点击删除按钮并确认 | 资源从列表消失 | 删除后唯一标题计数为 0 | `DELETE /api/v1/teacher/course-resources/{resourceId}` | 通过 | API-04 |
| BTN-019 | 学生 | `/student/assignments` | 点击“作业任务”入口 | 种子作业存在 | 进入列表 | 展示作业和“开始做题”入口 | 显示真实种子作业和入口 | 学生作业 API | 通过 | API-02 |
| BTN-020 | 学生 | `/student/assignments/6` | 打开作业详情 | 种子作业 ID `6` | 访问详情 | 展示附件、答案、提交历史 | 显示 `Task-Programming-A1`、附件选择、提交答案、提交历史 | 作业详情/提交 API | 通过 | 无 |
| BTN-021 | 学生 | `/student/grades` | 点击“我的成绩” | 已登录学生 | 访问成绩页 | 成绩页可达 | 显示成绩页、导出成绩按钮和课程选择提示 | 学生成绩 API | 通过 | 无 |
| BTN-022 | 学生 | `/student/labs` | 打开实验项目 | 已登录学生 | 访问实验页 | 实验页可达 | 页面可达，按当前 `MyCourseClassView` 契约不再读取 `features` | 学生课程/实验 API | 通过 | API-02 |
| BTN-023 | 教师 | `/teacher/grading/gradebook` | 打开成绩册 | 已登录教师 | 访问页面 | 成绩册页可达 | 页面可达 | 教师成绩 API | 通过 | 无 |
| BTN-024 | 教师 | `/teacher/labs` | 打开实验管理 | 已登录教师 | 访问页面 | 实验管理页可达 | 页面可达 | 教师实验 API | 通过 | 无 |
| BTN-025 | 教师 | `/teacher/notifications` | 打开通知入口 | 已登录教师 | 访问通知页 | 通知页可达 | 页面可达 | 通知 API | 通过 | 无 |
| BTN-026 | 学生 | `/student/notifications` | 打开通知入口 | 已登录学生 | 访问通知页 | 通知页可达 | 页面可达 | 通知 API | 通过 | 无 |

## 6. 已修复的用户可见操作

| 页面 / 组件 | 操作 | 原问题 | 当前结果 | 验证 |
| --- | --- | --- | --- | --- |
| 顶栏 `Topbar` | 在全局搜索框输入并按 Enter | 输入框没有实际导航行为 | 根据当前用户可见导航项跳到首个匹配目标 | 单元测试；浏览器中管理员输入 `课程` 后跳到 `/admin/course-catalogs` |
| 登录用户菜单 | 点击退出登录 | E2E 使用 `button` role 查询，但实际 Radix 菜单项是 `menuitem` | 测试改为真实 role，退出后回到 `/login` | 单条退出用例和完整真实 E2E 通过；浏览器点验通过 |
| 教师课程公告 | 空标题/正文点击“发布” | `handleCreate` 静默 return，无可见反馈 | 表单标题/正文为 `required`，空提交聚焦标题并显示浏览器必填提示 | 新增 Playwright 用例；浏览器点验通过 |
| 教师课程资源 | 上传、改名、下载、删除资源 | 首次 E2E 发现后端未启用对象存储时上传返回 `COURSE_RESOURCE_STORAGE_DISABLED`；下载工具只拉取 blob 不触发下载 | 后端联调启用本地 MinIO；上传按钮等待 POST 成功；下载工具触发浏览器下载；资源 E2E 创建后清理 | `download.contract.test.ts` 通过；资源 E2E 通过；完整真实 E2E `17/17` 通过 |
| 管理员用户管理 | 顶部“批量导入” | 按钮没有 click handler，无法触发已有 CSV 上传控件 | `FileUploadField` 增加 `triggerRef`，顶部按钮触发隐藏文件 input | `file-upload-field.test.tsx`；真实 `filechooser` E2E 通过 |
| 学生课程/作业/实验入口 | 读取课程班级功能开关 | 前端读取运行时 DTO 不存在的 `features` | 去除不存在字段依赖，内容和权限交由后端接口控制 | `typecheck`、`build`、真实 E2E 通过 |

## 7. 失败项

| 项目 | 原因 | 当前状态 |
| --- | --- | --- |
| 首次重跑真实 E2E 时 14 个登录前置失败 | 重启 Next dev server 时漏设 `AUBB_SERVER_ORIGIN`，`/api/v1/auth/login` 由 Next 返回 `404` | 已按正确环境变量重启，代理探针返回后端 `401 INVALID_CREDENTIALS`，随后真实 E2E `17/17` 通过 |
| 后端启用 bootstrap 后启动失败 | 当前本地库已存在学校根节点 `SCH-REALRUN`，重新传入其他学校 code 会触发一致性保护 | 最终关闭 bootstrap，用既有 realrun 种子数据启动后端并完成验证 |
| 课程资源 E2E 首次上传后列表无新增 | 后端未启用 MinIO，对象存储 Bean 不存在，上传 API 返回 `503 COURSE_RESOURCE_STORAGE_DISABLED` | 以本地 Docker MinIO 重启后端，readiness 显示 `minioStorage=UP`；资源上传/改名/下载/删除 E2E 通过 |
| go-judge 首次镜像构建失败 | Debian package 源临时 `502` | 重试后成功 |

## 8. 当前覆盖缺口

| 缺口 | 原因 | 建议 |
| --- | --- | --- |
| 破坏性按钮未全部提交 | 课程公告和课程资源已做创建-验证-清理闭环，但禁用用户、批量导入文件提交、发布成绩等重写入操作仍未全覆盖 | 后续在专用一次性数据库中新增“创建-验证-删除/清理”完整 Playwright 流程 |
| 文件上传/下载入口未全量覆盖 | 课程资源已覆盖上传/下载/删除；提交附件、实验附件、成绩导出等入口尚未逐个浏览器级覆盖 | 复用课程资源 E2E 模式，为每类文件入口准备固定测试文件和清理策略 |
| 通知 SSE 增量未验证 | 当前顶栏显示轮询模式；E2E 只验证通知页面可达和未读数 | 后续单独验证 EventSource 连接、断线回退和未读数增量 |
| 重写类操作未全量自动化 | 批量导入、发布成绩、实验评阅等需要更严格测试数据隔离 | 在专用空库中补充写入闭环和清理脚本 |

## 9. 结论

真实后端、真实前端、运行时 OpenAPI、真实权限 API 和浏览器级关键操作已完成闭环。当前按钮级验收没有发现阻断登录、导航、权限守卫、用户批量导入入口、课程公告、课程资源、学生作业与成绩查看的 P0/P1 问题；已发现的教师公告空表单静默反馈、顶栏搜索无实际行为、用户批量导入假按钮、下载按钮只取 blob 不触发浏览器下载、退出登录 selector 漂移、课程资源对象存储启动条件和学生端 DTO 不一致问题均已修复或记录为明确启动前置并验证。
