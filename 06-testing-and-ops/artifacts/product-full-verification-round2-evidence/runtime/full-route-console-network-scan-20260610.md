# 第二轮全站关键页 console/network 归因补证

## 1. 执行摘要

- 执行时间：2026-06-10 23:49-23:56 CST
- 工具：Playwright MCP 浏览器
- 环境：`http://127.0.0.1:3000` 前端、`http://127.0.0.1:18080` 后端
- 范围：公共、管理员、教师、学生、开课助教、班级助教共 `55` 个 route / 角色组合
- 结论：复核后 `55/55` 无意外 `console.error`，无意外业务 `4xx/5xx` 响应，无未解释 request failure

说明：首次批量巡检中 `/login` 出现 3 条 Next.js dev static chunk / HMR 请求 `net::ERR_ABORTED`，属于页面切换时静态资源请求取消，不是业务 API 或页面错误；随后对 `/login` 单独复核，`consoleErrors=[]`、`unexpectedResponses=[]`、`failedRequests=[]`，结果为通过。

## 2. 统计结果

| 指标 | 结果 |
| --- | --- |
| 扫描 route / 角色组合 | 55 |
| 通过 | 55 |
| 意外 console error 页面 | 0 |
| 意外业务 4xx/5xx 页面 | 0 |
| 未解释 request failure 页面 | 0 |
| 导航错误页面 | 0 |
| console warning 总数 | 0 |

## 3. 覆盖清单

| 角色 | Route 数 | 覆盖范围 | 结果 |
| --- | ---: | --- | --- |
| 无登录用户 | 3 | `/login`、`/unauthorized`、未登录访问 `/admin` | 通过 |
| 学校管理员 | 12 | 治理首页、平台配置、组织、用户、学期、课程模板、开课、权限解释、审计日志 | 通过 |
| 教师 | 20 | 教师首页、课程、成员、公告、资源、讨论、题库、判题环境、作业、提交、成绩、实验、通知 | 通过 |
| 学生 | 12 | 学生首页、课程、讨论、作业、WebIDE、提交详情、成绩、实验、通知 | 通过 |
| 开课助教 | 5 | 教师首页、授权开课、未授权开课、不存在开课、管理区禁止 | 通过 |
| 班级助教 | 3 | 教师首页、成员页、管理区禁止 | 通过 |

## 4. 预期负例归因

| 场景 | 页面表现 | 网络 / console 归因 |
| --- | --- | --- |
| 未登录访问 `/admin` | 跳转 `/login?next=%2Fadmin` | 无意外 console error / 业务 4xx |
| 开课助教访问 `/teacher/courses/5` | 页面显示课程不可访问态 | 无意外 console error / 业务 4xx；页面已避免继续渲染快捷动作入口 |
| 开课助教访问 `/teacher/courses/999999` | 页面显示课程不可访问态 | 无意外 console error / 业务 4xx；页面已避免停留加载态 |
| 助教访问 `/admin` | 跳转 `/unauthorized` | 权限拒绝为预期页面行为，无意外 console error |

## 5. 逐角色 route 明细

### 公共 / 无登录

- `/login`：通过，标题 `AUBB 在线教学与实验平台`
- `/unauthorized`：通过，标题 `权限不足`
- `/admin`：通过，最终 URL `/login?next=%2Fadmin`

### 管理员

- `/admin`：通过，标题 `管理端工作台`
- `/admin/platform-config`：通过，标题 `平台配置`
- `/admin/org-units`：通过，标题 `组织架构`
- `/admin/users`：通过，标题 `用户管理`
- `/admin/users/9`：通过，标题 `教师1`
- `/admin/academic-terms`：通过，标题 `学期管理`
- `/admin/course-catalogs`：通过，标题 `课程模板`
- `/admin/course-offerings`：通过，标题 `开课管理`
- `/admin/course-offerings/2`：通过，标题 `数据结构 2025 秋`
- `/admin/course-offerings/32`：通过，标题 `MCP-R2-06102015 开课实例-EDIT`
- `/admin/auth-explain`：通过，标题 `权限解释`
- `/admin/audit-logs`：通过，标题 `审计日志`

### 教师

- `/teacher`：通过，标题 `教师工作台`
- `/teacher/courses`：通过，标题 `我的课程`
- `/teacher/courses/2`：通过，标题 `数据结构 2025 秋`
- `/teacher/courses/2/members`：通过，标题 `成员管理`
- `/teacher/courses/2/announcements`：通过，标题 `课程公告`
- `/teacher/courses/2/resources`：通过，标题 `课程资源`
- `/teacher/courses/2/discussions`：通过，标题 `课程讨论`
- `/teacher/courses/2/discussions/36`：通过，标题 `MCP-R2-20260610-145754 教师讨论补证`
- `/teacher/courses/2/question-bank`：通过，标题 `题库管理`
- `/teacher/courses/2/judge-environments`：通过，标题 `判题环境`
- `/teacher/assignments`：通过，标题 `全部作业`
- `/teacher/assignments/create?offeringId=2`：通过，标题 `创建作业`
- `/teacher/assignments/7/edit?offeringId=2`：通过，标题 `编辑作业`
- `/teacher/submissions`：通过，标题 `全部提交`
- `/teacher/submissions/55`：通过，标题 `MCP-R2-20260610-1618 结构化提交补证作业`
- `/teacher/grading/gradebook`：通过，标题 `全部成绩`
- `/teacher/question-bank`：通过，标题 `题库中心`
- `/teacher/labs`：通过，标题 `全部实验`
- `/teacher/notifications`：通过，标题 `通知中心`
- `/me/notifications`：通过，标题 `通知中心`

### 学生

- `/student`：通过，标题 `学生学习中心`
- `/student/courses`：通过，标题 `我的课表`
- `/student/courses/2`：通过，标题 `数据结构 2025 秋`
- `/student/courses/2/discussions/36`：通过，标题 `MCP-R2-20260610-145754 教师讨论补证`
- `/student/assignments`：通过，标题 `全部作业`
- `/student/assignments/7`：通过，标题 `Task-Programming-A1`
- `/student/assignments/7/workspace/11`：通过，WebIDE 页面无意外 console/network 错误
- `/student/submissions/57?assignmentId=260`：通过，标题 `MCP-R2-POLL-0610105839`
- `/student/grades`：通过，标题 `全部成绩`
- `/student/labs`：通过，标题 `全部实验`
- `/student/notifications`：通过，标题 `通知中心`
- `/me/notifications`：通过，标题 `通知中心`

### 助教与权限负例

- 开课助教 `/teacher`：通过，标题 `教师工作台`
- 开课助教 `/teacher/courses/2`：通过，标题 `数据结构 2025 秋`
- 开课助教 `/teacher/courses/5`：通过，页面为未授权课程不可访问态
- 开课助教 `/teacher/courses/999999`：通过，页面为不存在课程不可访问态
- 开课助教 `/admin`：通过，最终 URL `/unauthorized`
- 班级助教 `/teacher`：通过，标题 `教师工作台`
- 班级助教 `/teacher/courses/2/members`：通过，标题 `成员管理`
- 班级助教 `/admin`：通过，最终 URL `/unauthorized`

## 6. 结论

`NFR-004` 的全站关键页 console/network 归因已补齐。当前未发现需要新增编号的 console、网络或权限错误缺陷。
