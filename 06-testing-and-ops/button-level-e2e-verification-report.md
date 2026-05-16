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
| 数据策略 | 新增数据统一使用 `E2E-*` 前缀；可清理则清理，不可清理则记录残留 |
| 敏感信息 | 只记录环境变量名，不记录密码、token、cookie、JWT、私钥或真实连接串 |

## 2. Full Suites 结果

| Suite | 用例数 | 覆盖范围 | 本轮结果 |
| --- | ---: | --- | --- |
| `full-admin.spec.ts` | 5 | 认证、平台配置、组织、用户、CSV 导入、学期、课程模板、开课、审计、权限解释 | 通过 |
| `full-course.spec.ts` | 5 | 教学班、成员、课程资源、讨论、题库、判题环境 | 通过 |
| `full-assignment-judge.spec.ts` | 3 | 作业生命周期、结构化提交、附件、编程工作区、样例运行、正式判题、教师评分和重判 | 通过 |
| `full-grading-lab-notification.spec.ts` | 3 | 成绩册、实验生命周期、报告附件、评阅、通知已读、SSE | 通过 |
| `full-navigation-permission.spec.ts` | 3 | 三角色导航、快捷入口、顶栏搜索、用户菜单、路由守卫、401/403、响应式 | 通过 |

补充 smoke specs 保留原登录、治理、课程、作业、成绩实验通知页面冒烟覆盖。Task 10 已用 `AUBB_E2E_REAL_BACKEND=1 npm run test:e2e` 重新跑全部 E2E，最终 `36 passed`。

## 3. GAP 覆盖矩阵

| GAP | 状态 | 证据摘要 |
| --- | --- | --- |
| `GAP-AUTH-01` | 已真实验证 | refresh、revoke、无 token `401`、管理员撤销会话后旧 token 失效 |
| `GAP-ADMIN-01` | 已修复后验证 | 平台配置保存、重载、恢复原值；后端 nullable 字段更新策略已修复 |
| `GAP-ADMIN-02` | 部分验证 | 子组织创建并出现在树中；根 `SCHOOL` 创建受后端唯一根策略限制；无删除 API |
| `GAP-ADMIN-03`、`GAP-ADMIN-04`、`GAP-ADMIN-05` | 已真实验证 | 用户创建、搜索、详情、身份/profile/组织关系、禁用启用、撤销会话、CSV 成功/失败行 |
| `GAP-ADMIN-06`、`GAP-ADMIN-07`、`GAP-ADMIN-08`、`GAP-ADMIN-09`、`GAP-ADMIN-10` | 已真实验证 | 学期、课程模板、开课、审计日志、权限解释允许/拒绝/错误输入 |
| `GAP-COURSE-01`、`GAP-COURSE-02` | 已真实验证 | 教学班、功能开关、批量成员、CSV 导入、禁用恢复、转班 |
| `GAP-COURSE-03`、`GAP-DOWNLOAD-01` | 已真实验证 | 教师资源上传/改名/下载/删除，学生侧下载同一资源 |
| `GAP-COURSE-04` | 已真实验证 | 教师发帖/回复、学生回复、锁定后学生回复被拒绝、解锁 |
| `GAP-COURSE-05` | 已真实验证 | 单选、多选、简答、文件、编程题创建、筛选、编辑、归档 |
| `GAP-COURSE-06` | 已真实验证 | 判题环境创建、编辑、归档 |
| `GAP-ASSIGN-01`、`GAP-ASSIGN-02` | 已真实验证 | 创建结构化作业、编辑、替换试卷、发布、学生可见、关闭后提交被拒绝 |
| `GAP-ASSIGN-03`、`GAP-ASSIGN-04` | 已真实验证 | 选择/简答/文件/编程提交、提交历史、详情、附件下载 |
| `GAP-ASSIGN-05`、`GAP-ASSIGN-06`、`GAP-ASSIGN-07` | 已真实验证 | 工作区文件操作、修订、恢复、重置、样例运行、正式判题、报告下载、教师评分和重判 |
| `GAP-GRADE-01`、`GAP-GRADE-02`、`GAP-GRADE-03` | 已真实验证 | 成绩册查询、报告、导出、人工评分、批量调整、模板下载、CSV 导入、发布、学生查询导出 |
| `GAP-LAB-01`、`GAP-LAB-02`、`GAP-LAB-03` | 已真实验证 | 实验创建/编辑/发布/关闭，学生附件和报告，教师评阅发布 |
| `GAP-NOTIF-01`、`GAP-NOTIF-02` | 已真实验证 | 通知列表、未读数、单条已读、全部已读，SSE `connected` 和 `notification` |
| `GAP-NAV-01` | 已真实验证 | 三角色侧边栏、概览快捷入口、顶栏搜索、用户菜单、越权页面/API |
| `GAP-RESP-01` | 已真实验证 | 管理、教师、学生关键页桌面和移动视口主操作可见可点击 |

## 4. 按钮/操作矩阵

| 编号 | 角色 | 页面/API | 操作 | 实际验证 |
| --- | --- | --- | --- | --- |
| BTN-001 | 未登录 | `/login` | 错误登录、正确登录 | 三角色登录落点、失败提示、退出登录由 smoke 覆盖 |
| BTN-002 | 管理员 | `/api/v1/auth/*` | refresh、revoke、me、会话撤销 | `full-admin` 验证旧会话失效和无 token `401` |
| BTN-003 | 管理员 | `/admin/platform-config` | 保存配置 | 读取、保存、重载、恢复原值 |
| BTN-004 | 管理员 | `/admin/org-units` | 创建组织 | 子组织创建并在树中可查；根创建按后端策略拒绝 |
| BTN-005 | 管理员 | `/admin/users` | 新增用户、搜索、批量导入 | 创建用户、搜索命中、CSV 一成功一失败、导入用户可查 |
| BTN-006 | 管理员 | `/admin/users/[userId]` | 身份、profile、组织关系、状态、撤销会话 | 全部 API 写入后验证；禁用用户登录返回 `ACCOUNT_DISABLED` |
| BTN-007 | 管理员 | 学期/课程模板/开课 | 创建、筛选、编辑、进入详情 | 三类治理对象均完成闭环 |
| BTN-008 | 管理员 | 审计/权限解释 | 筛选、允许/拒绝/错误输入 | 审计日志查到写操作；权限解释覆盖三类结果 |
| BTN-009 | 教师 | 课程成员 | 创建教学班、功能开关、批量添加、CSV 导入、禁用恢复、转班 | `full-course` 完成真实 API 闭环 |
| BTN-010 | 教师/学生 | 课程资源 | 上传、改名、下载、删除、学生下载 | 教师和学生下载均 OK 且非空；资源最终删除 |
| BTN-011 | 教师/学生 | 课程讨论 | 发帖、回复、锁定、学生锁定态回复 | 锁定后学生回复被拒绝，最后解锁 |
| BTN-012 | 教师 | 题库 | 五类题创建、筛选、编辑、归档 | 已归档题目作为残留 |
| BTN-013 | 教师 | 判题环境 | 创建、编辑、归档 | 已归档 profile 作为残留 |
| BTN-014 | 教师/学生 | 作业 | 创建、编辑、替换试卷、发布、关闭、学生可见性 | 关闭后学生提交被拒绝 |
| BTN-015 | 学生 | 作业提交 | 选择、简答、文件、编程答案提交 | 提交历史、提交详情、附件下载均验证 |
| BTN-016 | 学生 | 编程工作区 | 新建目录/文件、重命名、删除、保存、修订、恢复、重置 | 工作区 API 和页面入口均验证 |
| BTN-017 | 学生/教师 | 判题 | 样例运行、正式判题、报告查看/下载、重判 | 学生和教师报告下载均 OK；教师答案重判验证 |
| BTN-018 | 教师/学生 | 成绩册 | 查询、报告、导出、调分、导入模板、导入、发布、学生查看导出 | 开课和班级维度均覆盖 |
| BTN-019 | 教师/学生 | 实验 | 创建、编辑、发布、附件上传、保存、提交、评阅、发布、关闭 | 学生和教师附件下载均 OK |
| BTN-020 | 学生 | 通知 | 未读数、单条已读、全部已读、SSE | SSE 直连本地后端验证 `connected` 和 `notification` |
| BTN-021 | 三角色 | 侧边栏/快捷入口/顶栏搜索/用户菜单 | 全部导航项点击，搜索 Enter，菜单打开 | `full-navigation` 验证三角色全部导航 |
| BTN-022 | 三角色 | 权限负例 | 越权页面、无 token API、无角色 API | 页面回退到默认首页/无权限/登录；API 返回 `401/403` |
| BTN-023 | 三角色 | 响应式 | `1280x800`、`390x844` | 主按钮或移动导航菜单可见可点击 |

## 5. 本轮修复

| 文件 | 问题 | 修复 | 验证 |
| --- | --- | --- | --- |
| `PlatformConfigEntity.java` | nullable 配置字段清空后未写回 | 对可空字段使用 `FieldStrategy.ALWAYS` | 平台配置集成测试和 `full-admin` |
| `CourseAdministrationApplicationService.java` | 开课 keyword 搜索大小写不一致 | 改为大小写不敏感查询 | 课程集成测试和 `full-admin` |
| `JwtTokenService.java` | 无 primary org 用户登录写入 null JWT claim | 非空时才写入 claim | auth 集成测试 |
| `real-backend.ts` | 登录结果字段、429 重试、下载断言、session 复用不足 | 修复 `userId`、只对 429 retry、下载非空断言、支持传入 session | full suites |
| `full-fixtures.ts` | 种子学生可能被旧权限脚本置为 `DROPPED` | 每轮创建新的 active `E2E-*` fixture student | full suites |
| `full-assignment-judge.spec.ts` | 教师提交详情页仍用学生 cookie | 跳转前切换到教师 session | `3 passed` |
| `full-grading-lab-notification.spec.ts` | Node fetch 经 Next rewrite 读取 SSE chunk 不稳定，且触发函数可重复执行 | SSE 探针直连 `AUBB_SERVER_ORIGIN`，reader 加 deadline，触发状态独立保存 | `3 passed` |
| `full-navigation-permission.spec.ts` | 未先进入角色 shell、同名链接严格模式冲突、按钮文案和路由守卫断言不匹配 | 登录后进入角色首页，限定 `navigation`，改用“新增用户”，允许默认首页回退 | `3 passed` |
| `playwright.config.ts`、旧 smoke specs、`real-backend.ts` | 完整真实后端套件并行跑共享账号会触发登录限流，30 秒预算下出现超时 | 真实后端模式改为 1 worker 和 90 秒预算；非认证 smoke 使用 API session 注入；UI 登录 helper 只在明确 429 时等待重试 | 完整 `npm run test:e2e` 为 `36 passed` |

## 6. 残留数据

| 类型 | 残留策略 |
| --- | --- |
| `E2E-*` 用户 | 管理端、课程成员和 fixture student 用例会保留用户，用于审计；无统一删除 API |
| `E2E-*` 组织、学期、课程模板、开课 | 创建后保留；无删除 API |
| `E2E-*` 作业、提交、判题、成绩记录 | 创建后保留；当前业务无删除 API |
| 题库和判题环境 | 已归档后保留 |
| 课程资源 | 用例内删除 |
| 实验 | 最终关闭后保留 |
| 旧 seed 变更 | 权限 realrun 脚本可能保留 `U-ST1` 在 A1 为 `DROPPED`、`U-STX1` A1 到 A2 转班状态；full fixture 已规避 |

## 7. 当前风险

| 风险 | 说明 |
| --- | --- |
| UI 点击深度 | 部分重写入闭环通过 API helper 完成，页面入口和关键按钮已打开验证；不是每个表单字段都通过鼠标键盘逐项填写 |
| 数据残留 | 本地库会累积 `E2E-*` 数据；报告记录残留类型，未执行破坏性清库 |
| SSE 路径差异 | 浏览器 UI 使用前端配置和轮询回退；测试中的 SSE 事件为直连本地后端验证，避免 Node fetch 经 Next rewrite 的流式读取差异 |
| 全量结论依赖本地环境 | 结论只针对本地 Docker、`18080` 后端、`3000` 前端和当前种子数据，不代表生产环境 |

## 8. 收尾状态

| 项目 | 结果 |
| --- | --- |
| 前端 `3000` | Task 11 已停止；`curl --max-time 2 -sS http://127.0.0.1:3000/login` 连接失败 |
| 后端 `18080` | Task 11 已停止；`curl --max-time 2 -sS http://127.0.0.1:18080/actuator/health/readiness` 连接失败 |
| Docker compose | `docker compose down` 已执行；`docker compose ps` 无运行服务 |
