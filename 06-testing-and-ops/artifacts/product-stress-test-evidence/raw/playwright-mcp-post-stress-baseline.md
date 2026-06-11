# Playwright MCP 压测后页面回归

- 执行时间：2026-06-11 14:14-14:16 CST
- 目标前端：`http://127.0.0.1:3000`
- 目标后端：`http://127.0.0.1:18080`
- 执行方式：Playwright MCP 操作真实登录页和真实本地前后端页面。
- 账号范围：本地 E2E 管理员 `U-SA1`、教师 `U-TA1`、学生 `U-ST1`；本记录不保存密码。
- Console 结果：`product-stress-test-evidence/raw/playwright-mcp-post-stress-console.log`，warning/error 数量为 0。
- Network 结果：`product-stress-test-evidence/raw/playwright-mcp-post-stress-network.log`；MCP 监听期间未观察到 5xx。
- 配套命令健康检查：`product-stress-test-evidence/commands/19-healthcheck-strict-post-stress.log` 通过。

## 截图清单

| 页面 | 路径 | 截图 |
| --- | --- | --- |
| 登录页 | `/login` | `product-stress-test-screenshots/post-00-login.png` |
| 管理员首页 | `/admin` | `product-stress-test-screenshots/post-01-admin-home.png` |
| 管理员用户管理 | `/admin/users` | `product-stress-test-screenshots/post-02-admin-users.png` |
| 教师首页 | `/teacher` | `product-stress-test-screenshots/post-03-teacher-home.png` |
| 教师课程列表 | `/teacher/courses` | `product-stress-test-screenshots/post-04-teacher-courses.png` |
| 教师通知中心 | `/teacher/notifications` | `product-stress-test-screenshots/post-05-teacher-notifications.png` |
| 学生首页 | `/student` | `product-stress-test-screenshots/post-06-student-home.png` |
| 学生作业列表 | `/student/assignments` | `product-stress-test-screenshots/post-07-student-assignments.png` |
| 学生实验列表 | `/student/labs` | `product-stress-test-screenshots/post-08-student-labs.png` |
| 学生通知中心 | `/student/notifications` | `product-stress-test-screenshots/post-09-student-notifications.png` |
