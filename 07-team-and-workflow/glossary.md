---
title: "术语表"
section: "07-team-and-workflow"
status: current
---
# 术语表

| 术语 | 说明 |
| --- | --- |
| AUBB | Academic Unified Builder Bench，平台正式名称 |
| 模块化单体 | 单一 Spring Boot 应用仓库，按业务域拆为 `modules/*`，不是微服务拆分 |
| 平台配置 | 平台名称、主题、模块开关等平台级设置 |
| 组织单元 | 院系、班级、实验班等组织结构节点，层级为 SCHOOL → COLLEGE → COURSE → CLASS |
| 课程 | 教师组织教学活动的基本单元 |
| 课程模板 / course catalog | 课程的模板定义，用于跨学期复用 |
| 开课 / course offering | 某门课程在某学期的实际开课记录 |
| 教学班 / teaching class | 某次开课下的班级粒度，用于成员、权限、作业范围和可见性控制 |
| 课程成员 | 参与课程的教师、助教或学生 |
| 任务 | 作业、实验或报告类教学任务 |
| 提交 | 学员上传代码、文件或结果的行为 |
| 评测 | 系统对提交进行自动编译、执行和评分的过程 |
| 判题任务 / judge job | 正式自动评测任务，持久化到 `judge_jobs`，可走队列或本地异步执行 |
| 样例试运行 / sample run | 用户主动触发的同步试运行，不创建 `judge_jobs` |
| 判题 Worker / judge-worker | 复用同一镜像、关闭 Web 容器、专门承担判题消费与异步处理的运行角色，不是独立服务 |
| 批改 | 教师对提交进行人工点评和补充评分 |
| 成绩 | 根据评测和批改结果得到的最终得分 |
| 审计日志 | 对关键行为进行留痕的记录 |
| auth session | 服务端会话事实源，保存 refresh token hash、吊销状态和最近签发时间，不是 HttpSession |
| refresh token | `sessionId.secret` 形式的 opaque token，不是 JWT |
| SSE | 当前唯一的实时通知接口形态，基于 `SseEmitter` 实现 |
