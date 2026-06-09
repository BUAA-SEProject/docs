# AUBB 产品全功能完整验证报告

## 1. 验证元信息

- 执行日期：2026-06-09
- 工作区：`/Users/moorefoss/Code/AUBB`
- 执行合同：`goal-test.md`
- 本轮边界：默认不修改应用代码、配置代码、测试代码和生产文档正文；仅创建或更新本合同规定的验证产物。
- 主证据规则：用户可见功能必须以 Playwright MCP 页面操作为主证据；API、数据库、日志、命令、对象存储为辅助证据。
- 产物：
  - 功能清单：`docs/06-testing-and-ops/artifacts/product-full-verification-feature-inventory.md`
  - 主报告：`docs/06-testing-and-ops/artifacts/product-full-verification-report.md`
  - 三次演示彩排记录：`docs/06-testing-and-ops/artifacts/product-full-verification-rehearsal-log.md`
  - 截图目录：`docs/06-testing-and-ops/artifacts/product-full-verification-screenshots/`
  - 辅助证据目录：`docs/06-testing-and-ops/artifacts/product-full-verification-evidence/`

## 2. 总体验证结论

当前结论：`不通过`

原因：本轮继续补充了管理员权限解释允许/拒绝、开课助教禁止动作、1280/1440/390 响应式和关键页面 console/network 证据，Playwright MCP 截图范围扩展到 `001`-`114`。2026-06-10 修复阶段已回归第一轮确认的 P1 缺陷（编程题评测系统错误、实验终端交互不稳定）和 `just e2e-real` 辅助门禁失败；但 Playwright MCP 主证据对强制用户可见功能仍有缺口，三次完整演示彩排尚未完成。根据 `goal-test.md`，任一强制项仍为 `阻塞` 或三次彩排未全部成功时，最终结论不得为 `通过` 或 `有条件通过`。

## 3. 上次缺口复核

| 缺口 | 本轮纠偏动作 | 当前状态 |
| --- | --- | --- |
| 旧目标允许非合同状态 | 新清单状态仅使用 `通过`、`失败`、`阻塞`、`不适用` | 通过 |
| 未先生成完整功能清单 | 已在开始页面操作前创建 `product-full-verification-feature-inventory.md` | 通过 |
| 用户可见结论弱依赖套件/API | 本报告要求 MCP 主证据，命令/API 仅辅助 | 进行中 |
| 三次演示彩排不是收尾门槛 | 已创建三次彩排记录文件，未完成前结论保持 `不通过` | 阻塞 |
| 动态详情页无真实 ID | 已补充真实 `offeringId=2`、`discussionId=29`、`assignmentId=3/7`、`submissionId=45` 等正例；仍有管理员创建编辑、题库、实验报告等动态动作阻塞 | 阻塞 |

## 4. 输入缺失与环境阻塞

强制输入全部存在，见 `product-full-verification-evidence/commands/00-input-check.log`。

当前环境状态：

- `just dev-up` 已确认 Docker 依赖运行，后端 `18080` 和前端 `3000` 已监听。
- `just healthcheck-strict` 通过，env、端口、后端 readiness/OpenAPI 和前端登录页可用。
- `just seed-fixtures` 通过，22 个 case 全部成功。
- 本地库存在历史 `E2E-*` / `MCP-*` / `FULLRUN-*` 前缀残留，已做非破坏性摘要检查。

## 5. 命令门禁结果

| 顺序 | 命令 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | `just status` | 通过 | `product-full-verification-evidence/commands/01-just-status-rerun.log` |
| 2 | `just --list` | 通过 | `product-full-verification-evidence/commands/02-just-list.log` |
| 3 | `just dev-up` | 通过 | `product-full-verification-evidence/commands/03-just-dev-up.log` |
| 4 | `just healthcheck-strict` | 通过 | `product-full-verification-evidence/commands/04-just-healthcheck-strict.log` |
| 5 | 残留摘要检查 | 通过；前 3 次命令写法失败已保留 | `05-residual-summary.log`、`05b-residual-summary.log`、`05c-residual-summary.log`、`05d-residual-summary.log` |
| 6 | `just seed-fixtures` | 通过 | `product-full-verification-evidence/commands/06-just-seed-fixtures.log` |
| 7 | `just e2e-real` | 修复阶段已回归 | 第一轮证据 `product-full-verification-evidence/commands/07-just-e2e-real.log` 为 43 passed, 3 failed, 4 did not run；2026-06-10 修复阶段重跑通过，50 passed (3.7m) |
| 8 | `just verify` | 修复阶段已回归 | 第一轮证据 `product-full-verification-evidence/commands/10-just-verify.log` 为 server 356 tests passed，web lint/typecheck passed，docs build passed；2026-06-10 修复阶段重跑通过，server 357 tests passed，web lint/typecheck passed，docs build passed |
| 9 | `just verify-full` | 通过 | `product-full-verification-evidence/commands/11-just-verify-full.log`；server verify、web lint/typecheck/unit/build、docs build passed |
| 10 | `cd docs && npm run docs:build` | 通过 | `product-full-verification-evidence/commands/13-docs-build.log`、`product-full-verification-evidence/commands/24-docs-build-rerun.log`、`product-full-verification-evidence/commands/26-docs-build-rerun-20260609.log`；构建通过，仅有 chunk size 警告 |

## 6. 全功能清单摘要

- 初版清单已在页面操作前生成，后续已按新增 MCP 发现补充公共搜索、通知、通用通知路径、教师内容动作、学生简答题、Redis/MinIO/通知轮询和 NFR 问题。
- 清单覆盖公共、认证、管理员、教师、学生、助教、运行时、文档、非功能和三次演示彩排。
- 页面实际渲染出来的按钮、菜单、表单、筛选器、tabs、弹窗和链接仍按 MCP 页面操作持续补充；当前截图范围为 `001`-`114`。

## 7. 逐角色验证结果

| 角色 | 当前状态 | 说明 |
| --- | --- | --- |
| 无登录用户 | 部分通过 | 已覆盖 `/login`、空表单失败、未登录 `/admin` 重定向；`/` 未登录默认态仍待单独截图 |
| 学校管理员 | 部分通过 | 已覆盖治理首页、用户、审计、权限解释允许/拒绝、平台配置、组织、学期、课程模板、开课列表/详情、跨区禁止；保存/创建/编辑类动作仍未执行 |
| 教师 | 部分通过 | 已覆盖首页、课程列表/工作区、成员、资源上传下载、公告创建、讨论创建与回复、讨论详情、题库、判题环境、作业列表/创建表单/编辑页、提交、成绩册、实验、通知和全部已读；成员导入、题库/判题环境/实验发布、作业创建保存仍阻塞 |
| 学生 | 部分失败 | 已覆盖首页、课程列表/详情、作业、WebIDE、提交、成绩、通知、实验、讨论正反例和简答 Markdown 提交；编程题评测和实验终端已在修复阶段回归，客观题/文件题/实验报告提交仍阻塞 |
| 开课助教 | 部分通过 | `u-tac1` 已覆盖登录、授权提交页、管理员/学生区禁止和未授权开课公告拒绝；未授权页面仍暴露部分动作入口，详见 P2-007 |
| 班级助教 | 部分通过 | `u-tao1` 已覆盖登录、A1 作业提交允许、A2 作业提交拒绝、开课级成绩册拒绝；顶栏角色文案存在可理解性问题 |
| 缺档案用户 | 通过 | 已用 API 准备缺档案 class-ta 账号并通过 MCP 登录进入 `/profile-required` |

## 8. 公共与认证验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| COMMON-002 | 通过 | `product-full-verification-screenshots/001-login-page.png` | `/login` 可加载，显示平台名称、登录说明、用户名/密码表单、显示密码按钮和平台公告。 |
| COMMON-003 | 失败 | `product-full-verification-screenshots/002-login-empty-submit-no-visible-error.png` | 点击空表单“立即登录”后页面仍停留登录页，但没有可见字段错误或全局错误文案，仅焦点回到用户名输入框。 |
| COMMON-004 | 通过 | `product-full-verification-screenshots/055-anonymous-admin-redirect-login.png` | 未登录直接打开 `/admin` 被重定向到 `/login?next=%2Fadmin`。 |
| COMMON-005 | 通过 | `product-full-verification-screenshots/081-common-student-global-search-results.png`; `product-full-verification-screenshots/082-common-student-global-search-navigate-grades.png`; `product-full-verification-screenshots/085-common-teacher-global-search-results.png`; `product-full-verification-screenshots/086-common-teacher-global-search-navigate-submissions.png` | 学生顶栏搜索 `成绩` 可显示“全部成绩 学生端”并跳转 `/student/grades`；教师顶栏搜索 `提交` 可显示“全部提交 教师端”并跳转 `/teacher/submissions`。 |
| COMMON-006 | 通过 | `product-full-verification-screenshots/083-common-student-topbar-notification-link.png`; `product-full-verification-screenshots/087-teacher-notifications-before-mark-all-read.png`; `product-full-verification-screenshots/088-teacher-notifications-after-mark-all-read.png`; `product-full-verification-evidence/mcp-network-087-088-teacher-notifications-mark-read.md` | 学生顶栏通知入口可跳转通知页；教师通知页可显示未读数并点击“全部已读”，顶栏未读徽标消失。 |
| COMMON-007 | 通过 | `product-full-verification-screenshots/052-user-menu-logout-to-login.png` | 已登录用户打开用户菜单可见姓名、用户名、角色，并点击“退出登录”回到 `/login`。 |
| AUTH-001 | 通过 | `product-full-verification-screenshots/003-admin-dashboard.png` | 使用管理员账号登录后进入 `/admin`，顶栏显示“管理端”和“系统管理员 / 学校管理员”。 |
| AUTH-002 | 通过 | `product-full-verification-screenshots/010-teacher-dashboard.png` | 使用教师账号登录后进入 `/teacher`，首页显示课程、待批改提交、待处理实验和通知入口。 |
| AUTH-003 | 通过 | `product-full-verification-screenshots/014-student-dashboard.png` | 使用学生账号登录后进入 `/student`，首页显示学习总览、课程、待办、实验、成绩和通知入口。 |
| AUTH-004 | 通过 | `product-full-verification-screenshots/044-ta-u-tac1-dashboard.png`; `product-full-verification-screenshots/048-ta-u-tao1-dashboard.png` | 开课助教/班级助教均可登录教师端；`u-tac1` 显示开课与班级助教身份，`u-tao1` 进入教师端但文案仍显示“开课助教1”。 |
| AUTH-005 | 通过 | `product-full-verification-screenshots/053-profile-required-profileless-ta.png`; `product-full-verification-evidence/commands/12-profile-required-data-prep.log` | API 创建缺学术档案但有 class-ta 课程身份的账号，MCP 登录后进入 `/profile-required`，页面说明需要管理员补全档案并提供退出/返回动作。 |
| AUTH-006 | 通过 | `product-full-verification-screenshots/035-student-admin-unauthorized.png`; `product-full-verification-screenshots/036-student-teacher-unauthorized.png`; `product-full-verification-screenshots/037-teacher-admin-unauthorized.png`; `product-full-verification-screenshots/062-admin-teacher-unauthorized.png`; `product-full-verification-screenshots/063-admin-student-unauthorized.png` | 受限角色进入非授权工作区均显示 `/unauthorized` 权限不足页。 |
| AUTH-007 | 通过 | `product-full-verification-screenshots/084-auth-me-notifications-direct.png`; `product-full-verification-evidence/mcp-network-081-084-notifications.md` | 已登录学生直接打开 `/me/notifications` 可进入通用通知中心并保留学生端导航上下文。 |

## 9. 学生闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| STUDENT-001 | 通过 | `product-full-verification-screenshots/014-student-dashboard.png` | 学生首页显示课程/班级、未读通知、作业、实验和成绩等学习入口。 |
| STUDENT-002 | 通过 | `product-full-verification-screenshots/075-student-courses-list.png` | 学生课程列表显示真实课程 `数据结构 2025 秋`、教学班 A1 和“进入课堂”入口。 |
| STUDENT-003 | 通过 | `product-full-verification-screenshots/076-student-course-2-detail.png` | 使用真实教学班/课程上下文 ID `2` 打开学生课程详情，页面展示课程业务上下文。 |
| STUDENT-004 | 通过 | `product-full-verification-screenshots/077-student-course-2-discussion-26-detail.png`; `product-full-verification-screenshots/098-student-discussion-29-reply-filled.png`; `product-full-verification-screenshots/099-student-discussion-29-reply-created.png` | 学生直接打开无权 discussionId `26` 显示禁止参与；教师新建真实 discussionId `29` 后，学生可进入 `/student/courses/2/discussions/29` 填写并提交回复。 |
| STUDENT-005 | 通过 | `product-full-verification-screenshots/015-student-assignments-list.png` | 全部作业页显示已关闭、已发布和编程题作业，包含截止时间、分值和“查看作业/继续作答”等主操作。 |
| STUDENT-006 | 通过 | `product-full-verification-screenshots/016-student-programming-assignment-detail.png`; `product-full-verification-screenshots/020-student-assignment-after-webide-return.png` | 使用真实 assignmentId `7` 打开编程作业详情，可见题目、截止时间、总分、打开 IDE、提交答案和提交历史；从 IDE 保存返回后仍回到同一作业详情。 |
| STUDENT-007/008/009/011 | 阻塞 | `product-full-verification-evidence/student-accessible-assignment-types-20260609.log` | U-ST1 当前可访问的已发布作业只有简答题和编程题，未找到可提交的单选、多选、填空或文件题作业；在不改数据和不创建新作业的本阶段只能记录为阻塞。 |
| STUDENT-010 | 通过 | `product-full-verification-screenshots/100-student-short-answer-markdown-preview.png`; `product-full-verification-screenshots/101-student-short-answer-submission-45-detail.png`; `product-full-verification-evidence/student-short-answer-submission-45-db-fixed.log` | 学生打开真实 assignmentId `3`，输入 Markdown 简答并预览后提交；提交详情和 SQL 均显示 submissionId `45`、answerId `128` 已保存答案文本。但提交详情顶部仍显示“无文本答案”，详见 P2-006。 |
| STUDENT-012 | 通过 | `product-full-verification-screenshots/017-student-webide-initial.png` | 使用真实 assignmentId `7`、questionId `11` 打开 WebIDE，可见题目说明、文件浏览器、`main.py` 编辑器、保存、重置、历史、运行自测、保存并返回和状态栏。 |
| STUDENT-013 | 通过 | `product-full-verification-screenshots/019-student-webide-history.png` | IDE 历史面板显示版本号、保存时间、保存原因和恢复入口；保存按钮可点击且页面未报错。 |
| STUDENT-014 | 修复阶段已回归 | `product-full-verification-screenshots/018-student-webide-run-result.png`; `product-full-verification-screenshots/repair-p1-002-webide-sample-run-fixed.png` | 第一轮点击“运行自测”后页面展示部分样例通过，但同时出现 `RUNTIME_ERROR` 和“自定义评测脚本未返回裁决 JSON”；2026-06-10 修复阶段重新打开 WebIDE 并点击“运行自测”，页面显示 `ACCEPTED，样例输出与预期一致`。 |
| STUDENT-015 | 修复阶段已回归 | `product-full-verification-screenshots/020-student-assignment-after-webide-return.png`; `product-full-verification-screenshots/021-student-submission-detail-after-submit.png`; `product-full-verification-screenshots/repair-p1-002-submission-accepted-fixed.png` | 第一轮 IDE 返回作业详情后正式提交结果为 `SYSTEM_ERROR`；2026-06-10 修复阶段再次提交 submissionId `46`，提交详情显示反馈 `ACCEPTED，2/2 个测试点通过，得分 100/100`。 |
| STUDENT-016 | 修复阶段已回归 | `product-full-verification-screenshots/021-student-submission-detail-after-submit.png`; `product-full-verification-screenshots/repair-p1-002-submission-accepted-fixed.png` | 第一轮真实 submissionId `44` 的提交详情为 `SYSTEM_ERROR`；2026-06-10 修复阶段真实 submissionId `46` 的提交详情显示“已完成 / 通过”，辅助 DB 查询显示 `job_status=SUCCEEDED`、`verdict=ACCEPTED`、`score=100/100`。 |
| STUDENT-017 | 通过 | `product-full-verification-screenshots/022-student-grades.png`; `product-full-verification-screenshots/023-student-grades-offering-2.png` | 学生成绩全局入口可达；选择真实课程 `数据结构 2025 秋` 后显示 A1 班成绩、作业数量、作业得分、发布状态和提交编号。 |
| STUDENT-018 | 通过 | `product-full-verification-screenshots/033-student-notifications.png`; `product-full-verification-screenshots/034-student-notification-mark-read.png` | 通知中心显示判题、资源、公告、讨论、作业、实验、成绩等通知；单条“标记已读”后顶栏未读数从 17 降到 16，首条按钮消失。 |
| STUDENT-019 | 通过 | `product-full-verification-screenshots/024-student-labs-list.png`; `product-full-verification-screenshots/025-student-lab-selected.png` | 学生实验页显示真实教学班 A1 的已发布实验；选择 `MCP 终端闭环复核 0608-1644` 后显示实验环境、资源限制、会话时间、运行说明和操作按钮。 |
| STUDENT-020 | 修复阶段已回归 | `product-full-verification-screenshots/026-student-lab-runtime-started.png`; `product-full-verification-screenshots/029-student-lab-terminal-second-open.png`; `product-full-verification-screenshots/030-student-lab-terminal-echo.png`; `product-full-verification-screenshots/032-student-lab-stop-attempt.png`; `product-full-verification-screenshots/repair-p1-003-lab-terminal-fixed.png` | 第一轮实验环境可启动和停止，但首次打开终端停在“未连接”，且 echo 无独立输出结果行；2026-06-10 修复阶段 MCP 复测一次点击即可连接，`echo AUBB-MCP-TERMINAL` 出现独立输出行。 |
| STUDENT-021 | 阻塞 | `product-full-verification-screenshots/024-student-labs-list.png` | 实验报告内容、附件上传、保存草稿、正式提交入口可见；尚未选择实验并提交报告，不能标为通过。 |

## 10. 教师闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TEACHER-001 | 通过 | `product-full-verification-screenshots/010-teacher-dashboard.png` | 教师首页显示 4 门课程、待批改提交、待处理实验、未读通知和快速入口。 |
| TEACHER-002 | 通过 | `product-full-verification-screenshots/064-teacher-courses-list.png` | 教师课程列表可达并展示真实课程入口。 |
| TEACHER-003 | 通过 | `product-full-verification-screenshots/011-teacher-course-workspace-offering-2.png` | 使用真实 offeringId `2` 打开课程工作区，显示教学班、教师、学生、作业、实验、成绩以及成员、公告、资源、讨论、题库、判题环境等上下文导航。 |
| TEACHER-004 | 阻塞 | `product-full-verification-screenshots/065-teacher-course-2-members.png` | 成员页可达并显示成员管理入口；本阶段尚未执行添加/导入/状态变更。 |
| TEACHER-005 | 通过 | `product-full-verification-screenshots/089-teacher-announcement-create-dialog-filled.png`; `product-full-verification-screenshots/090-teacher-announcement-created.png`; `product-full-verification-evidence/content-actions-db-fixed-20260609.log` | 教师在 offeringId `2` 公告页打开发布弹窗，填写标题和正文并提交；列表和 SQL 均显示公告 `MCP 全功能验证公告 20260609-2019` 已创建。 |
| TEACHER-006 | 通过 | `product-full-verification-screenshots/091-teacher-resource-upload-dialog-file-selected.png`; `product-full-verification-screenshots/092-teacher-resource-uploaded-list.png`; `product-full-verification-evidence/resource-upload-download-sha256-20260609.log`; `product-full-verification-evidence/minio-resource-object-meta-20260609.log` | 教师上传 `mcp-upload-resource-20260609.txt` 后列表显示文件、大小和下载入口；MCP 下载文件与源文件 SHA256 一致，MinIO 对象元数据存在。 |
| TEACHER-007 | 通过 | `product-full-verification-screenshots/093-teacher-discussions-list-before-create.png`; `product-full-verification-screenshots/094-teacher-discussion-create-dialog-filled.png`; `product-full-verification-screenshots/095-teacher-discussion-created-list.png`; `product-full-verification-evidence/content-actions-db-fixed-20260609.log` | 教师创建真实 discussionId `29` 并在讨论列表看到新讨论；列表中历史长标题发生横向溢出，详见 P2-005。 |
| TEACHER-008 | 通过 | `product-full-verification-screenshots/069-teacher-course-2-discussion-26-detail.png`; `product-full-verification-screenshots/096-teacher-discussion-detail-reply-filled.png`; `product-full-verification-screenshots/097-teacher-discussion-reply-created.png`; `product-full-verification-screenshots/099-student-discussion-29-reply-created.png` | 使用真实 discussionId `26` 打开教师讨论详情；对新 discussionId `29` 提交教师回复后，学生也可在同一讨论提交回复。 |
| TEACHER-009~014 | 阻塞 | `product-full-verification-screenshots/070-teacher-course-2-question-bank.png` | 题库页可达；单选、多选、填空、简答、文件题、编程题创建/编辑尚未逐项执行。 |
| TEACHER-015 | 阻塞 | `product-full-verification-screenshots/071-teacher-course-2-judge-environments.png` | 判题环境页可达；创建、编辑、归档尚未执行。 |
| TEACHER-016 | 通过 | `product-full-verification-screenshots/012-teacher-assignments-offering-2.png` | 教师全部作业页可按课程筛选并显示真实作业状态、分值、截止时间和操作入口。 |
| TEACHER-017 | 阻塞 | `product-full-verification-screenshots/013-teacher-assignment-create-form.png` | 作业创建表单可达，课程上下文、教学班、标题、说明、开放/截止时间、提交次数、题目区、题库入口、判题设置入口可见；本阶段尚未执行创建提交，不能标为通过。 |
| TEACHER-018 | 阻塞 | `product-full-verification-screenshots/072-teacher-assignment-7-edit.png` | 使用真实 assignmentId `7` 打开作业编辑页；尚未保存草稿或发布确认。 |
| TEACHER-020 | 通过 | `product-full-verification-screenshots/040-teacher-submissions-list.png`; `product-full-verification-screenshots/041-teacher-submissions-assignment-7.png` | 全部提交页显示跨课程筛选；使用真实 `offeringId=2&assignmentId=7` 后显示作业 7 的提交记录，包含用户 14、提交时间、判题状态、得分和操作列。 |
| TEACHER-021 | 通过 | `product-full-verification-screenshots/038-teacher-submission-44-detail.png` | 使用真实 submissionId `44` 打开提交详情，显示提交编号、代码、提交级重判、分题反馈、答案重判、判题任务和下载报告。 |
| TEACHER-022 | 通过 | `product-full-verification-screenshots/039-teacher-submission-44-grade-saved.png`; `product-full-verification-evidence/commands/08-submission-answer-127-grade-check.log` | 教师填写分数 `0` 和本轮人工反馈后点击“保存批改”；辅助 SQL 确认 `submission_answers.id=127` 已写入 `manual_score=0`、`final_score=0`、反馈文本、批改人 `9` 和批改时间。 |
| TEACHER-023 | 失败 | `product-full-verification-screenshots/042-teacher-gradebook-offering-2.png`; `product-full-verification-screenshots/043-teacher-gradebook-student-u-st1.png`; `product-full-verification-evidence/downloads/gradebook-offering-2.csv` | 成绩册显示课程上下文、统计卡片、学生表格、学生搜索筛选和下载能力；筛选 `u-st1` 后学生数变为 1。点击“导出 Excel”下载成功，但文件名和内容为 `gradebook-offering-2.csv`，与按钮文案不一致。 |
| TEACHER-024 | 阻塞 | `product-full-verification-screenshots/073-teacher-labs.png` | 教师实验页可达；尚未创建/发布/关闭实验。 |
| TEACHER-026 | 通过 | `product-full-verification-screenshots/087-teacher-notifications-before-mark-all-read.png`; `product-full-verification-screenshots/088-teacher-notifications-after-mark-all-read.png`; `product-full-verification-evidence/mcp-network-087-088-teacher-notifications-mark-read.md` | 教师通知页显示未读通知和“全部已读”；点击后顶栏未读徽标消失，网络记录保存为辅助证据。 |

## 11. 管理员闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| ADMIN-001 | 通过 | `product-full-verification-screenshots/003-admin-dashboard.png` | 管理端工作台显示当前管理员、平台配置摘要、组织治理、用户治理、权限解释和审计日志入口。 |
| ADMIN-002 | 阻塞 | `product-full-verification-screenshots/056-admin-platform-config.png` | 平台配置页可达并显示配置表单；尚未执行保存与恢复。 |
| ADMIN-003 | 通过 | `product-full-verification-screenshots/057-admin-org-units-tree-detail.png` | 组织架构页显示组织树、节点详情、上下文入口、可新增下级和层级规则。 |
| ADMIN-004 | 阻塞 | `product-full-verification-screenshots/057-admin-org-units-tree-detail.png` | 新增根节点/新增子节点入口可见；尚未创建或编辑组织节点。 |
| ADMIN-005 | 通过 | `product-full-verification-screenshots/004-admin-users-list.png`; `product-full-verification-screenshots/005-admin-users-search-u-ta1.png` | 用户管理页显示关键词、学工号、状态、档案身份、身份角色、组织范围筛选；搜索 `u-ta1` 返回教师1真实用户。 |
| ADMIN-006 | 通过 | `product-full-verification-screenshots/006-admin-user-detail-u-ta1.png` | 使用真实 userId `9` 打开 `/admin/users/9`，可见解释权限、查看审计、强制下线、禁用账号、保存学籍资料等动作；未执行破坏性账号操作。 |
| ADMIN-007 | 通过 | `product-full-verification-screenshots/006-admin-user-detail-u-ta1.png` | 用户详情显示真实姓名、学号/工号、身份类型、学籍状态、主属学院、系统身份、组织成员关系。 |
| ADMIN-008 | 阻塞 | `product-full-verification-screenshots/058-admin-academic-terms.png` | 学期管理页可达；尚未创建/编辑学期。 |
| ADMIN-009 | 阻塞 | `product-full-verification-screenshots/059-admin-course-catalogs.png` | 课程模板页可达；尚未创建/编辑课程模板。 |
| ADMIN-010 | 阻塞 | `product-full-verification-screenshots/060-admin-course-offerings-list.png` | 开课管理页可达，显示真实开课列表和“新增开课”；尚未执行开课创建/编辑和共同管理学院选择。 |
| ADMIN-011 | 通过 | `product-full-verification-screenshots/061-admin-course-offering-2-detail.png` | 使用真实 offeringId `2` 打开管理员开课详情页。 |
| ADMIN-012 | 通过 | `product-full-verification-screenshots/114-admin-auth-explain-school-auth-read-allowed.png`; `product-full-verification-evidence/mcp-network-114-auth-explain-allowed-response.json`; `product-full-verification-evidence/admin-auth-explain-scope-db-20260609.log` | 管理员在权限解释页使用高级编号参数查询 userId `1`、权限“读取权限解释”、学校作用域 `SCHOOL/1`，页面显示“最终判定：允许 / 按作用域角色授权”；响应体为 `ALLOW_BY_SCOPE_ROLE`，DB 辅助证据显示 `u-sa1` 拥有 `school_admin@school:1` 和 `auth.explain.read`。平台作用域 `PLATFORM/0` 负例返回 `DENY_SCOPE_MISMATCH`，作为作用域边界辅助证据保存于 `product-full-verification-screenshots/102-admin-auth-explain-auth-read-denied.png`。 |
| ADMIN-013 | 通过 | `product-full-verification-screenshots/007-admin-auth-explain-deny.png` | 权限解释页从用户上下文进入，点击“立即分析”后显示“最终判定：拒绝 / 授权范围不匹配”。 |
| ADMIN-014 | 通过 | `product-full-verification-screenshots/008-admin-audit-logs-actor-u-ta1.png`; `product-full-verification-screenshots/009-admin-audit-log-detail.png` | 审计日志按操作者 `u-ta1` 筛选，显示作业发布、课程成员批量添加、登录成功等记录；详情展开显示日志元数据和复制 JSON。 |
| ADMIN-015 | 通过 | `product-full-verification-screenshots/062-admin-teacher-unauthorized.png`; `product-full-verification-screenshots/063-admin-student-unauthorized.png` | 管理员登录态直接打开 `/teacher`、`/student` 均进入 `/unauthorized`。 |

## 12. 助教与权限边界验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TA-006 | 通过 | `product-full-verification-screenshots/036-student-teacher-unauthorized.png` | 学生登录态直接打开 `/teacher` 被重定向到 `/unauthorized`，页面显示“权限不足”和返回首页。 |
| TA-007 | 通过 | `product-full-verification-screenshots/035-student-admin-unauthorized.png` | 学生登录态直接打开 `/admin` 被重定向到 `/unauthorized`，页面显示“权限不足”和返回首页。 |
| TA-008 | 通过 | `product-full-verification-screenshots/037-teacher-admin-unauthorized.png` | 教师登录态直接打开 `/admin` 被重定向到 `/unauthorized`，页面显示“权限不足”。 |
| TA-001/002 | 通过 | `product-full-verification-screenshots/044-ta-u-tac1-dashboard.png`; `product-full-verification-screenshots/045-ta-u-tac1-submissions-assignment-7.png` | `u-tac1` 作为开课+班级助教登录教师端，可进入授权作业提交列表。 |
| TA-003 | 通过 | `product-full-verification-screenshots/103-ta-u-tac1-offering-5-denied-workspace.png`; `product-full-verification-screenshots/104-ta-u-tac1-offering-5-announcements-denied.png`; `product-full-verification-evidence/mcp-network-103-104-ta-denied.md` | `u-tac1` 直接打开未授权 offeringId `5` 时，工作区数据面板返回“当前用户无权查看教学班”；继续进入 `/teacher/courses/5/announcements` 后公告接口返回 403，页面显示“当前用户无权管理该课程公告”。权限边界成立，但未授权页仍暴露“发布公告”等入口，详见 P2-007。 |
| TA-004/005 | 通过 | `product-full-verification-screenshots/048-ta-u-tao1-dashboard.png`; `product-full-verification-screenshots/049-ta-u-tao1-gradebook-offering-2.png`; `product-full-verification-screenshots/050-ta-u-tao1-submissions-assignment-7-allowed.png`; `product-full-verification-screenshots/051-ta-u-tao1-submissions-assignment-4-denied.png`; `product-full-verification-evidence/commands/10-tao1-role-bindings.log` | `u-tao1` 只有 class 2 的 `class_ta` 有效绑定；页面允许查看 A1 作业 7 提交，拒绝 A2 作业 4 提交，开课级成绩册显示无权。 |
| TA-009 | 通过 | `product-full-verification-screenshots/046-ta-u-tac1-admin-unauthorized.png`; `product-full-verification-screenshots/047-ta-u-tac1-student-unauthorized.png`; `product-full-verification-screenshots/051-ta-u-tao1-submissions-assignment-4-denied.png` | 助教不能进入管理员/学生工作区，班级助教不能访问其他班级作业提交。 |

## 13. 运行时能力验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| RUNTIME-006 | 修复阶段已回归 | `product-full-verification-screenshots/018-student-webide-run-result.png`; `product-full-verification-screenshots/021-student-submission-detail-after-submit.png`; `product-full-verification-screenshots/repair-p1-002-webide-sample-run-fixed.png`; `product-full-verification-screenshots/repair-p1-002-submission-accepted-fixed.png` | 第一轮编程题自测和正式提交均产生系统级评测错误；2026-06-10 修复阶段已通过 MCP 复测 WebIDE 自测和正式提交，提交详情为 `ACCEPTED，2/2 个测试点通过，得分 100/100`。 |
| RUNTIME-007 | 修复阶段已回归 | `product-full-verification-screenshots/026-student-lab-runtime-started.png`; `product-full-verification-screenshots/029-student-lab-terminal-second-open.png`; `product-full-verification-screenshots/032-student-lab-stop-attempt.png`; `product-full-verification-screenshots/repair-p1-003-lab-terminal-fixed.png` | 第一轮实验会话可创建和停止，但首次打开终端未连接且 echo 无输出回显；2026-06-10 修复阶段 MCP 复测一次打开终端即为“已连接”，命令回显和输出结果均可见，详见 P1-003。 |
| RUNTIME-001 | 通过 | `product-full-verification-evidence/commands/18-runtime-db-summary-fixed.log`; `product-full-verification-evidence/commands/08-submission-answer-127-grade-check.log` | PostgreSQL 中存在提交、批改分数、审计与通知记录；人工批改 SQL 已确认 submission answer 127 回写。 |
| RUNTIME-002 | 通过 | `product-full-verification-evidence/content-actions-db-fixed-20260609.log`; `product-full-verification-evidence/resource-upload-download-sha256-20260609.log`; `product-full-verification-evidence/minio-resource-object-meta-20260609.log` | 课程资源上传后，数据库记录 object key、原文件名、MIME 和大小；MCP 下载文件 SHA256 与源文件一致，MinIO 对象元数据存在。 |
| RUNTIME-003 | 通过 | `product-full-verification-evidence/commands/16-runtime-rabbitmq-ping.log`; `product-full-verification-evidence/commands/20-runtime-compose-ps.log` | RabbitMQ 进程 ping 成功，compose 状态为 healthy。 |
| RUNTIME-004 | 通过 | `product-full-verification-evidence/redis-auth-ping-20260609.log`; `product-full-verification-evidence/redis-key-scan-20260609.log`; `product-full-verification-evidence/commands/20-runtime-compose-ps.log` | Redis 认证 ping 返回 `PONG`，键扫描显示通知未读数、auth session 和课程摘要缓存键。 |
| RUNTIME-005 | 通过 | `product-full-verification-screenshots/083-common-student-topbar-notification-link.png`; `product-full-verification-screenshots/087-teacher-notifications-before-mark-all-read.png`; `product-full-verification-screenshots/088-teacher-notifications-after-mark-all-read.png`; `product-full-verification-evidence/mcp-network-087-088-teacher-notifications-mark-read.md` | 通知入口和教师“全部已读”页面状态变化已通过 MCP 验证，并保存网络摘要作为辅助证据。 |
| RUNTIME-008 | 通过 | `product-full-verification-screenshots/008-admin-audit-logs-actor-u-ta1.png`; `product-full-verification-screenshots/009-admin-audit-log-detail.png`; `product-full-verification-evidence/commands/18-runtime-db-summary-fixed.log` | 审计日志页面和数据库均显示审计记录，latest audit 为本轮操作时间。 |

## 14. 文档一致性验证

已确认强制输入文档存在；`just verify`、`just verify-full` 内部 docs build 均通过，且单独执行 `cd docs && npm run docs:build` 通过。收尾前又执行一次 `npm run docs:build`，证据为 `product-full-verification-evidence/commands/26-docs-build-rerun-20260609.log`，结果仍为通过，仅有 VitePress chunk size 警告。

## 15. 前端质量与响应式验证

已继续补充 1280、1440 和 390 视口截图；桌面关键页已形成更多 MCP 主证据，移动端仍缺管理员和教师关键页：

| 视口 | 状态 | 证据 | 说明 |
| --- | --- | --- | --- |
| `1280x800` | 通过 | `product-full-verification-screenshots/078-nfr-1280-student-course-discussion-denied.png`; `product-full-verification-screenshots/105-nfr-1280-ta-denied-announcements.png`; `product-full-verification-screenshots/106-nfr-1280-login-page.png`; `product-full-verification-screenshots/107-nfr-1280-admin-users.png` | 登录页、管理员用户表、学生无权页和助教无权公告页在 1280 宽度未出现结构性重叠；助教无权页暴露动作入口另记 P2-007。 |
| `1440x900` | 通过 | `product-full-verification-screenshots/079-nfr-1440-student-webide.png`; `product-full-verification-screenshots/108-nfr-1440-teacher-course-2-workspace.png`; `product-full-verification-screenshots/109-nfr-1440-teacher-assignment-create.png` | 教师课程工作区和作业创建表单布局稳定；学生 WebIDE 布局可见，但运行功能错误另见 P1-002。 |
| `390x844` | 阻塞 | `product-full-verification-screenshots/080-nfr-390-student-labs.png`; `product-full-verification-screenshots/110-nfr-390-login-filled.png`; `product-full-verification-screenshots/111-nfr-390-student-assignments.png`; `product-full-verification-screenshots/112-nfr-390-student-grades.png`; `product-full-verification-screenshots/113-nfr-390-student-notifications.png` | 登录和学生作业/成绩/通知/实验页在窄屏可用，未发现结构性重叠；管理员和教师移动关键页仍未形成 MCP 主证据，保持阻塞。 |

控制台与网络补证：

- `product-full-verification-evidence/mcp-console-107-admin-users-nfr.txt`、`mcp-console-108-teacher-course-nfr.txt`、`mcp-console-109-teacher-assignment-create-nfr.txt`、`mcp-console-111-student-assignments-nfr.txt`、`mcp-console-112-student-grades-nfr.txt`、`mcp-console-113-student-notifications-nfr.txt` 均为 0 个 error。
- `product-full-verification-evidence/mcp-console-103-104-ta-denied.txt` 中的 403 error 来自未授权 offeringId `5` 的负例验证，与 TA-003 权限拒绝一致。
- `product-full-verification-evidence/mcp-network-110-113-mobile-nfr.md` 中的 notification stream `ERR_ABORTED` 发生在页面切换，后续 stream 可重新建立；全站网络错误仍未逐页完成归因，因此 NFR-004 保持阻塞。

新增可用性问题：

- P2-005：教师讨论列表历史长标题横向溢出，证据 `product-full-verification-screenshots/093-teacher-discussions-list-before-create.png`。
- P2-006：学生简答提交详情顶部显示“无文本答案”，但分题区域和数据库均有真实答案，证据 `product-full-verification-screenshots/101-student-short-answer-submission-45-detail.png`。
- P2-007：开课助教访问未授权开课页时数据面板正确拒绝，但工作区和公告页仍展示快捷动作入口，证据 `product-full-verification-screenshots/103-ta-u-tac1-offering-5-denied-workspace.png`、`product-full-verification-screenshots/104-ta-u-tac1-offering-5-announcements-denied.png`。

## 16. 三次完整演示彩排记录摘要

三次完整演示彩排没有全部成功。彩排 1 和彩排 2 均已开始并失败；本轮在彩排 2 后继续补充了公告、资源、讨论、通知、简答提交、权限解释正反例、助教禁止动作和响应式证据，但这些补证不能把彩排 2 改写为成功。彩排 3 因 P1 缺陷和强制项阻塞未启动，见 `product-full-verification-rehearsal-log.md`。

## 17. 缺陷详情

### P2-001 登录空表单缺少可见错误提示

- 严重级别：P2
- 功能清单编号：COMMON-003
- 模块：web/auth
- 角色：无登录用户
- 页面或对象：`/login`
- 操作步骤：打开登录页，不输入用户名和密码，点击“立即登录”。
- 实际表现：页面停留在登录页，焦点回到用户名输入框，但未显示字段错误或全局错误文案。
- 期望表现：字段旁或表单顶部显示“请输入用户名 / 请输入密码”等可理解反馈。
- 影响说明：不会阻断登录主线，但会降低空表单错误态可理解性。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/002-login-empty-submit-no-visible-error.png`
  - MCP 页面观察：点击后页面仍为 `/login`，snapshot 中未出现可见错误文案。
  - 辅助证据：无。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复建议方向：在表单校验失败时显示字段级错误，并保持 `aria-invalid`/错误说明关联。
- 修复状态：待修复

### E2E-GATE-001 `just e2e-real` 辅助门禁失败

- 严重级别：P1
- 功能清单编号：STUDENT-006、ADMIN-010、TEACHER-001
- 模块：web/tests/e2e 或对应页面/数据链路
- 角色：学生、管理员、教师
- 页面或对象：`/student/assignments`、开课创建 Dialog、教师登录 fixture
- 操作步骤：执行 `just e2e-real`。
- 实际表现：第一轮 50 个用例中 43 通过、3 失败、4 未运行，命令退出码 1；2026-06-10 修复阶段完整重跑已通过，50 passed。
- 期望表现：真实后端 E2E 全部通过。
- 影响说明：这是辅助门禁失败，不能直接替代 MCP 页面结论；但按合同必须记录，且会阻止总体验收结论为通过。
- 证据：
  - MCP 截图：不适用。
  - MCP 页面观察：不适用。
  - 辅助证据：`product-full-verification-evidence/commands/07-just-e2e-real.log`
- 是否阻塞演示彩排：可能。学生作业详情和组织开课 UI 失败会影响演示路线可信度；教师登录限流可能是运行节奏问题。
- 是否阻塞后续功能验证：否，仍继续执行不依赖该门禁的 MCP 页面验证。
- 修复建议方向：分别调查学生作业列表主操作文案/数据状态、共同管理学院选择器可达性、登录限流策略或 E2E 节流。
- 修复状态：已回归
- 修复阶段补充证据（2026-06-10）：
  - 根因 1：学生作业 E2E 仍断言旧版主操作文案“开始做题”，而当前真实页面对已开始作业展示“继续作答 ${作业标题}”。
  - 根因 2：组织开课 E2E 直接点击“共同管理学院”，但 `MultiOptionPicker` 默认只展示前 6 个选项；历史 E2E 残留组织较多时目标学院需要先搜索。
  - 根因 3：教师登录 fixture 在快速真实 E2E 中可能触发 Redis 限流；Redis TTL 为 0 时服务端返回 `Retry-After: 0`，E2E 登录辅助逻辑也未对 `RATE_LIMIT_EXCEEDED` 提供兜底等待。
  - 代码修复：`web/src/tests/e2e/assignment-submission.spec.ts`、`web/src/tests/e2e/full-organization-structure.spec.ts`、`web/src/tests/e2e/real-backend.ts`、`server/src/main/java/com/aubb/server/common/ratelimit/RedisRateLimitService.java`、`server/src/test/java/com/aubb/server/common/ratelimit/RedisRateLimitServiceTests.java`。
  - 定向回归：真实后端 Playwright E2E 覆盖 `assignment-submission.spec.ts`、`full-organization-structure.spec.ts`、`teacher-course.spec.ts`，结果 `8 passed (32.2s)`。
  - 完整回归：`just e2e-real` 通过，`50 passed (3.7m)`。
  - 门禁回归：`cd server && bash ./mvnw -Dtest=RedisRateLimitServiceTests test` 通过，`Tests run: 4, Failures: 0, Errors: 0, Skipped: 0`；`just verify` 通过，后端 `357` tests passed，web lint/typecheck passed，docs build passed。

### P1-002 编程题自测和正式提交返回系统错误

- 严重级别：P1
- 功能清单编号：STUDENT-014、STUDENT-015、STUDENT-016、RUNTIME-006
- 模块：web/student assignments、server judge runtime 或题目评测脚本数据
- 角色：学生
- 页面或对象：`/student/assignments/7/workspace/11`、`/student/submissions/44?assignmentId=7`
- 操作步骤：学生打开编程作业 `Task-Programming-A1`，进入 WebIDE，点击“运行自测”；返回作业详情后点击“提交答案”。
- 实际表现：自测结果中同时出现 `ACCEPTED`、`RUNTIME_ERROR` 和“自定义评测脚本未返回裁决 JSON”；正式提交详情判题结果为 `SYSTEM_ERROR`，反馈同样指向自定义评测脚本未返回裁决 JSON。
- 期望表现：演示题目的自测和正式提交应返回可解释、稳定的通过/失败判定，不能以系统错误结束。
- 影响说明：编程题 WebIDE 是学生主线和运行时演示核心能力；当前结果会破坏演示主线，按合同阻止总体验收结论为通过或有条件通过。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/018-student-webide-run-result.png`
  - MCP 截图：`product-full-verification-screenshots/021-student-submission-detail-after-submit.png`
  - MCP 页面观察：提交详情显示 `SYSTEM_ERROR` 和“评测失败：自定义评测脚本未返回裁决 JSON”。
  - 辅助证据：后续补充 DB/日志或命令门禁。
- 是否阻塞演示彩排：是。
- 是否阻塞后续功能验证：否，仍可继续覆盖其他页面和权限边界。
- 修复建议方向：检查演示编程题的自定义评测脚本返回协议、go-judge 执行结果解析、样例/隐藏用例数据和前端错误解释。
- 修复状态：已回归
- 修复阶段补充证据（2026-06-10）：
  - 根因：演示编程题 fixture 使用旧版自定义 checker 协议，且 WebIDE 自测默认未带入题目样例输入。
  - 代码修复：`server/scripts/api-tests/permission/e2e_permission_realrun.py`、`server/scripts/api-tests/permission/e2e_permission_realrun_test.py`、`web/src/features/submission/hooks/use-programming-workspace-controller.ts`、`web/src/tests/unit/submission/programming-workspace-page.test.tsx`。
  - MCP 回归：学生 `U-ST1` 打开 `/student/assignments/7/workspace/11`，样例输入/期望输出自动填入后点击“运行自测”，显示 `ACCEPTED，样例输出与预期一致`；从作业详情提交后打开 `/student/submissions/46?assignmentId=7`，显示“已完成 / 通过”。
  - 截图：`product-full-verification-screenshots/repair-p1-002-webide-sample-run-fixed.png`、`product-full-verification-screenshots/repair-p1-002-submission-accepted-fixed.png`。
  - 命令验证：`cd server && python3 scripts/api-tests/permission/e2e_permission_realrun_test.py` 通过；`just seed-fixtures` 通过；`cd web && npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx` 通过；辅助 DB 查询确认 submissionId `46` 的 judge job 为 `SUCCEEDED/ACCEPTED/100/100`。

### P1-003 实验 Web 终端连接和交互输出不稳定

- 严重级别：P1
- 功能清单编号：STUDENT-020、RUNTIME-007
- 模块：web/student labs、server lab runtime 或终端连接代理
- 角色：学生
- 页面或对象：`/student/labs`
- 操作步骤：学生进入全部实验，选择 `MCP 终端闭环复核 0608-1644`，点击“启动环境”，再点击“打开终端”，等待连接；随后点击 Web 终端区域内的“打开终端”，输入 `echo AUBB-MCP-TERMINAL`，最后点击“停止环境”。
- 实际表现：环境启动后状态变为“运行中”；第一次打开终端后终端区显示“未连接”；再次点击 Web 终端区域按钮后显示“已连接”、`AUBB lab terminal ready.` 和 `resize accepted`；输入 echo 命令后页面仅显示命令本身，未显示独立输出结果行；停止环境最终回到“未启动”。控制台多次出现 `/api/v1/me/labs/16/sessions/current` 404，但会话创建后的 current 请求也返回 200。
- 期望表现：一次点击“打开终端”即可稳定连接，欢迎输出和用户命令回显/输出应可见且可用于演示。
- 影响说明：实验运行时是演示主线能力之一；需要二次点击且命令输出不可见会破坏现场演示可信度。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/026-student-lab-runtime-started.png`
  - MCP 截图：`product-full-verification-screenshots/028-student-lab-terminal-still-disconnected.png`
  - MCP 截图：`product-full-verification-screenshots/029-student-lab-terminal-second-open.png`
  - MCP 截图：`product-full-verification-screenshots/030-student-lab-terminal-echo.png`
  - MCP 截图：`product-full-verification-screenshots/032-student-lab-stop-attempt.png`
  - 辅助证据：MCP 网络记录显示 `POST /api/v1/me/labs/16/sessions` 为 201，后续 `GET /sessions/current` 为 200。
- 是否阻塞演示彩排：是。
- 是否阻塞后续功能验证：否。
- 修复建议方向：检查终端打开按钮状态机、WebSocket/stream 连接重试、终端输入提交和回显渲染，以及 current session 404 是否应静默处理。
- 修复状态：已回归
- 修复阶段补充证据（2026-06-10）：
  - 根因：外层“打开终端”只挂载终端组件，内层组件未自动发起 token/WebSocket 连接；修复过程中还确认 token 回调身份变化会造成重复连接，fake runtime 未按 xterm 的 `\r` 输入边界解析命令。
  - 代码修复：`web/src/features/lab/components/lab-terminal.tsx`、`web/src/tests/unit/lab/lab-terminal.test.tsx`、`server/src/main/java/com/aubb/server/modules/lab/application/runtime/FakeLabRuntimeProvisioner.java`、`server/src/test/java/com/aubb/server/integration/LabTerminalIntegrationTests.java`。
  - MCP 回归：学生 `U-ST1` 打开 `/student/labs`，选择 `MCP 终端闭环复核 0608-1644`，一次点击“打开终端”后状态为“已连接”；输入 `echo AUBB-MCP-TERMINAL` 后终端文本包含独立输出行 `AUBB-MCP-TERMINAL`。
  - 截图：`product-full-verification-screenshots/repair-p1-003-lab-terminal-fixed.png`。
  - 命令验证：`cd web && npm test -- src/tests/unit/lab/lab-terminal.test.tsx` 通过；`cd web && npm test -- src/tests/unit/lab/student-labs-page.test.tsx` 通过；`cd server && bash ./mvnw -Dtest=LabTerminalIntegrationTests#fakeTerminalWebSocketSendsWelcomeAndEchoesInput test` 通过；`just dev-down && just dev-up && just healthcheck-strict` 通过。

### P3-004 成绩册导出按钮文案与实际文件格式不一致

- 严重级别：P3
- 功能清单编号：TEACHER-023
- 模块：web/teacher gradebook
- 角色：教师
- 页面或对象：`/teacher/grading/gradebook?offeringId=2&studentUserId=14`
- 操作步骤：在教师成绩册点击“导出 Excel”。
- 实际表现：浏览器下载 `gradebook-offering-2.csv`，证据文件内容为 CSV 表头和数据行。
- 期望表现：按钮文案与实际导出格式一致；若导出 CSV，应标为“导出 CSV”，若标为 Excel，应返回 `.xlsx`。
- 影响说明：不影响成绩册数据导出主链路，但会造成交付演示时对文件格式的预期偏差。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/043-teacher-gradebook-student-u-st1.png`
  - 下载证据：`product-full-verification-evidence/downloads/gradebook-offering-2.csv`
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复建议方向：统一按钮文案、下载文件扩展名和 Content-Type。
- 修复状态：待修复

### P2-005 教师讨论列表长标题横向溢出

- 严重级别：P2
- 功能清单编号：TEACHER-007、NFR-005
- 模块：web/teacher discussions
- 角色：教师
- 页面或对象：`/teacher/courses/2/discussions`
- 操作步骤：教师进入课程 `offeringId=2` 的讨论列表，观察历史 E2E 讨论标题和新建讨论入口。
- 实际表现：历史长标题未换行或截断，链接宽度扩出主内容区和视口。
- 期望表现：长标题应在列表容器内换行或截断，不能造成横向溢出。
- 影响说明：不阻断讨论创建，但会影响教师端列表可读性和演示观感。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/093-teacher-discussions-list-before-create.png`
  - MCP 页面观察：截图中多个 `E2E-Discussion-*` 标题向右超出主内容区域。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复建议方向：为讨论标题链接增加容器宽度约束、`overflow-wrap` 或 line clamp，并验证 1280/1440/移动视口。
- 修复状态：待修复

### P2-006 简答提交详情顶部“无文本答案”与分题答案矛盾

- 严重级别：P2
- 功能清单编号：STUDENT-010、STUDENT-016、NFR-005
- 模块：web/student submissions
- 角色：学生
- 页面或对象：`/student/submissions/45?assignmentId=3`
- 操作步骤：学生打开简答作业 `assignmentId=3`，输入 Markdown 文本，预览后提交，并进入提交详情。
- 实际表现：提交详情顶部“答案内容”卡片显示“无文本答案”，但下方分题答案区域显示已提交的简答文本；SQL 也确认 `submission_answers.id=128` 保存了答案内容。
- 期望表现：提交详情不应出现互相矛盾的答案状态；若为分题答案，应隐藏顶部“无文本答案”或改为题目级摘要。
- 影响说明：不阻断简答提交保存，但会误导学生和演示讲解，降低提交详情可信度。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/101-student-short-answer-submission-45-detail.png`
  - 辅助证据：`product-full-verification-evidence/student-short-answer-submission-45-db-fixed.log`
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复建议方向：按题型区分提交详情摘要文案，简答/客观题优先展示 per-question answer 状态。
- 修复状态：待修复

### P2-007 未授权开课页仍展示可执行入口

- 严重级别：P2
- 功能清单编号：TA-003、NFR-005
- 模块：web/teacher course workspace、web/teacher announcements
- 角色：开课助教
- 页面或对象：`/teacher/courses/5`、`/teacher/courses/5/announcements`
- 操作步骤：以 `u-tac1` 登录教师端，直接打开未授权 offeringId `5` 的课程工作区，再点击或直达“发布全课公告”/公告页。
- 实际表现：接口正确返回 403，页面数据面板显示“当前用户无权查看教学班”或“当前用户无权管理该课程公告”；但课程工作区仍展示“发布全课公告”“上传课程资源”“管理本课作业”等快捷入口，公告页顶部仍展示“发布公告”按钮和课程导航。
- 期望表现：未授权课程上下文应隐藏或禁用后续动作入口，并以单一拒绝态替代可执行按钮，避免用户继续进入必然失败的子页面。
- 影响说明：不构成越权访问，权限边界由 API 和页面错误态守住；但会降低助教权限负例的可理解性和演示观感。
- 证据：
  - MCP 截图：`product-full-verification-screenshots/103-ta-u-tac1-offering-5-denied-workspace.png`
  - MCP 截图：`product-full-verification-screenshots/104-ta-u-tac1-offering-5-announcements-denied.png`
  - MCP 网络/控制台：`product-full-verification-evidence/mcp-network-103-104-ta-denied.md`、`product-full-verification-evidence/mcp-console-103-104-ta-denied.txt`
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复建议方向：在课程上下文加载 403 时进入页面级权限拒绝态；所有课程动作按钮和二级导航应依赖已授权课程上下文再渲染。
- 修复状态：待修复

## 18. 阻塞项与不适用项

当前阻塞来自尚未执行或因数据缺失阻塞的强制项：管理员保存/创建/编辑，教师成员导入、题库、判题环境、作业创建保存、实验发布，学生单选/多选/填空/文件题、实验报告提交，移动端管理员/教师 NFR、全站 console/network 逐页归因和第三次彩排。第一轮确认的 WebIDE 自测/提交系统错误、实验终端首次连接和命令输出不稳定、`just e2e-real` 辅助门禁失败已在 2026-06-10 修复阶段回归。

## 19. 修复优先级建议

第一阶段已优先修复 P1 与 E2E 辅助门禁问题；P2/P3 体验问题保留到后续低风险修复或完整验收阶段按影响面处理。

## 20. 最终 just status 与提交信息

- 第一轮收尾前 `just status`：`server/` clean；`web/` clean；`docs/` 有 3 个待提交验证产物修改；根目录不是 git 仓库。
- 状态证据：`product-full-verification-evidence/commands/22-final-just-status.log`、`product-full-verification-evidence/commands/23-post-commit-just-status.log`、`product-full-verification-evidence/commands/25-final-just-status-precommit.log`、`product-full-verification-evidence/commands/27-final-just-status-precommit-20260609.log`。
- 第一轮提交主题：`docs(test): 补充产品全功能验证证据`。
- 2026-06-10 修复阶段将按 `server/`、`web/`、`docs/` 子仓库分别提交本轮修复、回归测试和修复证据。
