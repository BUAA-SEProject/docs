# STRESS-0612022949 压力前 Playwright MCP 浏览器基线

- 时间：2026-06-12 02:50-02:55 Asia/Shanghai
- 环境：本地真实前端 `http://127.0.0.1:3000`，本地真实后端 `http://127.0.0.1:18080`
- 账号：使用本地 E2E 管理员、教师、学生测试账号；本文件不记录密码、token、cookie 或 JWT。

## 访问结果

| 页面 | 角色 | 结果 | 控制台错误 | 截图 |
| --- | --- | --- | --- | --- |
| `/login` | 未登录 | 登录页可见 | `/api/v1/auth/me` 与 `/api/v1/auth/refresh` 返回 401，符合未登录基线 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-login.png` |
| `/admin` | 管理员 | 管理端工作台可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-admin-dashboard.png` |
| `/admin/users` | 管理员 | 用户管理页可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-admin-users.png` |
| `/teacher` | 教师 | 教师工作台可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-teacher-dashboard.png` |
| `/teacher/grading/gradebook` | 教师 | 成绩册页可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-teacher-gradebook.png` |
| `/teacher/submissions` | 教师 | 提交列表页可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-teacher-submissions.png` |
| `/student` | 学生 | 学生工作台可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-student-dashboard.png` |
| `/student/assignments` | 学生 | 作业页可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-student-assignments.png` |
| `/student/labs` | 学生 | 实验入口页可见 | 无新增错误 | `product-stress-test-screenshots/STRESS-0612022949/STRESS-0612022949-pre-student-labs.png` |

## 说明

- 本基线只证明压力前真实浏览器入口、登录流和关键读页面可用。
- 真实 Kubernetes/Web 终端交互不在本基线中完成，后续仍需按压力合同单独验证。
