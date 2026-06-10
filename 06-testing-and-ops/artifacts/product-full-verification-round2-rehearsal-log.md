# AUBB 产品全功能完整验证第二轮演示彩排记录

## 1. 彩排元信息

- 执行阶段：第二阶段重新完整交付验收
- 创建时间：2026-06-10 CST
- 控制合同：`goal.md`、`goal-test.md`
- 主报告：`product-full-verification-round2-report.md`
- 功能清单：`product-full-verification-round2-feature-inventory.md`
- 状态枚举：`通过`、`失败`、`阻塞`、`不适用`
- 主证据目录：`product-full-verification-round2-screenshots/`

## 2. 彩排要求

每次彩排覆盖：

- 无登录用户进入登录页和受限页重定向。
- 管理员治理、组织/用户/权限解释/审计主线。
- 教师课程、题库/资源/作业/提交/成绩/实验主线。
- 学生课程、作业、WebIDE、成绩、实验、通知主线。
- 助教授权和拒绝边界。
- 故障预案：权限失败、对象不存在或服务不可用时的页面解释。

失败不得改写为成功；失败后继续记录剩余可执行路径。

## 3. 彩排记录

> 彩排后的第三阶段补证已补齐写入类强制动作、彩排中发现的 P1/P2 缺陷回归，以及全站关键页 console/network 归因。最终结论以 `product-full-verification-round2-report.md` 为准。

### 彩排 1

- 状态：通过主线
- 开始时间：2026-06-10 12:41 CST
- 结束时间：2026-06-10 12:48 CST
- 账号：
  - 管理员：`U-SA1`
  - 教师：`U-TA1`
  - 学生：`U-ST1`
  - 开课助教：`mcp-r2-mq6z7s5j-yz44k-offering-ta`
  - 班级助教：`mcp-r2-mq6z7s5j-yz44k-class-ta`
- 路线：
  1. 未登录访问 `/admin`，确认重定向登录。
  2. 管理员登录，打开治理首页、用户管理、权限解释、审计日志。
  3. 教师登录，打开教学工作台、课程工作区、提交列表、成绩册。
  4. 学生登录，打开学习中心、WebIDE，执行样例自测，打开实验、成绩、通知和学生访问管理员区负例。
  5. 开课助教登录，进入授权课程并验证管理员区禁止。
  6. 班级助教登录，进入成员页并验证管理员区禁止。
- 结果：主线页面均可打开，WebIDE 自测显示通过，权限负例进入 `/unauthorized`。
- 失败或阻塞：本次未执行写入类强制动作，例如平台配置保存、作业创建、实验报告提交。
- 证据：
  - `056-r2-rehearsal1-admin-dashboard.png`
  - `057-r2-rehearsal1-admin-users.png`
  - `058-r2-rehearsal1-admin-auth-explain.png`
  - `059-r2-rehearsal1-admin-audit-logs.png`
  - `060-r2-rehearsal1-teacher-dashboard.png`
  - `061-r2-rehearsal1-teacher-course.png`
  - `062-r2-rehearsal1-teacher-submissions.png`
  - `063-r2-rehearsal1-teacher-gradebook.png`
  - `064-r2-rehearsal1-student-dashboard.png`
  - `065-r2-rehearsal1-student-webide.png`
  - `066-r2-rehearsal1-student-webide-run.png`
  - `067-r2-rehearsal1-student-labs.png`
  - `068-r2-rehearsal1-student-grades.png`
  - `069-r2-rehearsal1-me-notifications.png`
  - `070-r2-rehearsal1-student-forbidden-admin.png`
  - `071-r2-rehearsal1-offering-ta-dashboard.png`
  - `072-r2-rehearsal1-offering-ta-course.png`
  - `073-r2-rehearsal1-offering-ta-forbidden-admin.png`
  - `074-r2-rehearsal1-class-ta-dashboard.png`
  - `075-r2-rehearsal1-class-ta-members.png`
  - `076-r2-rehearsal1-class-ta-forbidden-admin.png`

### 彩排 2

- 状态：通过主线
- 开始时间：2026-06-10 12:49 CST
- 结束时间：2026-06-10 12:53 CST
- 账号：
  - 管理员：`U-SA1`
  - 教师：`U-TA1`
  - 学生：`U-ST1`
  - 开课助教：`mcp-r2-mq6z7s5j-yz44k-offering-ta`
  - 班级助教：`mcp-r2-mq6z7s5j-yz44k-class-ta`
- 路线：
  1. 管理员复核平台配置、用户、开课详情、审计日志。
  2. 教师复核课程工作区、资源、作业、提交、成绩册、实验页。
  3. 学生复核学习中心、WebIDE、实验、成绩。
  4. 开课助教和班级助教复核授权课程/班级页面。
- 结果：主线页面均可打开，学生 WebIDE、实验、成绩和助教授权边界可演示。
- 失败或阻塞：管理员/教师段的第一次 MCP 执行超过单次工具 120 秒上限，但截图已在超时前落盘；随后用短段补齐教师实验、学生和助教主线。该工具超时不代表页面失败，但记录为执行风险。
- 证据：
  - `077-r2-rehearsal2-admin-platform-config.png`
  - `078-r2-rehearsal2-admin-users.png`
  - `079-r2-rehearsal2-admin-offering-detail.png`
  - `080-r2-rehearsal2-admin-audit-logs.png`
  - `081-r2-rehearsal2-teacher-course.png`
  - `082-r2-rehearsal2-teacher-resources.png`
  - `083-r2-rehearsal2-teacher-assignments.png`
  - `084-r2-rehearsal2-teacher-submissions.png`
  - `085-r2-rehearsal2-teacher-gradebook.png`
  - `086-r2-rehearsal2-teacher-labs.png`
  - `086-r2-rehearsal2-student-dashboard.png`
  - `087-r2-rehearsal2-student-webide.png`
  - `088-r2-rehearsal2-student-labs.png`
  - `089-r2-rehearsal2-student-grades.png`
  - `090-r2-rehearsal2-offering-ta-course.png`
  - `091-r2-rehearsal2-class-ta-members.png`

### 彩排 3

- 状态：通过主线，发现 P2
- 开始时间：2026-06-10 12:54 CST
- 结束时间：2026-06-10 12:57 CST
- 账号：
  - 管理员：`U-SA1`
  - 教师：`U-TA1`
  - 学生：`U-ST1`
  - 开课助教：`mcp-r2-mq6z7s5j-yz44k-offering-ta`
  - 班级助教：`mcp-r2-mq6z7s5j-yz44k-class-ta`
- 路线：
  1. 管理员登录并复核治理、组织、用户、权限解释。
  2. 教师登录并复核教学工作台、课程工作区、题库、作业、提交、实验。
  3. 学生登录并复核学习中心、WebIDE、自测、实验、成绩、通知、管理员区禁止。
  4. 助教登录并复核授权课程、未授权课程、管理员区禁止和班级成员页。
  5. 故障预案演练：不存在课程 ID `999999` 和未授权课程 ID `5`。
- 结果：管理员、教师、学生、助教主线可演示；WebIDE 自测显示 `ACCEPTED`；权限禁止主线生效。
- 失败或阻塞：
  - 未授权课程 ID `5` 页面正确显示“当前用户无权查看教学班”，但仍展示快捷入口，记为 P2-R2-002。
  - 不存在课程 ID `999999` 页面停留“加载中...”并展示快捷入口，记为 P2-R2-003。
  - 写入类强制动作仍未形成完整 MCP 主证据，保留为阻塞。
- 证据：
  - `092-r2-rehearsal3-admin-dashboard.png`
  - `093-r2-rehearsal3-admin-org-units.png`
  - `094-r2-rehearsal3-admin-users.png`
  - `095-r2-rehearsal3-admin-auth-explain.png`
  - `096-r2-rehearsal3-teacher-dashboard.png`
  - `097-r2-rehearsal3-teacher-course.png`
  - `098-r2-rehearsal3-teacher-question-bank.png`
  - `099-r2-rehearsal3-teacher-assignments.png`
  - `100-r2-rehearsal3-teacher-submissions.png`
  - `101-r2-rehearsal3-teacher-labs.png`
  - `102-r2-rehearsal3-student-dashboard.png`
  - `103-r2-rehearsal3-student-webide.png`
  - `104-r2-rehearsal3-student-webide-run.png`
  - `105-r2-rehearsal3-student-labs.png`
  - `106-r2-rehearsal3-student-grades.png`
  - `107-r2-rehearsal3-me-notifications.png`
  - `108-r2-rehearsal3-student-forbidden-admin.png`
  - `109-r2-rehearsal3-offering-ta-course.png`
  - `110-r2-rehearsal3-offering-ta-invalid-course.png`
  - `111-r2-rehearsal3-offering-ta-unauthorized-course.png`
  - `112-r2-rehearsal3-offering-ta-forbidden-admin.png`
  - `113-r2-rehearsal3-class-ta-members.png`
  - `114-r2-rehearsal3-class-ta-forbidden-admin.png`
