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

## 3. P0 阻塞问题

无。

## 4. P1 高优先级问题

无。

## 5. P2 体验问题

- [x] P2-R2-001 登录空表单缺少新增可见错误说明
- [x] P2-R2-002 未授权开课上下文仍展示快捷入口
- [x] P2-R2-003 不存在课程 ID 页面停留加载态并展示快捷入口

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

## 8. 第三阶段补证记录

本节记录不需要应用代码修改、但第二轮清单中仍缺少 MCP 主证据的补漏验证。

| 清单编号 | 状态 | MCP 操作 | 证据 |
| --- | --- | --- | --- |
| TEACHER-005 | 已补证 | 以教师账号打开 `/teacher/courses/2/announcements`，新建公告 `MCP-R2-20260610-143804`，提交后列表第一条显示新公告。 | `125-r2-teacher-announcement-created.png`；`product-full-verification-round2-evidence/runtime/teacher-announcement-create-network.txt` |
| TEACHER-007 | 已补证 | 以教师账号打开 `/teacher/courses/2/discussions?offeringId=2`，新建讨论 `MCP-R2-20260610-145754 教师讨论补证`，提交后列表第一条显示新讨论。 | `128-r2-teacher-discussion-created.png`；`product-full-verification-round2-evidence/runtime/teacher-discussion-create-network.txt` |
| TEACHER-008 | 已补证 | 以教师账号打开 `/teacher/courses/2/discussions/36?offeringId=2` 发布教师回复；随后从讨论列表锁定该讨论，详情页显示“已锁定”且发布按钮禁用。 | `129-r2-teacher-discussion-reply-visible.png`；`130-r2-teacher-discussion-reply-posted.png`；`132-r2-teacher-discussion-locked-list.png`；`133-r2-teacher-discussion-locked-detail.png`；`product-full-verification-round2-evidence/runtime/teacher-discussion-reply-network.txt`；`product-full-verification-round2-evidence/runtime/teacher-discussion-lock-network.txt` |
| TEACHER-019 | 已补证 | 以教师账号打开 `/teacher/notifications`，点击“全部已读”，顶部未读徽标从 9 清零。 | `123-r2-teacher-notifications-before-read-all.png`；`124-r2-teacher-notifications-after-read-all.png`；`product-full-verification-round2-evidence/runtime/teacher-notifications-after-network.txt` |
| STUDENT-004 | 已补证 | 以学生账号打开 `/student/courses/2/discussions/36`，确认教师新建讨论和教师回复可见，发布 `学生回复补证：MCP-R2-20260610-1537。` 后详情页回写学生回复。 | `131-r2-student-discussion-reply-posted.png`；`product-full-verification-round2-evidence/runtime/student-discussion-reply-network.txt` |
| STUDENT-018 | 已补证 | 以学生账号打开 `/student/notifications`，对 `MCP-R2-20260610-143804` 公告通知点击“标记已读”，顶部未读徽标从 32 降到 31，目标行按钮消失。 | `126-r2-student-notification-before-mark-read.png`；`127-r2-student-notification-after-mark-read.png`；`product-full-verification-round2-evidence/runtime/student-notifications-after-mark-read-network.txt` |
| RUNTIME-005 | 已补证 | 保存通知相关 Playwright MCP 网络摘要，覆盖通知流、未读数、全部已读和单条已读请求。 | `teacher-notifications-after-network.txt`；`student-notifications-after-mark-read-network.txt` |
