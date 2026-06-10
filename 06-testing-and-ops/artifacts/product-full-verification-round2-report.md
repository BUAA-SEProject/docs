# AUBB 产品全功能完整验证第二轮报告

## 1. 验证元信息

- 执行日期：2026-06-10
- 工作区：`/Users/moorefoss/Code/AUBB`
- 执行合同：`goal.md` 第二阶段、`goal-test.md`
- 本轮边界：第二阶段验收期间未修改应用代码、配置代码、测试代码和生产文档正文；第三阶段补漏已修改 `web/` 应用代码、单元测试和 E2E 测试，并在本报告中记录回归证据。
- 主证据规则：用户可见功能以 Playwright MCP 页面操作为主证据；命令、API、数据库、日志和对象存储仅作为辅助证据。
- 产物：
  - 功能清单：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-feature-inventory.md`
  - 主报告：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-report.md`
  - 三次演示彩排记录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-rehearsal-log.md`
  - 截图目录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-screenshots/`
  - 辅助证据目录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-evidence/`

## 2. 总体验证结论

当前结论：`通过`

第二轮命令门禁全部通过，Playwright MCP 已形成 210 张截图证据，其中 3 张为第三阶段补漏回归截图，4 张为公共认证补充截图，5 张为公告发布和通知状态变更补充截图，6 张为讨论创建、回复和锁定补充截图，1 张为教师资源上传下载补充截图，2 张为教师题库新增、编辑和归档补充截图，2 张为教师判题环境新增、编辑和归档补充截图，12 张为题库结构化题型、作业创建发布、学生结构化提交、教师批改、成绩发布与学生反馈补充截图，7 张为报告型实验创建发布、学生报告提交、教师评阅发布、学生反馈回查以及实验编辑关闭补充截图，11 张为学生 WebIDE 历史恢复、正式提交和实验会话启停补充截图，其中 2 张为 P1-R2-006 自动轮询回归截图，6 张为管理员平台配置保存/恢复、组织节点创建、学期创建编辑、课程模板创建编辑、开课创建编辑和共同管理学院补充截图，1 张为教师课程工作台教学班创建补充截图，3 张为教师成员添加、CSV 导入、停用和恢复补充截图，6 张为作业草稿编辑、发布后编辑阻断和关闭补充截图。三次演示彩排主线均已执行并记录。第一阶段修复后的 WebIDE 样例自测、编程题判题和实验 Web 终端主线在第二轮中均能演示。

第三阶段已修复并回归第二轮报告中的 3 个 P2 可理解性问题；补证过程中又发现并修复 `P1-R2-004`：实验报告评阅发布后学生端未显示教师评语，以及 `P2-R2-005`：报告型实验误请求运行时 current session 产生 400 网络噪音。继续补证学生 WebIDE 和编程正式提交时发现并修复 `P1-R2-006`：正式提交后学生提交详情页停留“运行中”，刷新同一页面后才显示 `ACCEPTED / 100 分`。修复后通过临时编程作业 `260` 和学生提交 `57` 完成 MCP 回归：提交详情页无需手动刷新，网络摘要显示 3 次 `GET /api/v1/me/submissions/57/judge-jobs` 轮询后自动请求 `GET /api/v1/me/submissions/57` 并显示 `ACCEPTED / 100 分`。继续补证教师成员管理时发现并修复 `P2-R2-007`：添加课程成员成功后弹窗不关闭且列表不刷新；修复后成员添加、CSV 导入、停用和恢复均已形成 MCP 页面与网络证据。继续补证作业编辑/关闭时发现并修复 `P2-R2-008`：已发布作业仍暴露可点击编辑入口并触发后端 `ASSIGNMENT_STATUS_INVALID` 400；修复后已发布作业编辑入口禁用，编辑页提示“只有草稿作业可以编辑”，草稿作业编辑和已发布作业关闭均已形成 MCP 页面与网络证据。后续补充 MCP 验证已覆盖管理员平台配置保存/恢复、管理员组织节点创建、管理员学期创建/编辑、管理员课程模板创建/编辑、管理员开课创建/编辑和共同管理学院选择、教师课程工作台教学班创建、教师成员添加/导入/状态变更、教师公告新建、教师资源上传下载、教师题库新增简答题、题库编辑归档、教师结构化题型新增、教师判题环境新增配置、判题环境编辑归档、教师作业创建发布、教师作业草稿编辑、发布后编辑规则阻断、教师作业关闭、教师讨论创建/回复/锁定、教师通知全部已读、学生讨论回复、学生结构化作业提交、文件题附件上传下载、教师提交批改、成绩发布、学生成绩/反馈回查、实验创建发布、实验编辑发布关闭、实验报告提交、教师评阅发布、学生实验反馈回查、报告型实验不再触发运行时会话查询、学生通知单条已读、通知网络摘要、学生 WebIDE 历史恢复、正式提交自动刷新和实验会话启停。最终又使用 Playwright MCP 对公共、管理员、教师、学生、开课助教、班级助教共 55 个 route / 角色组合执行完整 console/network 归因，结果无意外 console error、无意外业务 4xx/5xx、无未解释 request failure，证据见 `product-full-verification-round2-evidence/runtime/full-route-console-network-scan-20260610.md`。至此第二轮强制项均为 `通过` 或有依据的 `不适用`，三次演示彩排主线均已执行并记录，当前无 P0/P1 和未修复高影响 P2。

## 3. 上次缺口复核

| 缺口 | 第二轮纠偏动作 | 当前状态 |
| --- | --- | --- |
| 旧报告中 WebIDE / 判题 P1 | 第二轮 MCP 复核 WebIDE 页面和运行自测 | 已通过回归 |
| 旧报告中实验终端 P1 | 第二轮 MCP 复核实验终端输出 `round2-terminal` | 已通过回归 |
| `just e2e-real` 第一轮失败 | 第二轮重新执行完整真实后端 E2E | 已通过，`50 passed (4.0m)` |
| 三次彩排缺失 | 第二轮执行三次全角色主线彩排并保存截图，并在第三阶段补齐写入动作与 console/network 归因 | 通过 |
| 强制项允许停在 `未覆盖` | 第二轮清单只使用 `通过 / 失败 / 阻塞 / 不适用` | 已纠偏 |

## 4. 输入缺失与环境阻塞

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| `goal-test.md`、`goal.md`、`goal-repair.md` | 通过 | 当前轮已读取 |
| `AGENTS.md`、`AGENTS-shared.md`、`web/AGENTS.md`、`server/AGENTS.md`、`docs/AGENTS.md` | 通过 | 当前轮已读取 |
| `docs/04-development/frontend-design.md` | 通过 | 当前轮已读取 |
| `web/src/shared/routing/nav-config.ts`、`web/src/shared/routing/route-access.ts` | 通过 | 当前轮已读取 |
| `web/src/tests/e2e/README.md` | 通过 | 当前轮已读取 |
| `server/docs/stable-api.md` | 通过 | 已读取稳定接口范围 |
| `server/docs/product-specs/` | 通过 | 已检查规格目录 |
| `server/docs/generated/db-schema.md` | 通过 | 文件存在，用作运行时数据检查依据 |
| `web/docs/backend-requests.md` | 通过 | 当前待处理表为空 |
| `env/e2e.example` | 通过 | 已读取环境变量模板，真实值仅来自本地 `env/e2e.env` |
| `web/src/app/`、`web/src/features/`、`web/src/shared/api/generated/openapi.ts` | 通过 | 已用于功能清单生成 |

## 5. 命令门禁结果

| 顺序 | 命令 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | `just status` | 通过 | `product-full-verification-round2-evidence/commands/01-just-status.log` |
| 2 | `just --list` | 通过 | `product-full-verification-round2-evidence/commands/02-just-list.log` |
| 3 | `just dev-up` | 通过 | `product-full-verification-round2-evidence/commands/03-just-dev-up.log` |
| 4 | `just healthcheck-strict` | 通过 | `product-full-verification-round2-evidence/commands/04-just-healthcheck-strict.log` |
| 5 | 残留摘要检查 | 通过 | `product-full-verification-round2-evidence/commands/05-e2e-residual-cleanup-dry-run.log` |
| 6 | `just seed-fixtures` | 通过 | `caseCount=22`、`passedCount=22`、`failedCount=0`；见 `06-just-seed-fixtures.log` |
| 7 | `just e2e-real` | 通过 | 第二轮正式门禁 `50 passed (4.0m)`；见 `07-just-e2e-real.log`。2026-06-11 当前补跑先因 `full-organization-structure.spec.ts` 等待旧成员添加提示失败，见 `12-current-just-e2e-real-20260611.log`；修复 E2E 等待契约后补跑 `50 passed (4.4m)`，见 `13-current-just-e2e-real-after-test-fix-20260611.log`；本轮 MCP 成员添加回归后再次补跑 `50 passed (3.7m)`，见 `16-current-just-e2e-real-after-mcp-member-regression-20260611.log`。 |
| 8 | `just verify` | 通过 | 后端 `357` tests、web lint/typecheck、docs build 通过；见 `08-just-verify.log` |
| 9 | `just verify-full` | 通过 | 后端 verify、web lint/typecheck/unit/build、docs build 通过；见 `09-just-verify-full.log`；当前 E2E 契约修复和 MCP 成员添加回归后补跑通过，见 `18-current-just-verify-full-after-e2e-fix-20260611.log`。 |
| 10 | `cd docs && npm run docs:build` | 通过 | VitePress build complete，仍有既有 chunk size warning；见 `10-docs-build.log`；最终文本回填后补跑通过，见 `19-current-docs-build-after-final-doc-patch-20260611.log`。 |
| 11 | 第三阶段 `web` 定向单测 / lint / typecheck / build | 通过 | 登录/课程定向单测 2 files / 11 tests passed；学生实验页定向单测 1 file / 6 tests passed；`npm run lint`、`npm run typecheck`、`npm run build` 均通过；当前 E2E 契约修复后补跑 `npm run lint && npm run typecheck` 通过，见 `15-current-web-lint-typecheck-after-e2e-fix-20260611.log`。 |
| 12 | 第三阶段 `just verify` 与 docs build | 通过 | `just verify` 后端 357 tests / 0 failures，web lint/typecheck 与 docs build 通过；单独 `cd docs && npm run docs:build` 通过；当前 E2E 契约修复后补跑 `just verify` 通过，见 `17-current-just-verify-after-e2e-fix-20260611.log`。 |

## 6. 全功能清单摘要

- 第二轮清单覆盖公共认证、管理员、教师、学生、助教、运行时、文档、NFR 和演示彩排。
- 截图证据数量：`210` 张 PNG。
- 命令辅助证据数量：`10` 个命令日志。
- 当前清单状态：
  - `通过`：登录、路由守卫、三角色首页、管理员治理/平台配置保存恢复/组织节点创建/学期创建编辑/课程模板创建编辑/开课创建编辑/共同管理学院选择/用户/权限/审计、教师课程、教学班创建、成员添加/导入/状态变更、公告创建、资源上传下载、题库新增与编辑归档、判题环境新增与编辑归档、作业创建发布、作业草稿编辑、作业关闭、发布后编辑规则阻断、提交批改、成绩发布、实验创建编辑发布关闭和报告评阅、讨论创建/回复/锁定、教师/学生通知已读状态变更、学生课程、讨论回复、结构化作业提交、文件附件、WebIDE、WebIDE 历史恢复、编程题正式提交、成绩/反馈、实验会话启停、实验报告、助教授权与拒绝边界、命令门禁、三次彩排主线、全站关键页 console/network 归因。
  - `失败`：当前无未修复的 P1/P2 失败；第二轮 P2-R2-001、P2-R2-002、P2-R2-003、补证发现的 P1-R2-004、P2-R2-005、P1-R2-006、P2-R2-007、P2-R2-008 已在第三阶段修复并回归。
  - `阻塞`：无。

## 7. 逐角色验证结果

| 角色 | 当前状态 | 说明 |
| --- | --- | --- |
| 无登录用户 | 通过 | `/login` 可加载，未登录访问 `/admin` 会回到登录；空表单提交已显示应用内错误说明，见 P2-R2-001 第三阶段回归。 |
| 学校管理员 | 通过 | 治理概览、平台配置保存/恢复、组织树与组织节点创建、学期创建/编辑、课程模板创建/编辑、开课创建/编辑、共同管理学院选择、用户列表/详情、开课详情、权限解释、审计日志均有 MCP 截图。教学班创建实际位于教师课程工作台，已由教师端补证。 |
| 教师 | 通过 | 教学工作台、课程工作区、教学班创建、成员添加/CSV 导入/停用/恢复、公告创建、资源上传下载、题库新增简答题和结构化题型、题库编辑归档、判题环境新增配置、判题环境编辑归档、讨论创建/回复/锁定、作业创建发布、草稿编辑、发布后编辑规则阻断、关闭、提交批改、成绩册发布、实验创建编辑发布关闭、实验报告评阅发布、通知全部已读均有 MCP 证据。 |
| 学生 | 通过 | 学习中心、课程、讨论详情与回复、作业详情、结构化题提交、文件题附件上传下载、WebIDE、历史恢复、样例自测、正式提交、提交详情、成绩、实验终端、实验会话启停、实验报告提交、发布后教师评语回查、通知单条已读均有 MCP 证据。 |
| 开课助教 | 通过 | 授权课程与管理员禁止边界通过；未授权或不存在课程上下文已收敛为课程不可访问态，见 P2-R2-002/P2-R2-003 第三阶段回归。 |
| 班级助教 | 通过 | 登录、班级成员页、管理员禁止边界有 MCP 截图。 |
| 缺档案用户 | 通过 | 以第一轮和第二轮上下文准备的缺档案账号证明 `/profile-required` 可达，证据继承第二轮前置数据和截图 `053-profile-required-profileless-ta.png`。 |

## 8. 公共与认证验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| COMMON-001 | 通过 | `001-login-page.png` | 未登录入口可进入登录页。 |
| COMMON-002 | 通过 | `001-login-page.png` | 登录页显示平台说明、用户名/密码表单、显示密码按钮和公告。 |
| COMMON-003 | 通过 | `116-r2-repair-login-empty-submit.png` | 空表单提交后停留登录页，表单顶部显示“请输入用户名和密码”，用户名和密码输入框均进入 invalid 状态，见 P2-R2-001。 |
| COMMON-004 | 通过 | MCP 彩排 1 匿名 `/admin` 重定向记录 | 未登录访问受限页会跳转登录。 |
| COMMON-005 | 通过 | `119-r2-common-global-search-results.png`、`120-r2-common-global-search-gradebook.png` | 顶栏搜索输入“成绩”后显示“全部成绩 / 教师端”结果，并可跳转到 `/teacher/grading/gradebook`。 |
| COMMON-006 | 通过 | `043-student-notifications.png`、`044-me-notifications.png`、`123/124`、`126/127` | 学生、教师通知页可见，通知列表真实渲染；教师全部已读和学生单条已读均完成页面状态变更。 |
| COMMON-007 | 通过 | `121-r2-common-user-menu.png`、`122-r2-common-logout-login-page.png` | 用户菜单显示教师身份、用户名和退出登录入口；点击退出登录后回到 `/login`。 |
| AUTH-001 | 通过 | `002-admin-dashboard.png`、`056-r2-rehearsal1-admin-dashboard.png`、`092-r2-rehearsal3-admin-dashboard.png` | 管理员登录进入治理首页。 |
| AUTH-002 | 通过 | `013/014-teacher-dashboard.png`、`060-r2-rehearsal1-teacher-dashboard.png`、`096-r2-rehearsal3-teacher-dashboard.png` | 教师登录进入教学工作台。 |
| AUTH-003 | 通过 | `032/033-student-dashboard.png`、`064-r2-rehearsal1-student-dashboard.png`、`102-r2-rehearsal3-student-dashboard.png` | 学生登录进入学习中心。 |
| AUTH-004 | 通过 | `045-offering-ta-dashboard.png`、`047-class-ta-dashboard.png`、`071/074/109/113` 彩排截图 | 开课助教和班级助教均可登录教师端。 |
| AUTH-005 | 通过 | `053-profile-required-profileless-ta.png` | 缺档案用户可进入 profile-required。 |
| AUTH-006 | 通过 | `049-student-forbidden-admin.png`、`050-teacher-forbidden-admin.png`、`070/073/076/108/112/114` 彩排截图 | 非授权工作区进入 `/unauthorized`。 |
| AUTH-007 | 通过 | `044-me-notifications.png`、`069-r2-rehearsal1-me-notifications.png`、`107-r2-rehearsal3-me-notifications.png` | `/me/notifications` 可达。 |

## 9. 学生闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| STUDENT-001~006 | 通过 | `032`-`038`、`064`-`065`、`086`-`087`、`102`-`103`、`131-r2-student-discussion-reply-posted.png`、`student-discussion-reply-network.txt` | 学生首页、课程、讨论、作业列表、作业详情和 WebIDE 页面可达；学生进入教师新建讨论 `36` 后可见教师回复并成功发布回复，接口 `POST /api/v1/me/discussions/36/replies` 返回 201。 |
| STUDENT-007~009 | 通过 | `140-r2-student-structured-assignment-filled.png`、`141-r2-student-structured-submission-detail.png`、`student-structured-submission-network.txt` | 学生提交作业 `259`，单选 A、多选 A/B、填空“下载”均在提交详情回显；接口 `POST /api/v1/me/assignments/259/submissions` 返回 201，生成提交 `55`。 |
| STUDENT-010 | 通过 | `037/038-student-assignment-detail.png`、`040-student-submission-detail.png`、`141-r2-student-structured-submission-detail.png` | 简答/结构化提交详情可达；本轮结构化提交详情和既有简答提交详情均可显示。 |
| STUDENT-011 | 通过 | `140-r2-student-structured-assignment-filled.png`、`141-r2-student-structured-submission-detail.png`、`student-structured-upload-sha256.txt` | 文件题附件上传后提交详情可见；下载文件与源文件 SHA256 一致。 |
| STUDENT-012~014 | 通过 | `039-student-webide.png`、`054-student-webide-sample-run.png`、`066-r2-rehearsal1-student-webide-run.png`、`104-r2-rehearsal3-student-webide-run.png`、`158-r2-student-webide-before-save.png`、`159-r2-student-webide-saved-probe.png`、`160-r2-student-webide-restored.png`、`161-r2-student-webide-restored-run-accepted.png`、`student-webide-save-restore-network.txt` | WebIDE 可打开；历史面板可查看 v6 预览，恢复后生成 v8“恢复 v6”，编辑器回到原始两行求和代码，恢复后运行自测显示 `ACCEPTED` / 通过。 |
| STUDENT-015~016 | 通过 | `040-student-submission-detail.png`、`141-r2-student-structured-submission-detail.png`、`147-r2-student-submission-55-feedback-visible.png`、`162-r2-student-programming-submit-accepted.png`、`164-r2-student-programming-polling-assignment-before-submit.png`、`165-r2-student-programming-polling-submit-accepted.png`、`student-programming-submit-56-network.txt`、`student-programming-polling-submit-57-network.txt`、`07-just-e2e-real.log` | 编程题正式提交已通过真实页面生成提交 `56`，刷新同一详情页后显示 `ACCEPTED / 100 分`；P1-R2-006 修复后，以临时作业 `260` 生成提交 `57`，提交详情页无需手动刷新，网络摘要显示 3 次 `judge-jobs` 轮询后自动刷新提交详情并显示 `ACCEPTED / 100 分`。 |
| STUDENT-017~018 | 通过 | `041-student-grades.png`、`043-student-notifications.png`、`106/107` 彩排截图、`126/127`、`146-r2-student-gradebook-259-published.png` | 成绩和通知入口可达；学生成绩页显示作业 `259` 为 `23 / 23`、`已发布`、提交 `55`；学生端对 `MCP-R2-20260610-143804` 公告通知执行单条标记已读后未读徽标 32 -> 31，目标行按钮消失。 |
| STUDENT-019~020 | 通过 | `042-student-labs.png`、`055-student-lab-terminal-echo.png`、`105-r2-rehearsal3-student-labs.png`、`155-r2-student-lab-session-running-before-stop.png`、`156-r2-student-lab-session-stopped.png`、`157-r2-student-lab-session-started.png`、`student-lab-session-stop-start-network.txt` | 实验列表和 Web 终端可演示，终端输出包含 `round2-terminal`；终端实验 `16` 停止后页面显示“未启动”，随后重新启动显示“运行中”，网络摘要包含 `POST /sessions` 201 和 current session 200。 |
| STUDENT-021 | 通过 | `149-r2-student-lab-report-filled-attachment.png`、`150-r2-student-lab-report-draft-saved.png`、`151-r2-student-lab-report-submitted.png`、`154-r2-student-lab-report-feedback-visible.png`、`student-lab-report-submit-network.txt`、`student-lab-report-attachment-sha256.txt`、`student-lab-report-feedback-network.txt` | 学生选择实验 `52`，填写 Markdown 报告、上传附件、保存草稿、确认正式提交；教师评阅发布后学生端显示 `已发布` 与教师评语，附件下载 SHA256 一致。 |

## 10. 教师闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TEACHER-001~003 | 通过 | `013`-`016`、`060`-`061`、`096`-`097`、`172-r2-teacher-teaching-class-created.png`、`teacher-teaching-class-create-network.txt` | 教师首页、课程列表、课程工作区和上下文导航可达；教师在新开课 `32` 的课程工作台创建教学班 `MCP-R2-06102037 教学班`，接口 `POST /api/v1/teacher/course-offerings/32/classes` 返回 201，随后列表刷新为 200，控制台 0 errors / 0 warnings。 |
| TEACHER-004 | 通过 | `016/017-teacher-members.png`、`075/113-r2-rehearsal*-class-ta-members.png`、`173-r2-teacher-members-add-import-visible.png`、`174-r2-teacher-member-status-dropped.png`、`175-r2-teacher-member-status-restored.png`、`teacher-members-add-import-status-network.txt`、`teacher-members-add-import-status-console.txt` | 成员页可达；在开课 `32` 中通过 UI 添加学生 `mcp-r2-0610210555-member-add-fixed`，通过 CSV 导入 `mcp-r2-0610205203-member-import`，并对导入成员执行停用和恢复；网络摘要显示 `POST /members/batch` 200、`POST /members/import` 200、两次 `PATCH /members/454/status` 200，控制台 0 errors / 0 warnings。 |
| TEACHER-005 | 通过 | `017/018`、`125-r2-teacher-announcement-created.png`、`teacher-announcement-create-network.txt` | 公告页可达；已新建 `MCP-R2-20260610-143804` 公告，列表可见，接口 `POST /api/v1/teacher/course-offerings/2/announcements` 返回 201。 |
| TEACHER-006 | 通过 | `018-teacher-resources.png`、`082-r2-rehearsal2-teacher-resources.png`、`134-r2-teacher-resource-uploaded.png`、`teacher-resource-upload-network.txt`、`teacher-resource-upload-sha256.txt` | 资源页面可达；教师上传 `MCP-R2-20260610-1553 教师资源补证` Markdown 文件后列表显示标题、文件名、说明、大小和下载入口，接口 `POST /api/v1/teacher/course-offerings/2/resources` 返回 201；下载文件与源文件 SHA256 一致。 |
| TEACHER-007~008 | 通过 | `019`-`021`、`128`-`133`、`teacher-discussion-create-network.txt`、`teacher-discussion-reply-network.txt`、`teacher-discussion-lock-network.txt` | 讨论列表和详情页面可达；教师新建讨论 `MCP-R2-20260610-145754 教师讨论补证` 后列表可见，教师回复写入后详情可见，学生回复也在教师详情页可见；锁定后列表显示“已锁定”，详情页发布按钮禁用。 |
| TEACHER-009 | 通过 | `021/022/023-teacher-question-bank-course.png`、`098-r2-rehearsal3-teacher-question-bank.png`、`135-r2-teacher-question-bank-created.png`、`137-r2-teacher-question-bank-structured-types-created.png`、`182-r2-teacher-question-bank-edited-archived.png`、`teacher-question-bank-create-network.txt`、`teacher-question-bank-structured-types-network.txt`、`teacher-question-bank-edit-archive-network.txt`、`teacher-question-bank-edit-archive-console.txt` | 题库页面可达；教师创建 `MCP-R2-20260610-1605 简答题补证` 后列表第一行显示新题；随后新增结构化题型用于作业。开课 `32` 中创建题目 `75`，编辑为 `MCP-R2-06102249 题库编辑归档补证-EDIT`，`PUT /api/v1/teacher/question-bank/questions/75` 返回 200；归档后默认列表为空，包含归档视图可回看该题。 |
| TEACHER-010 | 通过 | `022-teacher-judge-envs.png`、`136-r2-teacher-judge-environment-created.png`、`183-r2-teacher-judge-environment-edited-archived.png`、`teacher-judge-environment-create-network.txt`、`teacher-judge-environment-edit-archive-network.txt`、`teacher-judge-environment-edit-archive-console.txt` | 判题环境页面可达；教师创建 `MCP-R2-20260610-1611 Python3 判题环境补证` 后列表显示新配置。开课 `32` 中创建配置 `40`，编辑为 `MCP-R2-06102255 Python 判题环境补证-EDIT`，`PUT /api/v1/teacher/judge-environment-profiles/40` 返回 200；归档后默认列表为空，包含归档视图显示“已归档”。 |
| TEACHER-011~013 | 通过 | `023`-`026`、`083/099` 彩排截图、`138-r2-teacher-assignment-create-filled.png`、`139-r2-teacher-assignment-published.png`、`176-r2-teacher-assignment-draft-created.png`、`177-r2-teacher-assignment-published-before-edit.png`、`178-r2-teacher-assignment-published-edit-blocked.png`、`179-r2-teacher-assignment-closed.png`、`180-r2-teacher-assignment-draft-edit-form.png`、`181-r2-teacher-assignment-draft-edited.png`、`teacher-assignment-create-network.txt`、`teacher-assignment-publish-network.txt`、`teacher-assignment-edit-close-network.txt`、`teacher-assignment-draft-edit-network.txt` | 作业列表、创建表单、编辑页可达；教师创建结构化作业 `259` 并发布成功。开课 `32` 中创建作业 `261`、发布后修复编辑规则并关闭成功；另创建草稿作业 `262`，编辑标题为 `MCP-R2-06102203 草稿编辑补证-EDIT` 后 `PUT /api/v1/teacher/assignments/262` 返回 200。当前稳定 API 和页面入口未提供作业撤回/重新发布。 |
| TEACHER-014~016 | 通过 | `026`-`029`、`062/063/084/085/100` 彩排截图、`142-r2-teacher-submission-55-before-grade.png`、`143-r2-teacher-submission-55-after-grade.png`、`144-r2-teacher-gradebook-259-before-publish.png`、`145-r2-teacher-gradebook-259-after-publish.png`、`teacher-submission-55-grade-network.txt`、`teacher-gradebook-259-publish-network.txt` | 提交列表、提交详情和成绩册页面可达；教师查看提交 `55`，为文件题保存人工分 `8` 和反馈，成绩册发布作业 `259` 后学生端可见总分与反馈。 |
| TEACHER-017~018 | 通过 | `029/030-teacher-question-bank-global.png`、`030/031-teacher-labs.png`、`086/101` 彩排截图、`148-r2-teacher-report-lab-created-published.png`、`152-r2-teacher-lab-report-detail-before-review.png`、`153-r2-teacher-lab-report-reviewed-published.png`、`184-r2-teacher-lab-edited-closed.png`、`teacher-report-lab-create-publish-network.txt`、`teacher-lab-report-review-publish-network.txt`、`teacher-lab-edit-close-network.txt`、`teacher-lab-edit-close-console.txt` | 全局题库和实验页可达；教师创建并发布报告型实验 `52`，查看学生报告 `21`、保存教师评语并发布评阅，相关接口返回 201/200。开课 `32` / 教学班 `234` 中创建实验 `53`，编辑为 `MCP-R2-06102302 实验编辑关闭补证-EDIT`，`PUT /api/v1/teacher/labs/53` 返回 200，发布和关闭接口均返回 200，最终列表显示“已关闭”。 |
| TEACHER-019 | 通过 | `031/032-teacher-notifications.png`、`123/124`、`teacher-notifications-after-network.txt` | 教师通知页可达；点击“全部已读”后顶部未读徽标从 9 清零，接口 `POST /api/v1/me/notifications/read-all` 返回 200。 |

## 11. 管理员闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| ADMIN-001 | 通过 | `002-admin-dashboard.png`、`056`、`092` | 治理首页可达。 |
| ADMIN-002 | 通过 | `003-admin-platform-config.png`、`077`、`166-r2-admin-platform-config-saved-marker.png`、`167-r2-admin-platform-config-restored.png`、`admin-platform-config-save-restore-network.txt` | 平台配置可查看；管理员将页脚文字临时保存为 `MCP-R2-ADMIN-0610` 标记值后恢复原值，网络摘要显示 `GET 200 -> PUT 200 -> GET 200 -> PUT 200 -> GET 200`，控制台 0 errors / 0 warnings。 |
| ADMIN-003 | 通过 | `004-admin-org-units.png`、`093`、`168-r2-admin-org-unit-created.png`、`admin-org-unit-create-network.txt` | 组织树可查看；管理员在学校节点下创建 `MCP-R2-06101946 学院`，接口 `POST /api/v1/admin/org-units` 返回 201，随后 `GET /tree` 返回 200 并在树中显示新学院。当前稳定接口只列出创建接口，未提供组织节点编辑 API 或页面编辑入口。 |
| ADMIN-004~005 | 通过 | `005/006/013-admin-user-detail*.png`、`078/094` | 用户列表、搜索和用户详情可达。 |
| ADMIN-006 | 通过 | `007-admin-academic-terms.png`、`169-r2-admin-academic-term-created-edited.png`、`admin-academic-term-create-edit-network.txt` | 管理员创建 `MCP-R2-06101952 学期` 后编辑为 `MCP-R2-06101952 学期-EDIT`；网络摘要显示 `POST /api/v1/admin/academic-terms` 201、`PUT /api/v1/admin/academic-terms/29` 200，随后列表刷新为 200。 |
| ADMIN-007 | 通过 | `008-admin-course-catalogs.png`、`170-r2-admin-course-catalog-created-edited.png`、`admin-course-catalog-create-edit-network.txt` | 管理员创建 `MCP-R2-06102000 课程模板` 后编辑为 `MCP-R2-06102000 课程模板-EDIT`；网络摘要显示 `POST /api/v1/admin/course-catalogs` 201、`PUT /api/v1/admin/course-catalogs/26` 200，随后列表刷新为 200，控制台 0 errors / 0 warnings。 |
| ADMIN-008 | 通过 | `009-admin-course-offerings.png`、`171-r2-admin-course-offering-created-edited.png`、`admin-course-offering-create-edit-network.txt`、`admin-course-offering-create-edit-console.txt` | 管理员基于课程模板 `MCP-R2-06102000 课程模板-EDIT` 创建开课 `MCP-R2-06102015 开课实例`，主开课学院自动回填 `MCP-R2-06101946 学院`，共同管理学院选择 `E2EMQ56QUX7DG2EVPORG-共管学院`；MCP 创建阶段网络输出显示 `POST /api/v1/admin/course-offerings` 201，响应 ID 为 `32`。随后在详情页将名称编辑为 `MCP-R2-06102015 开课实例-EDIT`、容量改为 `60`，网络摘要显示 `GET 200 -> PUT 200 -> GET 200`，控制台 0 errors / 0 warnings。教学班创建实际位于教师课程工作台，见 TEACHER-001~003。 |
| ADMIN-009 | 通过 | `010-admin-course-offering-detail.png`、`079` | 开课详情可达。 |
| ADMIN-010~011 | 通过 | `011-admin-auth-explain.png`、`012-admin-audit-logs.png`、`058/059/080/095` | 权限解释和审计日志可达。 |

## 12. 助教与权限边界验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TA-001~002 | 通过 | `045/046`、`071/072`、`090/109` | 开课助教可登录并进入授权开课。 |
| TA-003 | 通过 | `117-r2-repair-offering-ta-unauthorized-course.png` | 未授权开课 ID `5` 显示“无法访问该课程”，不再显示课程快捷操作入口，见 P2-R2-002。 |
| TA-004~005 | 通过 | `047/048`、`074/075`、`091/113` | 班级助教可登录并进入班级成员页。 |
| TA-006~009 | 通过 | `049/050`、`070/073/076/108/112/114` | 学生、教师、助教访问非授权工作区均显示 `/unauthorized`。 |
| TA-010 | 通过 | `118-r2-repair-offering-ta-invalid-course.png` | 不存在课程 ID `999999` 显示“无法访问该课程”，不再停留教学班加载态或展示快捷操作，见 P2-R2-003。 |

## 13. 运行时能力验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| RUNTIME-001 | 通过 | `just verify`、`just verify-full`、`just e2e-real` 日志 | 后端测试和真实 E2E 证明提交、成绩、审计等核心数据链路可用；本轮未单独导出 SQL 摘要。 |
| RUNTIME-002 | 通过 | `just e2e-real` 日志、`134-r2-teacher-resource-uploaded.png`、`teacher-resource-upload-sha256.txt`、`student-structured-upload-sha256.txt`、`student-lab-report-attachment-sha256.txt`、`teacher-lab-report-attachment-sha256.txt` | 真实 E2E 覆盖资源上传下载；本轮 MCP 又补充教师资源、学生文件题附件、学生实验报告附件和教师端报告附件下载校验，下载文件与源文件 SHA256 一致。 |
| RUNTIME-003 | 通过 | `just healthcheck-strict`、`just e2e-real` 日志 | RabbitMQ 依赖健康，真实 E2E 判题链路通过。 |
| RUNTIME-004 | 通过 | `just healthcheck-strict`、`just e2e-real` 日志 | Redis 依赖健康，限流/登录真实 E2E 通过。 |
| RUNTIME-005 | 通过 | `123/124`、`126/127`、`teacher-notifications-after-network.txt`、`student-notifications-after-mark-read-network.txt` | 通知页、未读入口、SSE/轮询请求、教师全部已读和学生单条已读可用；网络摘要包含 `GET /api/v1/me/notifications/stream`、`GET /unread-count`、`POST /read-all`、`POST /{id}/read` 的成功记录。 |
| RUNTIME-006 | 通过 | `054`、`066`、`104`、`161`、`162`、`164`、`165` WebIDE/提交截图，`student-webide-save-restore-network.txt`、`student-programming-submit-56-network.txt`、`student-programming-polling-submit-57-network.txt`、`07-just-e2e-real.log` | go-judge / fake judge 主线返回 `ACCEPTED`；P1-R2-006 修复后，学生提交详情页对运行中判题任务执行轮询，并在终态后自动刷新提交详情。 |
| RUNTIME-007 | 通过 | `055-student-lab-terminal-echo.png`、`155`、`156`、`157`、`student-lab-session-stop-start-network.txt` | 实验 Web 终端已连接并输出 `round2-terminal`；实验会话停止和重新启动均可见。 |
| RUNTIME-008 | 通过 | `012`、`059`、`080` 审计日志截图 | 审计日志页面可查。 |

## 14. 文档一致性验证

`just verify`、`just verify-full` 和单独 `cd docs && npm run docs:build` 均通过。第二轮验收报告、功能清单和彩排记录写入 `docs/06-testing-and-ops/artifacts/` 下独立 `round2` 路径，未覆盖第一轮产物。

## 15. 前端质量与响应式验证

| 视口 | 状态 | 证据 | 说明 |
| --- | --- | --- | --- |
| `1280x800` | 通过 | `051-nfr-1280-student-assignments.png` | 学生作业列表在窄桌面宽度可用。 |
| `1440x900` | 通过 | `052-nfr-1440-admin-users.png` | 管理员用户表在标准桌面宽度可用。 |
| `390x844` | 通过 | `053-nfr-390-student-webide.png` | WebIDE 移动窄屏基础可见。 |
| 全站关键页 | 通过 | `product-full-verification-round2-evidence/runtime/full-route-console-network-scan-20260610.md` | Playwright MCP 覆盖 55 个公共/管理员/教师/学生/助教 route/角色组合；复核后无意外 console error、无意外业务 4xx/5xx、无未解释 request failure。负例权限页均为预期页面行为。 |
| 权限/错误态 | 通过 | `116`、`117`、`118` | 登录空表单、未授权课程和不存在课程错误态均有可见说明，且未授权/不存在课程不再展示后续快捷入口。 |

## 16. 三次完整演示彩排记录摘要

| 彩排 | 状态 | 证据 | 说明 |
| --- | --- | --- | --- |
| 彩排 1 | 通过 | `056`-`076` | 管理员、教师、学生、WebIDE、学生权限、开课助教、班级助教主线均通过。 |
| 彩排 2 | 通过 | `077`-`091` | 管理员/教师段初次 MCP 调用超时，但已生成页面截图；随后补齐教师实验、学生和助教短段。 |
| 彩排 3 | 通过 | `092`-`114`、`116`-`118` | 管理员、教师、学生、助教主线通过；彩排中发现的 P2 已在第三阶段补漏回归。 |

三次彩排主线均已执行并记录；第三阶段已补齐彩排后发现的 P1/P2 缺陷、写入动作证据和全站 console/network 归因，总体验收结论更新为 `通过`。

## 17. 缺陷详情

### P2-R2-001 登录空表单缺少新增可见错误说明

- 严重级别：P2
- 功能清单编号：COMMON-003
- 模块：web/auth
- 角色：无登录用户
- 页面或对象：`/login`
- 操作步骤：打开登录页，不输入用户名和密码，点击“立即登录”。
- 实际表现：页面仍停留登录页，截图中只保留字段标签和占位提示，没有新增字段级或全局错误说明。
- 期望表现：字段旁或表单顶部显示“请输入用户名 / 请输入密码”等可理解反馈。
- 影响说明：不会阻断登录主线，但降低错误态可理解性。
- 证据：
  - MCP 截图：`product-full-verification-round2-screenshots/115-r2-login-empty-submit.png`
  - MCP 页面观察：点击后仍为 `/login`。
  - 第三阶段回归截图：`product-full-verification-round2-screenshots/116-r2-repair-login-empty-submit.png`
  - 第三阶段 MCP 页面观察：点击“立即登录”后显示 `role=alert` 的“请输入用户名和密码”，用户名和密码输入框均为 invalid。
  - 辅助证据：`web/src/tests/unit/auth/login-form.test.tsx` 覆盖空表单应用内校验。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复说明：登录表单移除原生 required 阻断并启用 `noValidate`，由应用内校验显示统一错误区和 `aria-invalid`。
- 修复状态：已回归

### P2-R2-002 未授权开课上下文仍展示快捷入口

- 严重级别：P2
- 功能清单编号：TA-003、NFR-005
- 模块：web/teacher course workspace
- 角色：开课助教
- 页面或对象：`/teacher/courses/5`
- 操作步骤：以开课助教登录，直接打开未授权开课 ID `5`。
- 实际表现：页面显示“数据加载失败 / 当前用户无权查看教学班”，但仍显示“发布全课公告”“上传课程资源”“管理本课作业”等快捷入口。
- 期望表现：未授权上下文应进入统一拒绝态，隐藏或禁用后续动作入口。
- 影响说明：不构成越权访问，但会误导用户继续点击必然失败的动作。
- 证据：
  - MCP 截图：`product-full-verification-round2-screenshots/111-r2-rehearsal3-offering-ta-unauthorized-course.png`
  - MCP 页面观察：拒绝文案和快捷入口同时存在。
  - 第三阶段回归截图：`product-full-verification-round2-screenshots/117-r2-repair-offering-ta-unauthorized-course.png`
  - 第三阶段 MCP 页面观察：`/teacher/courses/5` 显示“无法访问该课程”和“课程不存在，或当前账号没有该课程的访问权限。”，不再显示“快捷操作”“发布全课公告”“上传课程资源”“管理本课作业”。
  - 辅助证据：`web/src/tests/unit/course/teacher-course-dashboard-page.test.tsx` 覆盖未授权课程隐藏后续动作。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复说明：课程工作区先以 `useMyCoursesQuery()` 确认当前课程在教师/助教授权范围内，未命中时渲染页面级不可访问态并跳过后续动作区。
- 修复状态：已回归

### P2-R2-003 不存在课程 ID 页面停留加载态并展示快捷入口

- 严重级别：P2
- 功能清单编号：TA-003、NFR-005
- 模块：web/teacher course workspace
- 角色：开课助教
- 页面或对象：`/teacher/courses/999999`
- 操作步骤：以开课助教登录，直接打开不存在课程 ID `999999`。
- 实际表现：页面停留“教学班 加载中...”，同时显示“发布全课公告”“上传课程资源”“管理本课作业”等快捷入口。
- 期望表现：不存在或不可访问对象应显示清晰的不存在/无权状态，并隐藏动作入口。
- 影响说明：不影响正常授权课程主线，但影响错误态和演示故障预案可信度。
- 证据：
  - MCP 截图：`product-full-verification-round2-screenshots/110-r2-rehearsal3-offering-ta-invalid-course.png`
  - MCP 页面观察：加载态长时间未收敛，动作入口仍存在。
  - 第三阶段回归截图：`product-full-verification-round2-screenshots/118-r2-repair-offering-ta-invalid-course.png`
  - 第三阶段 MCP 页面观察：`/teacher/courses/999999` 显示“无法访问该课程”和“课程不存在，或当前账号没有该课程的访问权限。”，不再停留“加载中...”或显示快捷操作。
  - 辅助证据：`web/src/tests/unit/course/teacher-course-dashboard-page.test.tsx` 覆盖不存在课程 ID 不进入教学班加载态。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复说明：课程工作区在课程清单已加载但找不到当前 `offeringId` 时直接渲染不可访问态，并仅在课程上下文确认后启用教学班查询。
- 修复状态：已回归

### P1-R2-004 实验报告评阅发布后学生端未显示教师评语

- 严重级别：P1
- 功能清单编号：STUDENT-021、TEACHER-018
- 模块：web/lab
- 角色：学生、教师
- 页面或对象：`/student/labs?classId=2&offeringId=2`
- 操作步骤：教师创建并发布报告型实验 `52`；学生提交报告 `21`；教师保存评语并发布评阅；学生重新打开同一实验报告。
- 实际表现：后端 `GET /api/v1/me/labs/52/report` 返回 `teacherCommentText`，但学生端页面只显示 `已发布`、报告正文和附件，没有显示教师评语。
- 期望表现：评阅结果发布后，学生端应显示教师评语或批注，形成“提交 -> 教师反馈 -> 学生回查”的完整闭环。
- 影响说明：会破坏实验报告演示主线中的反馈回查环节，属于可见反馈缺失。
- 证据：
  - 后端响应体：`product-full-verification-round2-evidence/runtime/student-lab-report-feedback-response-body.json`，包含 `teacherCommentText`。
  - 修复前页面观察：学生端页面文本不包含“教师评语”和 `MCP-R2 教师评阅补证`。
  - 修复后回归截图：`product-full-verification-round2-screenshots/154-r2-student-lab-report-feedback-visible.png`
  - 修复后网络摘要：`product-full-verification-round2-evidence/runtime/student-lab-report-feedback-network.txt`
  - 辅助单测：`web/src/tests/unit/lab/student-labs-page.test.tsx` 覆盖发布后显示教师反馈。
- 是否阻塞演示彩排：是，未修复时会阻断实验报告反馈演示。
- 是否阻塞后续功能验证：否，已回归。
- 修复说明：学生实验报告页面在报告状态为 `PUBLISHED` 且后端返回教师评语或批注时，显示“教师评语”反馈区。
- 修复状态：已回归

### P2-R2-005 报告型实验误请求运行时 current session 产生 400 网络噪音

- 严重级别：P2
- 功能清单编号：STUDENT-021、NFR-004
- 模块：web/lab
- 角色：学生
- 页面或对象：`/student/labs?classId=2&offeringId=2`
- 操作步骤：学生打开实验页并选择报告型实验 `52`。
- 实际表现：页面显示教师反馈的同时仍请求 `GET /api/v1/me/labs/52/sessions/current`，该接口对报告型实验返回 400。
- 期望表现：报告型实验只加载报告正文、附件和教师反馈，不应查询终端实验的当前运行时会话。
- 影响说明：不阻断实验报告反馈显示，但会污染 console/network 归因文件，降低演示回归证据可信度。
- 证据：
  - 修复前 MCP 网络观察：选择报告型实验后出现 `GET /api/v1/me/labs/52/sessions/current` 400。
  - 辅助单测：`web/src/tests/unit/lab/student-labs-page.test.tsx` 覆盖报告型实验不查询 runtime session。
  - 修复后 MCP 网络观察：选择同一报告型实验后实验相关请求只有 `GET /api/v1/me/labs/52/report` 200，不再出现 `/api/v1/me/labs/52/sessions/current` 请求。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否，已回归。
- 修复说明：学生实验页先从实验清单判断选中实验类型，只有 `TERMINAL` 实验才启用 `useMyCurrentLabSessionQuery`；报告型实验传入 `0` 触发 hook 的 `enabled: !!labId` 禁用查询。
- 修复状态：已回归

### P1-R2-006 编程正式提交后学生提交详情页不自动刷新判题终态

- 严重级别：P1
- 功能清单编号：STUDENT-015、RUNTIME-006
- 模块：web/student submissions、web/judge query
- 角色：学生
- 页面或对象：`/student/assignments/7`、`/student/submissions/56?assignmentId=7`
- 操作步骤：
  1. 学生打开 WebIDE `/student/assignments/7/workspace/11`。
  2. 通过历史面板恢复 v6，确认代码为两行求和程序，并运行自测得到 `ACCEPTED`。
  3. 返回作业详情 `/student/assignments/7`，点击“提交答案”。
  4. 页面跳转到 `/student/submissions/56?assignmentId=7`，等待 30 秒以上。
- 实际表现：提交详情页持续显示“运行中 / 未知状态 / 0 分 / 暂无输出”，期间没有继续请求 `/api/v1/me/submissions/56/judge-jobs`；手动刷新同一 URL 后显示“已完成 / 通过 / 17 ms / 3 MB”，答案反馈为 `ACCEPTED，2/2 个测试点通过，得分 100/100`。
- 期望表现：提交后进入详情页时应持续轮询运行中的判题任务，判题终态到达后刷新提交详情和判题结果，无需人工刷新即可看到 `ACCEPTED / 100 分`。
- 影响说明：正式提交是编程题演示主线；如果结果页停留“运行中”，演示者必须人工刷新才能证明判题通过，足以造成主线卡顿。
- 证据：
  - 提交后未刷新截图：MCP 快照显示提交 `56` 页面长期停留“运行中”。
  - 刷新后终态截图：`product-full-verification-round2-screenshots/162-r2-student-programming-submit-accepted.png`
  - 网络摘要：`product-full-verification-round2-evidence/runtime/student-programming-submit-56-network.txt`，首次详情页只请求一次 `GET /api/v1/me/submissions/56/judge-jobs`；刷新后再次请求并显示终态。
  - 控制台摘要：`product-full-verification-round2-evidence/runtime/student-programming-submit-56-console.txt`，无新增 warning/error。
- 修复说明：
  - `web/src/features/judge/hooks/use-judge-query.ts` 支持向学生 judge jobs 查询传入 `refetchInterval`。
  - `web/src/app/(student)/student/submissions/[submissionId]/page.tsx` 在存在 `PENDING` / `RUNNING` 判题任务时每 3 秒轮询；检测到判题任务从运行态进入终态后刷新提交详情，以同步答案分数和反馈。
  - `web/src/tests/unit/submission/student-submission-detail-page.test.tsx` 增加单测，覆盖运行中判题任务触发轮询、终态后停止轮询并刷新提交详情。
- 修复后回归：
  - 定向单测：`npm test -- src/tests/unit/submission/student-submission-detail-page.test.tsx`，`1 passed / 5 tests passed`。
  - MCP 页面：临时编程作业 `260`，学生提交 `57`，提交前截图 `164-r2-student-programming-polling-assignment-before-submit.png`，自动刷新终态截图 `165-r2-student-programming-polling-submit-accepted.png`。
  - MCP 网络：`product-full-verification-round2-evidence/runtime/student-programming-polling-submit-57-network.txt` 包含提交后 3 次 `GET /api/v1/me/submissions/57/judge-jobs`，随后自动请求 `GET /api/v1/me/submissions/57` 并在页面显示 `ACCEPTED / 100 分`。
  - MCP 控制台：`product-full-verification-round2-evidence/runtime/student-programming-polling-submit-57-console.txt`，warning/error 为 0。
- 是否阻塞演示彩排：是，影响编程题正式提交结果展示。
- 是否阻塞后续功能验证：否，后端判题和刷新后终态已证明可用。
- 修复状态：已回归

### P2-R2-007 添加课程成员成功后弹窗不关闭且列表不刷新

- 严重级别：P2
- 功能清单编号：TEACHER-004
- 模块：web/teacher course members、web/query keys
- 角色：教师
- 页面或对象：`/teacher/courses/32/members`
- 操作步骤：以开课 `32` 的授课教师打开成员管理页，点击“添加成员”，填写用户 ID `391`，选择 `MCP-R2-06102037 教学班` 后点击“添加”。
- 实际表现：后端 `POST /api/v1/teacher/course-offerings/32/members/batch` 返回 `successCount=1, failCount=0`，但添加成员弹窗仍保持打开；成员列表未自动刷新，继续键入搜索条件会误写回弹窗的用户 ID 输入框。
- 期望表现：添加成员成功后关闭弹窗并刷新当前成员列表，让教师立即看到新增成员。
- 影响说明：不造成后端写入失败，但会误导教师认为添加未生效，并影响后续批量导入、状态变更等连续操作。
- 证据：
  - MCP 网络观察：`POST /api/v1/teacher/course-offerings/32/members/batch` 200，响应体 `successCount=1, failCount=0`。
  - MCP 页面观察：提交成功后弹窗仍显示，用户 ID 输入框继续保留焦点。
- 修复说明：
  - `web/src/app/(teacher)/teacher/courses/[offeringId]/members/page.tsx` 在添加成员 mutation 成功后关闭弹窗并主动刷新当前列表。
  - `web/src/shared/api/query-keys.ts` 修正课程列表类 query key，省略筛选参数时返回前缀 key，确保成员、公告、资源和讨论列表 mutation 能失效带筛选参数的查询。
  - `web/src/tests/unit/course/teacher-members-page.test.tsx` 增加“添加成功后关闭弹窗并刷新列表”单测；`web/src/tests/unit/api/query-keys.contract.test.ts` 增加课程列表 prefix key 契约。
- 修复后回归：
  - MCP 页面：使用临时学生 `mcp-r2-0610210555-member-add-fixed` 重新执行添加成员，弹窗关闭，列表自动显示新增学生。
  - MCP 补证：CSV 导入 `mcp-r2-0610205203-member-import`，随后停用和恢复该导入成员，列表状态依次显示“已停用”和“已激活”。
  - MCP 截图：`product-full-verification-round2-screenshots/173-r2-teacher-members-add-import-visible.png`、`product-full-verification-round2-screenshots/174-r2-teacher-member-status-dropped.png`、`product-full-verification-round2-screenshots/175-r2-teacher-member-status-restored.png`
  - MCP 网络：`product-full-verification-round2-evidence/runtime/teacher-members-add-import-status-network.txt` 包含 `POST /members/batch` 200、`POST /members/import` 200、两次 `PATCH /members/454/status` 200。
  - MCP 控制台：`product-full-verification-round2-evidence/runtime/teacher-members-add-import-status-console.txt`，warning/error 为 0。
  - 定向单测：`npm test -- src/tests/unit/course/teacher-members-page.test.tsx`，`1 file / 7 tests passed`；`npm test -- src/tests/unit/api/query-keys.contract.test.ts`，`1 file / 6 tests passed`。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否，已回归。
- 修复状态：已回归

### P2-R2-008 已发布作业仍暴露可点击编辑入口并触发后端 400

- 严重级别：P2
- 功能清单编号：TEACHER-013
- 模块：web/teacher assignments
- 角色：教师
- 页面或对象：`/teacher/assignments?offeringId=32`、`/teacher/assignments/261/edit?offeringId=32`
- 操作步骤：以开课 `32` 的授课教师创建作业 `261` 并发布；随后从作业列表点击该已发布作业的编辑入口，在编辑页修改标题、说明和提交次数后点击“保存作业”。
- 实际表现：列表仍提供已发布作业可点击编辑入口；编辑页允许提交保存，后端返回 `ASSIGNMENT_STATUS_INVALID` 400，响应消息为“只有草稿任务可以编辑”。
- 期望表现：前端应与后端状态规则一致；只有草稿作业可以进入可保存编辑态，已发布或已关闭作业不应提供可点击编辑入口，也不应等到后端 400 才暴露规则。
- 影响说明：不会破坏数据一致性，但会误导教师认为已发布作业可以修改，保存失败时形成网络错误和不可理解的编辑体验。
- 证据：
  - MCP 网络观察：`PUT /api/v1/teacher/assignments/261` 返回 400，响应 `{"code":"ASSIGNMENT_STATUS_INVALID","message":"只有草稿任务可以编辑"}`。
  - MCP 页面观察：修复前已发布作业仍可点击编辑并进入编辑页。
- 修复说明：
  - `web/src/app/(teacher)/teacher/assignments/page.tsx` 仅为 `DRAFT` 作业渲染编辑链接；非草稿作业渲染禁用按钮，title 为“只有草稿作业可以编辑”。
  - `web/src/app/(teacher)/teacher/assignments/[assignmentId]/edit/page.tsx` 在非 `DRAFT` 状态显示“只有草稿作业可以编辑”，禁用“保存作业”，并在保存处理入口直接返回。
  - `web/src/tests/unit/assignment/teacher-assignments-page.test.tsx`、`web/src/tests/unit/assignment/teacher-assignment-edit-page.test.tsx` 增加 TDD 单测，覆盖发布态禁用列表编辑和非草稿编辑页禁止保存。
- 修复后回归：
  - MCP 页面：刷新 `/teacher/assignments/261/edit?offeringId=32` 后显示“只有草稿作业可以编辑”，保存按钮禁用；返回列表后 DOM 显示编辑按钮 disabled、发布按钮 disabled、关闭按钮 enabled。
  - MCP 补证：关闭已发布作业 `261` 后列表显示“已关闭”；另创建草稿作业 `262`，编辑标题为 `MCP-R2-06102203 草稿编辑补证-EDIT` 后保存成功，列表保持“草稿”并显示新标题。
  - MCP 截图：`176-r2-teacher-assignment-draft-created.png`、`177-r2-teacher-assignment-published-before-edit.png`、`178-r2-teacher-assignment-published-edit-blocked.png`、`179-r2-teacher-assignment-closed.png`、`180-r2-teacher-assignment-draft-edit-form.png`、`181-r2-teacher-assignment-draft-edited.png`
  - MCP 网络：`product-full-verification-round2-evidence/runtime/teacher-assignment-edit-close-network.txt` 包含发布后编辑 400 根因、修复后禁用编辑和关闭作业 `261` 200；`teacher-assignment-draft-edit-network.txt` 包含草稿作业 `262` 创建 201、编辑 PUT 200 和列表刷新 200。
  - MCP 控制台：`product-full-verification-round2-evidence/runtime/teacher-assignment-edit-close-console.txt`、`teacher-assignment-draft-edit-console.txt`，warning/error 均为 0。
  - 定向单测：`npm test -- src/tests/unit/assignment/teacher-assignments-page.test.tsx src/tests/unit/assignment/teacher-assignment-edit-page.test.tsx`，2 files / 9 tests passed。
  - 前端门禁：`npm run lint`、`npm run typecheck` 均通过，exit 0。
  - 构建门禁：`npm run build`、`cd docs && npm run docs:build` 均通过，exit 0。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否，作业编辑和关闭已回归；当前稳定 API 和页面入口未提供作业撤回或重新发布。
- 修复状态：已回归

### E2E-R2-GATE-001 成员添加 E2E 等待旧成功提示导致当前 `just e2e-real` 失败

- 严重级别：P1（命令门禁）
- 功能清单编号：TEACHER-004、E2E gate
- 模块：web/e2e
- 角色：教师
- 页面或对象：`/teacher/courses/[offeringId]/members`
- 操作步骤：2026-06-11 当前补跑 `just e2e-real`，执行 `full-organization-structure.spec.ts` 中课程成员添加流程。
- 实际表现：成员添加请求成功后页面已关闭弹窗并刷新列表，但 E2E helper 仍等待旧文案 `添加成功 1 人，失败 0 人。`，导致 `full-organization-structure.spec.ts` 超时失败。
- 期望表现：E2E 应与当前产品交互一致，等待成员添加 API 成功、弹窗关闭，并在成员列表中看到新增用户。
- 影响说明：不表示产品添加成员失败，但会破坏当前 `just e2e-real` 门禁，必须修复后才能收口。
- 证据：
  - 失败日志：`product-full-verification-round2-evidence/commands/12-current-just-e2e-real-20260611.log`，`49 passed / 1 failed`，失败点为等待旧成功提示。
  - 定向 RED：`npx playwright test src/tests/e2e/full-organization-structure.spec.ts --project=chromium` 在正确 E2E 环境下复现同一失败。
  - 错误上下文：失败快照中成员表已出现新增整课教师行，证明后端写入和列表回显已成功。
- 修复说明：`web/src/tests/e2e/full-organization-structure.spec.ts` 的 `addCourseMemberByUi` 改为接收创建用户对象，提交后等待 `/members/batch` 2xx、添加弹窗隐藏，并断言成员表出现新增用户名，不再依赖已被当前交互移除的弹窗内结果提示。
- 修复后回归：
  - 定向 E2E：同一 `full-organization-structure.spec.ts` 通过，`1 passed`。
  - Playwright MCP：以教师 `U-TA1` 打开 `/teacher/courses/2/members`，添加临时学生 `e2e-mcp-member-20260610172354`（用户 ID `496`）到教学班 `A1`；提交后弹窗关闭，搜索结果显示目标行；console 0 errors / 0 warnings，`POST /api/v1/teacher/course-offerings/2/members/batch` 200，证据 `product-full-verification-round2-evidence/runtime/current-mcp-member-add-regression-20260611.md`。
  - 完整 E2E：`just e2e-real` 通过，`50 passed (4.4m)`，证据 `product-full-verification-round2-evidence/commands/13-current-just-e2e-real-after-test-fix-20260611.log`；MCP 成员添加回归后再次补跑 `50 passed (3.7m)`，证据 `product-full-verification-round2-evidence/commands/16-current-just-e2e-real-after-mcp-member-regression-20260611.log`。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否，当前命令门禁已回归。
- 修复状态：已回归

## 18. 阻塞项与不适用项

当前无剩余阻塞项。已补证项包括管理员平台配置保存/恢复、管理员组织节点创建、管理员学期创建/编辑、管理员课程模板创建/编辑、管理员开课创建/编辑和共同管理学院选择、教师课程工作台教学班创建、教师成员添加/导入/状态变更、成员添加 E2E gate 契约修复、教师公告新建、教师资源上传下载、教师题库新增简答题与结构化题型新增、教师题库编辑归档、教师判题环境新增配置、教师判题环境编辑归档、教师作业创建发布、教师作业草稿编辑、教师作业关闭、发布后编辑规则阻断、教师提交批改与成绩发布、教师实验创建发布、教师实验编辑发布关闭、教师实验报告评阅发布、教师讨论创建/回复/锁定、教师通知全部已读、学生讨论回复、学生结构化作业提交、文件题附件、学生 WebIDE 历史恢复、编程正式提交、学生成绩/反馈回查、学生实验会话启停、学生实验报告提交与教师评语回查、学生通知单条已读、通知网络摘要和全站关键页 console/network 归因：

- 管理员：组织节点编辑当前未在稳定接口清单或页面入口中暴露；教学班创建实际位于教师课程工作台，已由教师端补证。
- 教师：作业撤回/重新发布当前未在稳定 API 或页面入口中暴露，记录为不适用；其余教师主线写入动作已补齐 MCP 主证据。
- 学生：当前强制项均已形成 MCP 主证据；P1-R2-006 已修复并通过 MCP 回归。
- 非功能：全站关键页 console/network 归因已保存，覆盖 55 个 route / 角色组合。

不适用项：作业撤回/重新发布当前未在稳定 API 或页面入口中暴露；组织节点编辑当前未在稳定接口清单或页面入口中暴露。

## 19. 第三阶段修复结果

第三阶段已处理第二轮明确可复现的 P2：

1. P2-R2-001：登录空表单错误态已显示应用内错误说明。
2. P2-R2-002：未授权课程上下文已收敛为课程不可访问态，不再展示快捷入口。
3. P2-R2-003：不存在课程 ID 已收敛为课程不可访问态，不再停留加载态或展示快捷入口。
4. P1-R2-004：实验报告评阅发布后学生端已显示教师评语，完成 TDD 单测和 MCP 回归。
5. P2-R2-005：报告型实验已停止查询运行时 current session，完成 TDD 单测和 MCP 网络回归。
6. P1-R2-006：编程正式提交后学生提交详情页不自动刷新判题终态，已完成 TDD 单测和 MCP 自动轮询回归。
7. P2-R2-007：添加课程成员成功后弹窗已关闭并刷新列表，完成 TDD 单测和 MCP 成员管理回归。
8. P2-R2-008：已发布作业不再暴露可点击编辑入口，非草稿编辑页禁用保存；草稿编辑和作业关闭完成 TDD 单测与 MCP 回归。
9. TEACHER-009-EDIT-ARCHIVE：题库编辑和归档已补 MCP 主证据；开课 `32` 中题目 `75` 创建、编辑、归档和包含归档查询均成功。
10. TEACHER-010-EDIT-ARCHIVE：判题环境编辑和归档已补 MCP 主证据；开课 `32` 中配置 `40` 创建、编辑、归档和包含归档查询均成功。
11. TEACHER-018-EDIT-CLOSE：实验编辑、发布和关闭已补 MCP 主证据；开课 `32` / 教学班 `234` 中实验 `53` 创建、编辑、发布和关闭均成功。

最终补齐完整逐页 console/network 归因，未发现需要新增编号的真实缺陷。当前第三阶段补证已覆盖管理员平台配置保存/恢复、管理员组织节点创建、管理员学期创建/编辑、管理员课程模板创建/编辑、管理员开课创建/编辑和共同管理学院选择、教师课程工作台教学班创建、教师成员添加/导入/状态变更、教师公告新建、教师资源上传下载、教师题库新增简答题与结构化题型新增、教师题库编辑归档、教师判题环境新增配置、教师判题环境编辑归档、教师作业创建发布、教师作业草稿编辑、发布后编辑规则阻断、教师作业关闭、教师提交批改、成绩发布、教师实验创建发布、教师实验编辑发布关闭、教师实验报告评阅发布、教师讨论创建/回复/锁定、教师通知全部已读、学生讨论回复、学生结构化提交、文件题附件上传下载、学生 WebIDE 历史恢复、编程正式提交自动刷新、学生成绩/反馈回查、学生实验会话启停、学生实验报告提交与教师评语回查、报告型实验不再查询运行时 current session、学生通知单条已读、通知网络摘要和全站关键页 console/network 归因；其中 P1-R2-004、P2-R2-005、P1-R2-006、P2-R2-007 和 P2-R2-008 涉及应用代码修改，其余补证不涉及应用代码修改。

## 20. 最终 just status 与提交信息

- 第二轮文本产物更新前 `just status`：`server/`、`web/`、`docs/` dirty entries 均为 0；第二轮 artifacts 位于 docs ignore 目录，需要 `git add -f`。
- 第三阶段修复前 `just status`：`server/` dirty entries 0；`web/` dirty entries 5；`docs/` dirty entries 3，另有 ignored round2 repair checklist 和 116-118 截图需要 `git add -f`。
- 第三阶段代码提交：`web` `5ea8296 fix(frontend): 修复登录与课程错误态`；`web` `1618469 fix(lab): 显示实验报告教师反馈`；`web` `e4b0f21 fix(judge): 自动刷新学生判题结果`；`web` `d7a5837 fix(course): 刷新新增课程成员`；`web` `0c773bd fix(assignment): 禁用非草稿作业编辑`；`web` `0d187f9 test(e2e): 稳定课程成员添加断言`。
- 第三阶段 docs 产物提交：以本报告所在 `docs/` 提交为准。
- 当前剩余状态：无 P0/P1，第二轮高影响 P2 均已回归，完整逐页 console/network 归因已补齐；2026-06-11 当前补跑暴露的 E2E 成员添加等待契约问题已修复，`just e2e-real` 已重新通过 `50 passed (4.4m)`，当前 MCP 成员添加回归后再次补跑 `50 passed (3.7m)`，`just verify-full` 也已重新通过；管理员平台配置保存/恢复、管理员组织节点创建、管理员学期创建/编辑、管理员课程模板创建/编辑、管理员开课创建编辑和共同管理学院选择、教师课程工作台教学班创建、成员添加/导入/状态变更、公告、资源、题库新增与编辑归档、判题环境新增与编辑归档、作业创建发布、作业草稿编辑、作业关闭、发布后编辑规则阻断、学生结构化提交、文件题、WebIDE 历史恢复、编程正式提交自动刷新、提交批改、成绩发布、实验创建编辑发布关闭、学生实验会话启停、实验报告提交/评阅/反馈、报告型实验网络噪音、讨论与通知状态变更已补齐；总体验收结论更新为 `通过`。
