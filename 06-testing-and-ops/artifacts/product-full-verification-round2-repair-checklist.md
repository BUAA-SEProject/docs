# AUBB 产品全功能交付修复清单

## 1. 修复元信息

- 修复开始时间：2026-06-10 13:35 CST
- 修复阶段：第三阶段
- 依据报告：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-report.md`
- 依据功能清单：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-feature-inventory.md`
- 依据彩排记录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-rehearsal-log.md`
- 初始 `just status` 摘要：`server/`、`web/`、`docs/` 均 clean；`server` ahead 1，`web` ahead 1，`docs` ahead 6。

## 2. 修复总览

| 编号 | 级别 | 角色 | 问题摘要 | 状态 | 回归证据 |
| --- | --- | --- | --- | --- | --- |
| P2-R2-001 | P2 | 无登录用户 | 登录空表单缺少新增可见错误说明 | 已回归 | `116-r2-repair-login-empty-submit.png` |
| P2-R2-002 | P2 | 开课助教 | 未授权开课上下文仍展示快捷入口 | 已回归 | `117-r2-repair-offering-ta-unauthorized-course.png` |
| P2-R2-003 | P2 | 开课助教 | 不存在课程 ID 页面停留加载态并展示快捷入口 | 已回归 | `118-r2-repair-offering-ta-invalid-course.png` |
| P1-R2-004 | P1 | 学生 | 实验报告评阅发布后学生端未显示教师评语 | 已回归 | `154-r2-student-lab-report-feedback-visible.png` |
| P2-R2-005 | P2 | 学生 | 报告型实验误请求运行时 current session 产生 400 网络噪音 | 已回归 | MCP 网络观察未再出现 `/api/v1/me/labs/52/sessions/current` |
| P1-R2-006 | P1 | 学生 | 编程正式提交后提交详情页不自动刷新判题终态 | 已回归 | `164-r2-student-programming-polling-assignment-before-submit.png`；`165-r2-student-programming-polling-submit-accepted.png`；`student-programming-polling-submit-57-network.txt` |
| P2-R2-007 | P2 | 教师 | 添加课程成员成功后弹窗不关闭且列表不刷新 | 已回归 | `173-r2-teacher-members-add-import-visible.png`；`teacher-members-add-import-status-network.txt` |

## 3. P0 阻塞问题

- [x] P1-R2-004 实验报告评阅发布后学生端未显示教师评语

## 4. P1 高优先级问题

- [x] P1-R2-006 编程正式提交后提交详情页不自动刷新判题终态

## 5. P2 体验问题

- [x] P2-R2-001 登录空表单缺少新增可见错误说明
- [x] P2-R2-002 未授权开课上下文仍展示快捷入口
- [x] P2-R2-003 不存在课程 ID 页面停留加载态并展示快捷入口
- [x] P2-R2-005 报告型实验误请求运行时 current session 产生 400 网络噪音
- [x] P2-R2-007 添加课程成员成功后弹窗不关闭且列表不刷新

## 6. P3 优化项

无。

## 7. 每项修复记录

### P2-R2-001 登录空表单缺少新增可见错误说明

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P2-R2-001。
- 修复状态：已回归
- 修改文件：
  - `web/src/features/auth/components/login-form.tsx`
  - `web/src/tests/unit/auth/login-form.test.tsx`
- 修复说明：登录表单启用 `noValidate` 并移除原生 `required`，空提交由应用内校验显示统一错误区，同时保持输入框 `aria-invalid`。
- Playwright MCP 回归：
  - 页面：`/login`
  - 账号：无登录用户
  - 步骤：打开登录页，不输入用户名和密码，点击“立即登录”。
  - 结果：页面显示“请输入用户名和密码”，用户名和密码输入框均为 invalid。
  - 截图：`product-full-verification-round2-screenshots/116-r2-repair-login-empty-submit.png`
- 命令验证：
  - 命令：`cd web && npm test -- src/tests/unit/auth/login-form.test.tsx src/tests/unit/course/teacher-course-dashboard-page.test.tsx`、`npm run lint`、`npm run typecheck`、`npm run build`、根目录 `just verify`、`cd docs && npm run docs:build`
  - 结果：定向单测 2 files / 11 tests passed；web lint/typecheck/build 通过；`just verify` 通过，后端 357 tests / 0 failures，web lint/typecheck 和 docs build 通过；docs build 单独通过。
- Commit：`web` `5ea8296 fix(frontend): 修复登录与课程错误态`；`docs` 为本清单所在提交。
- 剩余风险：无登录主线风险；空表单错误文案为统一全局错误区，未拆成字段旁两条错误。

### P2-R2-002 未授权开课上下文仍展示快捷入口

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P2-R2-002。
- 修复状态：已回归
- 修改文件：
  - `web/src/app/(teacher)/teacher/courses/[offeringId]/page.tsx`
  - `web/src/features/course/hooks/use-teaching-query.ts`
  - `web/src/tests/unit/course/teacher-course-dashboard-page.test.tsx`
- 修复说明：课程工作区先用 `useMyCoursesQuery()` 确认当前开课在授权课程范围内；未命中时渲染页面级“无法访问该课程”状态，隐藏教学班区和快捷操作。
- Playwright MCP 回归：
  - 页面：`/teacher/courses/5`
  - 账号：开课助教
  - 步骤：以开课助教登录，直接打开未授权开课 ID `5`。
  - 结果：页面显示“无法访问该课程”，未显示“快捷操作”“发布全课公告”“上传课程资源”“管理本课作业”。
  - 截图：`product-full-verification-round2-screenshots/117-r2-repair-offering-ta-unauthorized-course.png`
- 命令验证：
  - 命令：`cd web && npm test -- src/tests/unit/auth/login-form.test.tsx src/tests/unit/course/teacher-course-dashboard-page.test.tsx`、`npm run lint`、`npm run typecheck`、`npm run build`、根目录 `just verify`、`cd docs && npm run docs:build`
  - 结果：定向单测 2 files / 11 tests passed；web lint/typecheck/build 通过；`just verify` 通过，后端 357 tests / 0 failures，web lint/typecheck 和 docs build 通过；docs build 单独通过。
- Commit：`web` `5ea8296 fix(frontend): 修复登录与课程错误态`；`docs` 为本清单所在提交。
- 剩余风险：该页面使用“我的课程”清单判断当前课程上下文，若清单接口异常则显示同一课程不可访问错误态并提供重试。

### P2-R2-003 不存在课程 ID 页面停留加载态并展示快捷入口

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P2-R2-003。
- 修复状态：已回归
- 修改文件：
  - `web/src/app/(teacher)/teacher/courses/[offeringId]/page.tsx`
  - `web/src/features/course/hooks/use-teaching-query.ts`
  - `web/src/tests/unit/course/teacher-course-dashboard-page.test.tsx`
- 修复说明：课程清单已加载但找不到当前 `offeringId` 时直接渲染不可访问态；教学班查询增加可选 `enabled`，仅在课程上下文确认后启用。
- Playwright MCP 回归：
  - 页面：`/teacher/courses/999999`
  - 账号：开课助教
  - 步骤：以开课助教登录，直接打开不存在课程 ID `999999`。
  - 结果：页面显示“无法访问该课程”，未停留“加载中...”，未显示快捷操作。
  - 截图：`product-full-verification-round2-screenshots/118-r2-repair-offering-ta-invalid-course.png`
- 命令验证：
  - 命令：`cd web && npm test -- src/tests/unit/auth/login-form.test.tsx src/tests/unit/course/teacher-course-dashboard-page.test.tsx`、`npm run lint`、`npm run typecheck`、`npm run build`、根目录 `just verify`、`cd docs && npm run docs:build`
  - 结果：定向单测 2 files / 11 tests passed；web lint/typecheck/build 通过；`just verify` 通过，后端 357 tests / 0 failures，web lint/typecheck 和 docs build 通过；docs build 单独通过。
- Commit：`web` `5ea8296 fix(frontend): 修复登录与课程错误态`；`docs` 为本清单所在提交。
- 剩余风险：同 P2-R2-002；不存在和未授权课程共用统一不可访问文案。

### P1-R2-004 实验报告评阅发布后学生端未显示教师评语

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P1-R2-004。
- 修复状态：已回归
- 修改文件：
  - `web/src/app/(student)/student/labs/page.tsx`
  - `web/src/tests/unit/lab/student-labs-page.test.tsx`
- 修复说明：学生实验报告页面在报告状态为 `PUBLISHED` 且后端返回教师评语或批注时，显示“教师评语”反馈区；补充单测覆盖发布后反馈可见。
- Playwright MCP 回归：
  - 页面：`/student/labs?classId=2&offeringId=2`
  - 账号：学生 `U-ST1`
  - 步骤：教师创建并发布报告型实验 `52`，学生提交报告 `21`，教师保存并发布评阅；学生重新打开同一实验。
  - 结果：学生端显示 `已发布` 状态、附件和 `MCP-R2 教师评阅补证：报告内容完整，附件可下载，草稿、附件和正式提交链路已核验。`
  - 截图：`product-full-verification-round2-screenshots/154-r2-student-lab-report-feedback-visible.png`
- 命令验证：
  - 命令：`cd web && npm test -- src/tests/unit/lab/student-labs-page.test.tsx`
  - 结果：6 tests passed。
- Commit：`web` `1618469 fix(lab): 显示实验报告教师反馈`；`docs` 为本清单所在提交。
- 剩余风险：学生端仅在后端报告状态为 `PUBLISHED` 时显示教师反馈；未发布的 `REVIEWED` 状态按产品规格不对学生展示评语。

### P2-R2-005 报告型实验误请求运行时 current session 产生 400 网络噪音

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P2-R2-005。
- 修复状态：已回归
- 修改文件：
  - `web/src/app/(student)/student/labs/page.tsx`
  - `web/src/tests/unit/lab/student-labs-page.test.tsx`
- 修复说明：学生实验页仅在选中实验类型为 `TERMINAL` 时启用当前运行时会话查询；报告型实验仍保留报告正文、附件和教师反馈链路，但不再请求 `/sessions/current`。
- Playwright MCP 回归：
  - 页面：`/student/labs?classId=2&offeringId=2`
  - 账号：学生 `U-ST1`
  - 步骤：打开学生实验页，选择报告型实验 `MCP-R2-20260610-164443 报告实验补证`。
  - 结果：页面显示教师评语；MCP 网络观察中实验相关请求只有 `GET /api/v1/me/labs/52/report` 200，未再出现 `GET /api/v1/me/labs/52/sessions/current`。
- 命令验证：
  - 命令：`cd web && npm test -- src/tests/unit/lab/student-labs-page.test.tsx`
  - 结果：6 tests passed，其中新增单测覆盖报告型实验不查询 runtime session。
- Commit：`web` `1618469 fix(lab): 显示实验报告教师反馈`；`docs` 为本清单所在提交。
- 剩余风险：终端型实验仍按原逻辑查询 current session；报告型实验不展示运行时状态。

### P1-R2-006 编程正式提交后提交详情页不自动刷新判题终态

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P1-R2-006。
- 修复状态：已回归
- 修改文件：
  - `web/src/app/(student)/student/submissions/[submissionId]/page.tsx`
  - `web/src/features/judge/hooks/use-judge-query.ts`
  - `web/src/tests/unit/submission/student-submission-detail-page.test.tsx`
- 修复说明：学生提交详情页在存在 `PENDING` / `RUNNING` 判题任务时每 3 秒轮询 judge jobs；当判题任务从运行态进入终态后刷新提交详情，确保答案分数和反馈自动回填，并在终态后停止轮询。
- Playwright MCP 回归：
  - 页面：`/student/assignments/260?offeringId=2&classId=2`、`/student/submissions/57?offeringId=2&classId=2&assignmentId=260`
  - 账号：学生 `U-ST1`
  - 步骤：创建临时编程作业 `260`，模板代码包含短暂 `sleep` 以保持运行中状态；学生从作业详情点击“提交答案”，进入提交 `57` 详情页等待。
  - 结果：无需手动刷新，页面自动显示 `ACCEPTED / 100 分`；网络摘要包含 3 次 `GET /api/v1/me/submissions/57/judge-jobs`，随后自动请求 `GET /api/v1/me/submissions/57`。
  - 截图：`product-full-verification-round2-screenshots/164-r2-student-programming-polling-assignment-before-submit.png`；`product-full-verification-round2-screenshots/165-r2-student-programming-polling-submit-accepted.png`
- 命令验证：
  - 命令：`npm test -- src/tests/unit/submission/student-submission-detail-page.test.tsx`、`npm run lint`、`npm run typecheck`、`npm run build`、根目录 `just verify`、`cd docs && npm run docs:build`
  - 结果：学生提交详情页定向单测 1 file / 5 tests passed；web lint/typecheck/build 通过；`just verify` 通过，后端 357 tests / 0 failures，web lint/typecheck 和 docs build 通过；docs build 单独通过。
- Commit：`web` `e4b0f21 fix(judge): 自动刷新学生判题结果`；`docs` 为本清单所在提交。
- 剩余风险：临时作业 `260` 与提交 `57` 为本轮回归残留测试数据；不污染固定演示作业 `7`。

### P2-R2-007 添加课程成员成功后弹窗不关闭且列表不刷新

- 报告链接或位置：`product-full-verification-round2-report.md` 缺陷详情 P2-R2-007。
- 修复状态：已回归
- 修改文件：
  - `web/src/app/(teacher)/teacher/courses/[offeringId]/members/page.tsx`
  - `web/src/shared/api/query-keys.ts`
  - `web/src/tests/unit/course/teacher-members-page.test.tsx`
  - `web/src/tests/unit/api/query-keys.contract.test.ts`
- 修复说明：添加成员 mutation 成功后关闭弹窗并主动刷新当前成员列表；课程列表类 query key 在省略筛选参数时返回前缀 key，确保成员、公告、资源和讨论列表 mutation 能正确失效带筛选参数的查询。
- Playwright MCP 回归：
  - 页面：`/teacher/courses/32/members`
  - 账号：开课 `32` 的授课教师
  - 步骤：点击“添加成员”，填写用户 ID `393`，选择 `MCP-R2-06102037 教学班` 后提交；随后通过 CSV 导入 `mcp-r2-0610205203-member-import`，并对该导入成员执行停用和恢复。
  - 结果：添加成功后弹窗关闭，成员列表自动显示 `MCP-R2-0610210555-member-add-fixed`；CSV 导入后列表显示 `MCP-R2-0610205203-member-import`；停用后目标行显示“已停用/恢复”，恢复后回到“已激活/停用”。
  - 截图：`product-full-verification-round2-screenshots/173-r2-teacher-members-add-import-visible.png`；`product-full-verification-round2-screenshots/174-r2-teacher-member-status-dropped.png`；`product-full-verification-round2-screenshots/175-r2-teacher-member-status-restored.png`
  - 网络：`product-full-verification-round2-evidence/runtime/teacher-members-add-import-status-network.txt`，包含 `POST /members/batch` 200、`POST /members/import` 200、两次 `PATCH /members/454/status` 200。
  - 控制台：`product-full-verification-round2-evidence/runtime/teacher-members-add-import-status-console.txt`，warning/error 为 0。
- 命令验证：
  - 命令：`npm test -- src/tests/unit/course/teacher-members-page.test.tsx`、`npm test -- src/tests/unit/api/query-keys.contract.test.ts`
  - 结果：成员页定向单测 1 file / 7 tests passed；query key 契约单测 1 file / 6 tests passed。
- Commit：待本轮提交。
- 剩余风险：本轮留下临时开课 `32`、教学班 `234` 和临时成员账号作为补证数据；未污染固定演示课程 `2`。

## 8. 第三阶段补证记录

本节记录第二轮清单中仍缺少 MCP 主证据的补漏验证；若补证中发现并修复代码问题，对应缺陷记录见第 7 节。

| 清单编号 | 状态 | MCP 操作 | 证据 |
| --- | --- | --- | --- |
| ADMIN-002 | 已补证 | 以管理员账号打开 `/admin/platform-config`，将页脚文字从 `© 2026 AUBB Team` 临时保存为 `© 2026 AUBB Team · MCP-R2-ADMIN-0610`，随后恢复原值并再次保存；页面保持在平台配置表单，最终字段值已回到原值。 | `166-r2-admin-platform-config-saved-marker.png`；`167-r2-admin-platform-config-restored.png`；`product-full-verification-round2-evidence/runtime/admin-platform-config-save-restore-network.txt`；`product-full-verification-round2-evidence/runtime/admin-platform-config-save-restore-console.txt` |
| ADMIN-003 | 已补证 | 以管理员账号打开 `/admin/org-units`，在学校根节点下新建学院 `MCP-R2-06101946 学院` / `MCP-R2-COL-06101946`；提交后树列表显示新节点。当前稳定接口清单仅包含 `POST /api/v1/admin/org-units`，页面未提供组织节点编辑入口。 | `168-r2-admin-org-unit-created.png`；`product-full-verification-round2-evidence/runtime/admin-org-unit-create-network.txt`；`product-full-verification-round2-evidence/runtime/admin-org-unit-create-console.txt` |
| ADMIN-006 | 已补证 | 以管理员账号打开 `/admin/academic-terms`，创建学期 `MCP-R2-06101952 学期` / `MCP-R2-TERM-06101952`；随后点击该行“编辑学期”，将名称改为 `MCP-R2-06101952 学期-EDIT` 并保存。 | `169-r2-admin-academic-term-created-edited.png`；`product-full-verification-round2-evidence/runtime/admin-academic-term-create-edit-network.txt`；`product-full-verification-round2-evidence/runtime/admin-academic-term-create-edit-console.txt` |
| ADMIN-007 | 已补证 | 以管理员账号打开 `/admin/course-catalogs`，创建课程模板 `MCP-R2-06102000 课程模板` / `MCP-R2-CAT-06102000`；随后点击该行“编辑”，将名称改为 `MCP-R2-06102000 课程模板-EDIT` 并保存。 | `170-r2-admin-course-catalog-created-edited.png`；`product-full-verification-round2-evidence/runtime/admin-course-catalog-create-edit-network.txt`；`product-full-verification-round2-evidence/runtime/admin-course-catalog-create-edit-console.txt` |
| ADMIN-008 | 已补证 | 以管理员账号打开 `/admin/course-offerings`，基于课程模板 `MCP-R2-06102000 课程模板-EDIT` 创建开课 `MCP-R2-06102015 开课实例` / `MCP-R2-OFF-06102015`；主开课学院由模板自动锁定为 `MCP-R2-06101946 学院`，共同管理学院选择 `E2EMQ56QUX7DG2EVPORG-共管学院`，主讲教师选择 `e2emq6yao1yyb2we2org-offering-teacher`；随后进入开课 `32` 详情，将名称改为 `MCP-R2-06102015 开课实例-EDIT`、容量改为 `60` 并保存。 | `171-r2-admin-course-offering-created-edited.png`；`product-full-verification-round2-evidence/runtime/admin-course-offering-create-edit-network.txt`；`product-full-verification-round2-evidence/runtime/admin-course-offering-create-edit-console.txt` |
| TEACHER-003-CLASS | 已补证 | 以开课 `32` 的授课教师账号打开 `/teacher/courses/32`，在课程工作台填写班级名称 `MCP-R2-06102037 教学班`、班级编码 `MCP-R2-CLS-06102037` 并点击“创建班级”；页面列表显示新教学班，后端返回教学班 ID `234`。 | `172-r2-teacher-teaching-class-created.png`；`product-full-verification-round2-evidence/runtime/teacher-teaching-class-create-network.txt`；`product-full-verification-round2-evidence/runtime/teacher-teaching-class-create-console.txt` |
| TEACHER-004 | 已补证 | 以开课 `32` 的授课教师账号打开 `/teacher/courses/32/members`，通过“添加成员”添加学生 `mcp-r2-0610210555-member-add-fixed`；通过 CSV `teacher-members-import-mcp-r2-0610205203.csv` 导入 `mcp-r2-0610205203-member-import`；随后对导入成员执行停用和恢复。补证中发现并修复 P2-R2-007。 | `173-r2-teacher-members-add-import-visible.png`；`174-r2-teacher-member-status-dropped.png`；`175-r2-teacher-member-status-restored.png`；`product-full-verification-round2-evidence/runtime/teacher-members-add-import-status-network.txt`；`product-full-verification-round2-evidence/runtime/teacher-members-add-import-status-console.txt` |
| TEACHER-005 | 已补证 | 以教师账号打开 `/teacher/courses/2/announcements`，新建公告 `MCP-R2-20260610-143804`，提交后列表第一条显示新公告。 | `125-r2-teacher-announcement-created.png`；`product-full-verification-round2-evidence/runtime/teacher-announcement-create-network.txt` |
| TEACHER-006 | 已补证 | 以教师账号打开 `/teacher/courses/2/resources?offeringId=2`，在“上传资源”弹窗填写标题 `MCP-R2-20260610-1553 教师资源补证` 和说明，选择 `teacher-resource-upload-sample.md` 后提交；列表显示新资源、大小、上传时间和下载入口，并下载同一文件校验哈希。 | `134-r2-teacher-resource-uploaded.png`；`product-full-verification-round2-evidence/runtime/teacher-resource-upload-network.txt`；`product-full-verification-round2-evidence/runtime/teacher-resource-upload-sha256.txt` |
| TEACHER-007 | 已补证 | 以教师账号打开 `/teacher/courses/2/discussions?offeringId=2`，新建讨论 `MCP-R2-20260610-145754 教师讨论补证`，提交后列表第一条显示新讨论。 | `128-r2-teacher-discussion-created.png`；`product-full-verification-round2-evidence/runtime/teacher-discussion-create-network.txt` |
| TEACHER-009 | 已补证 | 以教师账号打开 `/teacher/courses/2/question-bank?offeringId=2`，点击“新增题目”，创建简答题 `MCP-R2-20260610-1605 简答题补证`；提交后列表第一行显示题目标题、分类、标签和默认分值。 | `135-r2-teacher-question-bank-created.png`；`product-full-verification-round2-evidence/runtime/teacher-question-bank-create-network.txt` |
| TEACHER-009-STRUCTURED | 已补证 | 以教师账号继续在课程题库新增单选、多选、填空、文件题，作为结构化作业题目来源。 | `137-r2-teacher-question-bank-structured-types-created.png`；`product-full-verification-round2-evidence/runtime/teacher-question-bank-structured-types-network.txt` |
| TEACHER-010 | 已补证 | 以教师账号打开 `/teacher/courses/2/judge-environments?offeringId=2`，点击“新增配置”，创建 `MCP-R2-20260610-1611 Python3 判题环境补证`；提交后列表显示新配置、语言、运行环境和可用状态。 | `136-r2-teacher-judge-environment-created.png`；`product-full-verification-round2-evidence/runtime/teacher-judge-environment-create-network.txt` |
| TEACHER-012 | 已补证 | 以教师账号打开 `/teacher/assignments/create?offeringId=2`，创建结构化作业 `259`，包含单选、多选、填空、文件题并发布。 | `138-r2-teacher-assignment-create-filled.png`；`139-r2-teacher-assignment-published.png`；`teacher-assignment-create-network.txt`；`teacher-assignment-publish-network.txt` |
| TEACHER-015 | 已补证 | 以教师账号打开提交 `55`，查看学生结构化答案和文件题附件，为文件题保存人工分 `8` 与反馈。 | `142-r2-teacher-submission-55-before-grade.png`；`143-r2-teacher-submission-55-after-grade.png`；`teacher-submission-55-grade-network.txt` |
| TEACHER-016 | 已补证 | 以教师账号打开成绩册，发布作业 `259` 成绩。 | `144-r2-teacher-gradebook-259-before-publish.png`；`145-r2-teacher-gradebook-259-after-publish.png`；`teacher-gradebook-259-publish-network.txt` |
| TEACHER-018 | 已补证 | 以教师账号创建并发布报告型实验 `52`，打开学生报告 `21`，保存并发布评阅。 | `148-r2-teacher-report-lab-created-published.png`；`152-r2-teacher-lab-report-detail-before-review.png`；`153-r2-teacher-lab-report-reviewed-published.png`；`teacher-report-lab-create-publish-network.txt`；`teacher-lab-report-review-publish-network.txt` |
| TEACHER-008 | 已补证 | 以教师账号打开 `/teacher/courses/2/discussions/36?offeringId=2` 发布教师回复；随后从讨论列表锁定该讨论，详情页显示“已锁定”且发布按钮禁用。 | `129-r2-teacher-discussion-reply-visible.png`；`130-r2-teacher-discussion-reply-posted.png`；`132-r2-teacher-discussion-locked-list.png`；`133-r2-teacher-discussion-locked-detail.png`；`product-full-verification-round2-evidence/runtime/teacher-discussion-reply-network.txt`；`product-full-verification-round2-evidence/runtime/teacher-discussion-lock-network.txt` |
| TEACHER-019 | 已补证 | 以教师账号打开 `/teacher/notifications`，点击“全部已读”，顶部未读徽标从 9 清零。 | `123-r2-teacher-notifications-before-read-all.png`；`124-r2-teacher-notifications-after-read-all.png`；`product-full-verification-round2-evidence/runtime/teacher-notifications-after-network.txt` |
| STUDENT-004 | 已补证 | 以学生账号打开 `/student/courses/2/discussions/36`，确认教师新建讨论和教师回复可见，发布 `学生回复补证：MCP-R2-20260610-1537。` 后详情页回写学生回复。 | `131-r2-student-discussion-reply-posted.png`；`product-full-verification-round2-evidence/runtime/student-discussion-reply-network.txt` |
| STUDENT-007~011 | 已补证 | 以学生账号打开作业 `259`，提交单选 A、多选 A/B、填空“下载”和文件题附件；提交详情回显分题答案，附件下载 SHA256 与源文件一致。 | `140-r2-student-structured-assignment-filled.png`；`141-r2-student-structured-submission-detail.png`；`student-structured-submission-network.txt`；`student-structured-upload-sha256.txt` |
| STUDENT-016~017 | 已补证 | 教师发布作业 `259` 成绩后，学生成绩页显示 `23 / 23`、`已发布`、提交 `55`；学生提交详情显示教师文件题反馈。 | `146-r2-student-gradebook-259-published.png`；`147-r2-student-submission-55-feedback-visible.png`；`student-grade-feedback-259-network.txt` |
| STUDENT-021 | 已补证 | 以学生账号选择实验 `52`，填写 Markdown 报告、上传附件、保存草稿、正式提交；教师发布评阅后，学生端回查教师评语可见。 | `149-r2-student-lab-report-filled-attachment.png`；`150-r2-student-lab-report-draft-saved.png`；`151-r2-student-lab-report-submitted.png`；`154-r2-student-lab-report-feedback-visible.png`；`student-lab-report-submit-network.txt`；`student-lab-report-attachment-sha256.txt`；`student-lab-report-feedback-network.txt` |
| STUDENT-013 | 已补证 | 以学生账号打开 WebIDE `/student/assignments/7/workspace/11`，打开历史面板，预览 v6 后执行恢复，当前代码回到原始两行求和程序，并运行自测得到 `ACCEPTED`。 | `158-r2-student-webide-before-save.png`；`159-r2-student-webide-saved-probe.png`；`160-r2-student-webide-restored.png`；`161-r2-student-webide-restored-run-accepted.png`；`student-webide-save-restore-network.txt`；`student-webide-console-after-restore.txt` |
| STUDENT-015 | 已补证 | 以学生账号从作业详情 `/student/assignments/7` 点击“提交答案”，生成提交 `56`；修复前提交详情页等待后仍显示“运行中”，刷新后显示 `ACCEPTED / 100 分`。修复后使用临时作业 `260` 生成提交 `57`，详情页无需手动刷新自动显示 `ACCEPTED / 100 分`。 | `162-r2-student-programming-submit-accepted.png`；`164-r2-student-programming-polling-assignment-before-submit.png`；`165-r2-student-programming-polling-submit-accepted.png`；`student-programming-submit-56-network.txt`；`student-programming-polling-submit-57-network.txt`；`student-programming-polling-submit-57-console.txt` |
| STUDENT-019 | 已补证 | 以学生账号选择终端实验 `16`，从运行中状态点击“停止环境”后页面显示“未启动”，再点击“启动环境”后显示“运行中”。 | `155-r2-student-lab-session-running-before-stop.png`；`156-r2-student-lab-session-stopped.png`；`157-r2-student-lab-session-started.png`；`student-lab-session-stop-start-network.txt` |
| STUDENT-018 | 已补证 | 以学生账号打开 `/student/notifications`，对 `MCP-R2-20260610-143804` 公告通知点击“标记已读”，顶部未读徽标从 32 降到 31，目标行按钮消失。 | `126-r2-student-notification-before-mark-read.png`；`127-r2-student-notification-after-mark-read.png`；`product-full-verification-round2-evidence/runtime/student-notifications-after-mark-read-network.txt` |
| RUNTIME-005 | 已补证 | 保存通知相关 Playwright MCP 网络摘要，覆盖通知流、未读数、全部已读和单条已读请求。 | `teacher-notifications-after-network.txt`；`student-notifications-after-mark-read-network.txt` |
| RUNTIME-002 | 已补证 | 保存教师资源、学生文件题附件、学生实验报告附件和教师端实验报告附件下载哈希，证明上传下载一致。 | `teacher-resource-upload-sha256.txt`；`student-structured-upload-sha256.txt`；`student-lab-report-attachment-sha256.txt`；`teacher-lab-report-attachment-sha256.txt` |
