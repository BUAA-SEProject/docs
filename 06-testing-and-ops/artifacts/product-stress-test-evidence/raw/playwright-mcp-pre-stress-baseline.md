# Playwright MCP 压测前页面基线

- 执行时间：2026-06-11 13:14-13:15 CST
- 目标前端：`http://127.0.0.1:3000`
- 目标后端：`http://127.0.0.1:18080`
- 执行方式：Playwright MCP 操作真实登录页和真实本地前后端页面。
- 账号范围：本地 E2E 管理员 `U-SA1`、教师 `U-TA1`、学生 `U-ST1`；本记录不保存密码。
- Console 结果：`product-stress-test-evidence/raw/playwright-mcp-pre-stress-console.log`，warning/error 数量为 0。
- Network 结果：`product-stress-test-evidence/raw/playwright-mcp-pre-stress-network.log`；未观察到 5xx。页面切换和清理 session 期间存在 SSE/请求 `net::ERR_ABORTED`，属于导航中断，不作为后端 5xx。

## 截图清单

| 页面 | 路径 | 截图 |
| --- | --- | --- |
| 登录页 | `/login` | `product-stress-test-screenshots/pre-00-login.png` |
| 管理员首页 | `/admin` | `product-stress-test-screenshots/pre-01-admin-home.png` |
| 管理员用户管理 | `/admin/users` | `product-stress-test-screenshots/pre-02-admin-users.png` |
| 教师首页 | `/teacher` | `product-stress-test-screenshots/pre-03-teacher-home.png` |
| 教师课程列表 | `/teacher/courses` | `product-stress-test-screenshots/pre-04-teacher-courses.png` |
| 教师通知中心 | `/teacher/notifications` | `product-stress-test-screenshots/pre-05-teacher-notifications.png` |
| 学生首页 | `/student` | `product-stress-test-screenshots/pre-06-student-home.png` |
| 学生作业列表 | `/student/assignments` | `product-stress-test-screenshots/pre-07-student-assignments.png` |
| 学生实验列表 | `/student/labs` | `product-stress-test-screenshots/pre-08-student-labs.png` |
| 学生通知中心 | `/student/notifications` | `product-stress-test-screenshots/pre-09-student-notifications.png` |
