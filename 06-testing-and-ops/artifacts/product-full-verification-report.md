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

原因：已确认存在会破坏演示主线的 P1 缺陷（编程题评测系统错误、实验终端交互不稳定），`just e2e-real` 辅助门禁失败；同时 Playwright MCP 主证据仍未覆盖全部强制用户可见功能，三次完整演示彩排尚未完成。根据 `goal-test.md`，任一强制项仍为 `阻塞` 或三次彩排未全部成功时，最终结论不得为 `通过` 或 `有条件通过`。

## 3. 上次缺口复核

| 缺口 | 本轮纠偏动作 | 当前状态 |
| --- | --- | --- |
| 旧目标允许 `未覆盖` | 新清单状态仅使用 `通过`、`失败`、`阻塞`、`不适用` | 通过 |
| 未先生成完整功能清单 | 已在开始页面操作前创建 `product-full-verification-feature-inventory.md` | 通过 |
| 用户可见结论弱依赖套件/API | 本报告要求 MCP 主证据，命令/API 仅辅助 | 进行中 |
| 三次演示彩排不是收尾门槛 | 已创建三次彩排记录文件，未完成前结论保持 `不通过` | 阻塞 |
| 动态详情页无真实 ID | 待通过 API/页面解析真实 ID 后逐项打开 | 阻塞 |

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
| 7 | `just e2e-real` | 失败 | `product-full-verification-evidence/commands/07-just-e2e-real.log`；43 passed, 3 failed, 4 did not run |
| 8 | `just verify` | 通过 | `product-full-verification-evidence/commands/10-just-verify.log`；server 356 tests passed，web lint/typecheck passed，docs build passed |
| 9 | `just verify-full` | 通过 | `product-full-verification-evidence/commands/11-just-verify-full.log`；server verify、web lint/typecheck/unit/build、docs build passed |
| 10 | `cd docs && npm run docs:build` | 通过 | `product-full-verification-evidence/commands/13-docs-build.log`；构建通过，仅有 chunk size 警告 |

## 6. 全功能清单摘要

- 初版清单已生成。
- 初版覆盖公共、认证、管理员、教师、学生、助教、运行时、文档、非功能和三次演示彩排。
- 页面实际渲染出来的按钮、菜单、表单、筛选器、tabs、弹窗和链接将在 MCP 页面操作时持续补充。

## 7. 逐角色验证结果

| 角色 | 当前状态 | 说明 |
| --- | --- | --- |
| 无登录用户 | 部分通过 | 已覆盖 `/login`、空表单失败、未登录 `/admin` 重定向；`/` 未登录默认态仍待单独截图 |
| 学校管理员 | 部分通过 | 已覆盖治理首页、用户、审计、权限解释拒绝、平台配置、组织、学期、课程模板、开课列表/详情、跨区禁止；保存/创建/编辑类动作仍未执行 |
| 教师 | 部分通过 | 已覆盖首页、课程列表/工作区、成员、资源、公告、讨论、讨论详情、题库、判题环境、作业列表/创建表单/编辑页、提交、成绩册、实验、通知；创建/上传/发布类动作仍未完整执行 |
| 学生 | 部分失败 | 已覆盖首页、课程列表/详情、作业、WebIDE、提交、成绩、通知、实验和一个讨论无权负例；编程题评测与实验终端为失败，客观题/文件题/实验报告提交仍阻塞 |
| 开课助教 | 部分通过 | `u-tac1` 已覆盖登录、授权提交页、管理员/学生区禁止；更细的禁止动作仍待覆盖 |
| 班级助教 | 部分通过 | `u-tao1` 已覆盖登录、A1 作业提交允许、A2 作业提交拒绝、开课级成绩册拒绝；顶栏角色文案存在可理解性问题 |
| 缺档案用户 | 通过 | 已用 API 准备缺档案 class-ta 账号并通过 MCP 登录进入 `/profile-required` |

## 8. 公共与认证验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| COMMON-002 | 通过 | `product-full-verification-screenshots/001-login-page.png` | `/login` 可加载，显示平台名称、登录说明、用户名/密码表单、显示密码按钮和平台公告。 |
| COMMON-003 | 失败 | `product-full-verification-screenshots/002-login-empty-submit-no-visible-error.png` | 点击空表单“立即登录”后页面仍停留登录页，但没有可见字段错误或全局错误文案，仅焦点回到用户名输入框。 |
| COMMON-004 | 通过 | `product-full-verification-screenshots/055-anonymous-admin-redirect-login.png` | 未登录直接打开 `/admin` 被重定向到 `/login?next=%2Fadmin`。 |
| COMMON-007 | 通过 | `product-full-verification-screenshots/052-user-menu-logout-to-login.png` | 已登录用户打开用户菜单可见姓名、用户名、角色，并点击“退出登录”回到 `/login`。 |
| AUTH-001 | 通过 | `product-full-verification-screenshots/003-admin-dashboard.png` | 使用管理员账号登录后进入 `/admin`，顶栏显示“管理端”和“系统管理员 / 学校管理员”。 |
| AUTH-002 | 通过 | `product-full-verification-screenshots/010-teacher-dashboard.png` | 使用教师账号登录后进入 `/teacher`，首页显示课程、待批改提交、待处理实验和通知入口。 |
| AUTH-003 | 通过 | `product-full-verification-screenshots/014-student-dashboard.png` | 使用学生账号登录后进入 `/student`，首页显示学习总览、课程、待办、实验、成绩和通知入口。 |
| AUTH-004 | 通过 | `product-full-verification-screenshots/044-ta-u-tac1-dashboard.png`; `product-full-verification-screenshots/048-ta-u-tao1-dashboard.png` | 开课助教/班级助教均可登录教师端；`u-tac1` 显示开课与班级助教身份，`u-tao1` 进入教师端但文案仍显示“开课助教1”。 |
| AUTH-005 | 通过 | `product-full-verification-screenshots/053-profile-required-profileless-ta.png`; `product-full-verification-evidence/commands/12-profile-required-data-prep.log` | API 创建缺学术档案但有 class-ta 课程身份的账号，MCP 登录后进入 `/profile-required`，页面说明需要管理员补全档案并提供退出/返回动作。 |
| AUTH-006 | 通过 | `product-full-verification-screenshots/035-student-admin-unauthorized.png`; `product-full-verification-screenshots/036-student-teacher-unauthorized.png`; `product-full-verification-screenshots/037-teacher-admin-unauthorized.png`; `product-full-verification-screenshots/062-admin-teacher-unauthorized.png`; `product-full-verification-screenshots/063-admin-student-unauthorized.png` | 受限角色进入非授权工作区均显示 `/unauthorized` 权限不足页。 |

## 9. 学生闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| STUDENT-001 | 通过 | `product-full-verification-screenshots/014-student-dashboard.png` | 学生首页显示课程/班级、未读通知、作业、实验和成绩等学习入口。 |
| STUDENT-002 | 通过 | `product-full-verification-screenshots/075-student-courses-list.png` | 学生课程列表显示真实课程 `数据结构 2025 秋`、教学班 A1 和“进入课堂”入口。 |
| STUDENT-003 | 通过 | `product-full-verification-screenshots/076-student-course-2-detail.png` | 使用真实教学班/课程上下文 ID `2` 打开学生课程详情，页面展示课程业务上下文。 |
| STUDENT-004 | 阻塞 | `product-full-verification-screenshots/077-student-course-2-discussion-26-detail.png` | 直接打开真实 discussionId `26` 返回“当前用户无权参与该课程讨论”；当前数据集中没有 A1 班可参与讨论，学生讨论正例需先创建 A1 讨论。 |
| STUDENT-005 | 通过 | `product-full-verification-screenshots/015-student-assignments-list.png` | 全部作业页显示已关闭、已发布和编程题作业，包含截止时间、分值和“查看作业/继续作答”等主操作。 |
| STUDENT-006 | 通过 | `product-full-verification-screenshots/016-student-programming-assignment-detail.png`; `product-full-verification-screenshots/020-student-assignment-after-webide-return.png` | 使用真实 assignmentId `7` 打开编程作业详情，可见题目、截止时间、总分、打开 IDE、提交答案和提交历史；从 IDE 保存返回后仍回到同一作业详情。 |
| STUDENT-012 | 通过 | `product-full-verification-screenshots/017-student-webide-initial.png` | 使用真实 assignmentId `7`、questionId `11` 打开 WebIDE，可见题目说明、文件浏览器、`main.py` 编辑器、保存、重置、历史、运行自测、保存并返回和状态栏。 |
| STUDENT-013 | 通过 | `product-full-verification-screenshots/019-student-webide-history.png` | IDE 历史面板显示版本号、保存时间、保存原因和恢复入口；保存按钮可点击且页面未报错。 |
| STUDENT-014 | 失败 | `product-full-verification-screenshots/018-student-webide-run-result.png` | 点击“运行自测”后页面展示部分样例通过，但同时出现 `RUNTIME_ERROR` 和“自定义评测脚本未返回裁决 JSON”，不能证明编程题运行链路稳定可演示。 |
| STUDENT-015 | 失败 | `product-full-verification-screenshots/020-student-assignment-after-webide-return.png`; `product-full-verification-screenshots/021-student-submission-detail-after-submit.png` | IDE 内确认“保存并返回”可回到作业详情；作业详情点击“提交答案”进入提交详情，但提交结果为 `SYSTEM_ERROR`。 |
| STUDENT-016 | 失败 | `product-full-verification-screenshots/021-student-submission-detail-after-submit.png` | 使用真实 submissionId `44` 打开提交详情，页面展示提交编号、代码、反馈和下载报告入口，但判题结果为 `SYSTEM_ERROR`，反馈为“评测失败：自定义评测脚本未返回裁决 JSON”。 |
| STUDENT-017 | 通过 | `product-full-verification-screenshots/022-student-grades.png`; `product-full-verification-screenshots/023-student-grades-offering-2.png` | 学生成绩全局入口可达；选择真实课程 `数据结构 2025 秋` 后显示 A1 班成绩、作业数量、作业得分、发布状态和提交编号。 |
| STUDENT-018 | 通过 | `product-full-verification-screenshots/033-student-notifications.png`; `product-full-verification-screenshots/034-student-notification-mark-read.png` | 通知中心显示判题、资源、公告、讨论、作业、实验、成绩等通知；单条“标记已读”后顶栏未读数从 17 降到 16，首条按钮消失。 |
| STUDENT-019 | 通过 | `product-full-verification-screenshots/024-student-labs-list.png`; `product-full-verification-screenshots/025-student-lab-selected.png` | 学生实验页显示真实教学班 A1 的已发布实验；选择 `MCP 终端闭环复核 0608-1644` 后显示实验环境、资源限制、会话时间、运行说明和操作按钮。 |
| STUDENT-020 | 失败 | `product-full-verification-screenshots/026-student-lab-runtime-started.png`; `product-full-verification-screenshots/029-student-lab-terminal-second-open.png`; `product-full-verification-screenshots/030-student-lab-terminal-echo.png`; `product-full-verification-screenshots/032-student-lab-stop-attempt.png` | 实验环境可启动、二次点击后 Web 终端可连接并显示欢迎输出，停止环境最终成功；但第一次打开终端停在“未连接”，且输入 `echo AUBB-MCP-TERMINAL` 后未出现独立回显结果行，终端交互演示不稳定。 |
| STUDENT-021 | 阻塞 | `product-full-verification-screenshots/024-student-labs-list.png` | 实验报告内容、附件上传、保存草稿、正式提交入口可见；尚未选择实验并提交报告，不能标为通过。 |

## 10. 教师闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TEACHER-001 | 通过 | `product-full-verification-screenshots/010-teacher-dashboard.png` | 教师首页显示 4 门课程、待批改提交、待处理实验、未读通知和快速入口。 |
| TEACHER-002 | 通过 | `product-full-verification-screenshots/064-teacher-courses-list.png` | 教师课程列表可达并展示真实课程入口。 |
| TEACHER-003 | 通过 | `product-full-verification-screenshots/011-teacher-course-workspace-offering-2.png` | 使用真实 offeringId `2` 打开课程工作区，显示教学班、教师、学生、作业、实验、成绩以及成员、公告、资源、讨论、题库、判题环境等上下文导航。 |
| TEACHER-004 | 阻塞 | `product-full-verification-screenshots/065-teacher-course-2-members.png` | 成员页可达并显示成员管理入口；本阶段尚未执行添加/导入/状态变更。 |
| TEACHER-005 | 阻塞 | `product-full-verification-screenshots/067-teacher-course-2-announcements.png` | 公告页可达并显示创建/列表能力；尚未创建、编辑或切换状态。 |
| TEACHER-006 | 阻塞 | `product-full-verification-screenshots/066-teacher-course-2-resources.png` | 资源页可达并显示资源管理能力；尚未上传/下载/重命名/删除文件。 |
| TEACHER-007 | 阻塞 | `product-full-verification-screenshots/068-teacher-course-2-discussions.png` | 讨论列表可达，显示创建讨论、真实讨论和锁定讨论动作；尚未创建/回复/锁定。 |
| TEACHER-008 | 通过 | `product-full-verification-screenshots/069-teacher-course-2-discussion-26-detail.png` | 使用真实 discussionId `26` 打开教师讨论详情页。 |
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
| TEACHER-026 | 阻塞 | `product-full-verification-screenshots/074-teacher-notifications.png` | 教师通知页可达；尚未执行标记已读。 |

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
| TA-004/005 | 通过 | `product-full-verification-screenshots/048-ta-u-tao1-dashboard.png`; `product-full-verification-screenshots/049-ta-u-tao1-gradebook-offering-2.png`; `product-full-verification-screenshots/050-ta-u-tao1-submissions-assignment-7-allowed.png`; `product-full-verification-screenshots/051-ta-u-tao1-submissions-assignment-4-denied.png`; `product-full-verification-evidence/commands/10-tao1-role-bindings.log` | `u-tao1` 只有 class 2 的 `class_ta` 有效绑定；页面允许查看 A1 作业 7 提交，拒绝 A2 作业 4 提交，开课级成绩册显示无权。 |
| TA-009 | 通过 | `product-full-verification-screenshots/046-ta-u-tac1-admin-unauthorized.png`; `product-full-verification-screenshots/047-ta-u-tac1-student-unauthorized.png`; `product-full-verification-screenshots/051-ta-u-tao1-submissions-assignment-4-denied.png` | 助教不能进入管理员/学生工作区，班级助教不能访问其他班级作业提交。 |

## 13. 运行时能力验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| RUNTIME-006 | 失败 | `product-full-verification-screenshots/018-student-webide-run-result.png`; `product-full-verification-screenshots/021-student-submission-detail-after-submit.png` | 编程题自测和正式提交均产生系统级评测错误，详见 P1-002。 |
| RUNTIME-007 | 失败 | `product-full-verification-screenshots/026-student-lab-runtime-started.png`; `product-full-verification-screenshots/029-student-lab-terminal-second-open.png`; `product-full-verification-screenshots/032-student-lab-stop-attempt.png` | 实验会话可创建和停止，终端二次打开后可连接，但首次打开未连接且 echo 无输出回显，详见 P1-003。 |
| RUNTIME-001 | 通过 | `product-full-verification-evidence/commands/18-runtime-db-summary-fixed.log`; `product-full-verification-evidence/commands/08-submission-answer-127-grade-check.log` | PostgreSQL 中存在提交、批改分数、审计与通知记录；人工批改 SQL 已确认 submission answer 127 回写。 |
| RUNTIME-003 | 通过 | `product-full-verification-evidence/commands/16-runtime-rabbitmq-ping.log`; `product-full-verification-evidence/commands/20-runtime-compose-ps.log` | RabbitMQ 进程 ping 成功，compose 状态为 healthy。 |
| RUNTIME-004 | 阻塞 | `product-full-verification-evidence/commands/15-runtime-redis-ping.log`; `product-full-verification-evidence/commands/19-runtime-redis-ping-fixed.log`; `product-full-verification-evidence/commands/20-runtime-compose-ps.log` | Redis compose 状态为 healthy，但直接 `redis-cli ping` 因认证策略返回 NOAUTH/AUTH failed；未取得认证后缓存键级证据。 |
| RUNTIME-008 | 通过 | `product-full-verification-screenshots/008-admin-audit-logs-actor-u-ta1.png`; `product-full-verification-screenshots/009-admin-audit-log-detail.png`; `product-full-verification-evidence/commands/18-runtime-db-summary-fixed.log` | 审计日志页面和数据库均显示审计记录，latest audit 为本轮操作时间。 |

## 14. 文档一致性验证

已确认强制输入文档存在；`just verify`、`just verify-full` 内部 docs build 均通过，且单独执行 `cd docs && npm run docs:build` 通过，仅有 VitePress chunk size 警告。

## 15. 前端质量与响应式验证

已执行最小视口截图，但覆盖不足以满足合同要求：

| 视口 | 状态 | 证据 | 说明 |
| --- | --- | --- | --- |
| `1280x800` | 阻塞 | `product-full-verification-screenshots/078-nfr-1280-student-course-discussion-denied.png` | 仅覆盖学生讨论无权页，管理员/教师/登录关键页未完整覆盖。 |
| `1440x900` | 阻塞 | `product-full-verification-screenshots/079-nfr-1440-student-webide.png` | 覆盖学生 WebIDE，但该页面仍存在评测系统错误；管理员/教师关键页未完整覆盖。 |
| `390x844` | 阻塞 | `product-full-verification-screenshots/080-nfr-390-student-labs.png` | 覆盖学生实验页，未覆盖登录、管理员开课、教师作业创建等全部要求页面。 |

## 16. 三次完整演示彩排记录摘要

三次彩排均未执行完成，见 `product-full-verification-rehearsal-log.md`。

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
- 实际表现：50 个用例中 43 通过、3 失败、4 未运行，命令退出码 1。
- 期望表现：真实后端 E2E 全部通过。
- 影响说明：这是辅助门禁失败，不能直接替代 MCP 页面结论；但按合同必须记录，且会阻止总体验收结论为通过。
- 证据：
  - MCP 截图：不适用。
  - MCP 页面观察：不适用。
  - 辅助证据：`product-full-verification-evidence/commands/07-just-e2e-real.log`
- 是否阻塞演示彩排：可能。学生作业详情和组织开课 UI 失败会影响演示路线可信度；教师登录限流可能是运行节奏问题。
- 是否阻塞后续功能验证：否，仍继续执行不依赖该门禁的 MCP 页面验证。
- 修复建议方向：分别调查学生作业列表主操作文案/数据状态、共同管理学院选择器可达性、登录限流策略或 E2E 节流。
- 修复状态：待修复

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
- 修复状态：待修复

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
- 修复状态：待修复

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

## 18. 阻塞项与不适用项

当前阻塞同时来自两类事实：

- 已确认应用缺陷：WebIDE 自测/提交返回系统错误，实验终端首次连接和命令输出不稳定。
- 尚未执行的强制项：管理员保存/创建/编辑，教师成员导入、资源上传、公告/讨论/题库/判题环境/实验发布，学生客观题、文件题、实验报告提交，完整 NFR 覆盖和第三次彩排。

## 19. 修复优先级建议

本阶段不进入修复。发现缺陷后仅记录严重级别、复现步骤、影响范围和建议归属。

## 20. 最终 just status 与提交信息

- 最终 `just status`：`server/` clean；`web/` clean；`docs/` clean，`main...origin/main [ahead 2]`；根目录不是 git 仓库。
- 状态证据：`product-full-verification-evidence/commands/22-final-just-status.log`、`product-full-verification-evidence/commands/23-post-commit-just-status.log`。
- 本轮提交：`docs` 子仓库 commit `1fdb885 docs(test): 记录产品全功能验证证据`。
- 仅提交验证产物；未修改 `server/`、`web/` 应用代码、配置代码、测试代码或生产文档正文。
