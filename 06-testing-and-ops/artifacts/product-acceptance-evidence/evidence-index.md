# 产品验收证据索引

- 验收时间：2026-06-09 16:10-16:50 CST
- 工作区：`/Users/moorefoss/Code/AUBB`
- 报告：`docs/06-testing-and-ops/artifacts/product-acceptance-report.md`
- 截图目录：`docs/06-testing-and-ops/artifacts/product-acceptance-screenshots/`
- 凭据处理：仅记录测试账号标识，不记录密码、token 或连接串值。

## 命令门禁

| 命令 | 结果 | 证据摘要 |
| --- | --- | --- |
| `just status` | 通过 | 初始 `server/`、`web/`、`docs/` 均 clean |
| `just --list` | 通过 | 统一入口包含 dev、healthcheck、seed、e2e、verify、docs-build |
| `just dev-up` | 通过 | Docker 依赖、后端 18080、前端 3000 可用 |
| `just healthcheck-strict` | 通过 | 工具、env、端口、readiness、OpenAPI、login 探针均 OK |
| `server/scripts/ops/e2e-residual-cleanup.sh` | 通过 | dry-run 命中 0，未执行删除 |
| `just seed-fixtures` | 通过 | 22/22 fixture cases passed |
| `just e2e-real` | 失败 | 50 tests，48 passed，2 failed |
| `just verify` | 通过 | 后端 356 tests 通过；web lint/typecheck 通过；docs build 通过 |
| `just verify-full` | 通过 | 后端 verify、web lint/typecheck/unit/build、docs build 全通过 |
| `cd docs && npm run docs:build` | 通过 | VitePress build complete |

## Playwright MCP 截图

| 文件 | 页面或证据 |
| --- | --- |
| `mcp-01-admin-home.png` | 管理员工作台 |
| `mcp-02-admin-users.png` | 管理员用户管理 |
| `mcp-03-admin-org-units.png` | 管理员组织架构 |
| `mcp-04-admin-course-offerings.png` | 管理员开课管理 |
| `mcp-05-admin-auth-explain.png` | 管理员权限解释 |
| `mcp-06-admin-audit-logs.png` | 管理员审计日志 |
| `mcp-07-admin-platform-config.png` | 管理员平台配置 |
| `mcp-08-teacher-home.png` | 教师工作台 |
| `mcp-09-teacher-courses.png` | 教师我的课程 |
| `mcp-10-teacher-assignments.png` | 教师全部作业 |
| `mcp-11-teacher-submissions.png` | 教师全部提交 |
| `mcp-12-teacher-gradebook.png` | 教师成绩册 |
| `mcp-13-teacher-question-bank.png` | 教师题库中心 |
| `mcp-14-teacher-labs.png` | 教师实验中心 |
| `mcp-15-teacher-notifications.png` | 教师通知中心 |
| `mcp-16-teacher-forbidden-admin-users.png` | 教师越权访问管理端 |
| `mcp-17-student-home.png` | 学生学习中心 |
| `mcp-18-student-courses.png` | 学生课程 |
| `mcp-19-student-assignments.png` | 学生全部作业，显示“继续作答” |
| `mcp-20-student-assignment-detail.png` | 学生作业详情 |
| `mcp-22-student-grades.png` | 学生成绩 |
| `mcp-23-student-labs.png` | 学生实验 |
| `mcp-24-student-notifications.png` | 学生通知 |
| `mcp-25-student-forbidden-admin.png` | 学生越权访问管理端 |
| `mcp-26-responsive-admin-users-1280.png` | 1280x800 管理员用户页 |
| `mcp-27-responsive-1440-route-guard.png` | 1440x900 越权路由守卫观察 |
| `mcp-28-responsive-student-assignments-mobile.png` | 390x844 学生作业页 |
| `mcp-29-responsive-teacher-labs-1440.png` | 1440x900 教师实验页 |

## 失败证据

- P1-001：`web/test-results/assignment-submission-assi-04c46-or-the-active-fixture-class-chromium/error-context.md`
- P1-001 trace：`web/test-results/assignment-submission-assi-04c46-or-the-active-fixture-class-chromium/trace.zip`
- P1-002：`web/test-results/full-organization-structur-753bf-ember-management-through-UI-chromium/error-context.md`
- P1-002 trace：`web/test-results/full-organization-structur-753bf-ember-management-through-UI-chromium/trace.zip`
- E2E 覆盖摘要：`web/test-results/full-e2e-coverage.md`

## 未覆盖

- 未执行 3 次完整演示彩排。
- 未构造 profile-required 专用账号做页面级复核。
- WebIDE 完整闭环由真实 UI E2E 覆盖，未在 MCP 截图中重新捕获工作区页面。
