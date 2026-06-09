# AUBB 产品全功能完整验证三次演示彩排记录

## 1. 彩排规则

- 每次彩排必须从登录开始。
- 每次彩排必须按真实讲解顺序覆盖管理员、教师、学生、助教和故障预案。
- 失败彩排不得记为成功；失败后可调整演示数据或路线，再继续下一次。
- 三次彩排未全部成功时，`DEMO-001`、`DEMO-002`、`DEMO-003` 保持 `阻塞` 或 `失败`，总体验收结论不得为 `通过`。

## 2. 彩排 1

- 状态：`失败`
- 开始时间：2026-06-09 18:40 CST
- 结束时间：2026-06-09 19:12 CST
- 角色：学校管理员、教师、学生、开课助教、班级助教
- 截图：`003-admin-dashboard.png`、`010-teacher-dashboard.png`、`014-student-dashboard.png`、`018-student-webide-run-result.png`、`021-student-submission-detail-after-submit.png`、`026-student-lab-runtime-started.png`、`028-student-lab-terminal-still-disconnected.png`、`030-student-lab-terminal-echo.png`、`038-teacher-submission-44-detail.png`、`039-teacher-submission-44-grade-saved.png`、`044-ta-u-tac1-dashboard.png`
- 失败点：学生编程题自测和正式提交返回 `SYSTEM_ERROR`，自定义评测脚本未返回裁决 JSON；实验终端首次打开未连接且 echo 无独立输出。彩排无法作为完整成功记录。
- 是否完整通过：否

### 计划路线

1. 管理员登录。
2. 管理员检查平台配置、组织、用户、课程或开课。
3. 管理员使用权限解释或审计日志说明治理能力。
4. 教师登录。
5. 教师进入课程工作区。
6. 教师创建或复核题目、作业、实验或资源。
7. 教师发布作业或实验。
8. 学生登录。
9. 学生完成作业或实验报告。
10. 学生触发文件、判题或通知能力。
11. 教师查看提交或报告。
12. 教师批改、发布成绩或反馈。
13. 学生查看成绩、反馈和通知。
14. 助教登录并验证授权范围。
15. 演示故障预案：说明服务不可用、权限失败或判题失败时的讲解和恢复路径。

## 3. 彩排 2

- 状态：`失败`
- 开始时间：2026-06-09 19:12 CST
- 结束时间：2026-06-09 19:49 CST
- 角色：学校管理员、教师、学生、开课助教、班级助教
- 截图：`040-teacher-submissions-list.png`、`041-teacher-submissions-assignment-7.png`、`042-teacher-gradebook-offering-2.png`、`043-teacher-gradebook-student-u-st1.png`、`044-ta-u-tac1-dashboard.png`、`045-ta-u-tac1-submissions-assignment-7.png`、`046-ta-u-tac1-admin-unauthorized.png`、`047-ta-u-tac1-student-unauthorized.png`、`048-ta-u-tao1-dashboard.png`、`049-ta-u-tao1-gradebook-offering-2.png`、`050-ta-u-tao1-submissions-assignment-7-allowed.png`、`051-ta-u-tao1-submissions-assignment-4-denied.png`、`053-profile-required-profileless-ta.png`
- 后续补证截图：`081-common-student-global-search-results.png`、`082-common-student-global-search-navigate-grades.png`、`083-common-student-topbar-notification-link.png`、`084-auth-me-notifications-direct.png`、`085-common-teacher-global-search-results.png`、`086-common-teacher-global-search-navigate-submissions.png`、`087-teacher-notifications-before-mark-all-read.png`、`088-teacher-notifications-after-mark-all-read.png`、`089-teacher-announcement-create-dialog-filled.png`、`090-teacher-announcement-created.png`、`091-teacher-resource-upload-dialog-file-selected.png`、`092-teacher-resource-uploaded-list.png`、`093-teacher-discussions-list-before-create.png`、`094-teacher-discussion-create-dialog-filled.png`、`095-teacher-discussion-created-list.png`、`096-teacher-discussion-detail-reply-filled.png`、`097-teacher-discussion-reply-created.png`、`098-student-discussion-29-reply-filled.png`、`099-student-discussion-29-reply-created.png`、`100-student-short-answer-markdown-preview.png`、`101-student-short-answer-submission-45-detail.png`
- 失败点：虽然补充了助教权限边界、profile-required、搜索、通知、教师公告、资源上传下载、讨论创建回复和学生简答提交证据，但 WebIDE/实验终端 P1 未修复，且管理员保存创建编辑、题库/判题环境/实验发布、学生客观题/文件题/实验报告提交等强制项仍未形成 MCP 主证据。本次不能记为完整演示成功。
- 是否完整通过：否

### 计划路线

同彩排 1。若彩排 1 中断，本次必须使用修正后的演示数据或路线，并记录差异。

## 4. 彩排 3

- 状态：`阻塞`
- 开始时间：未启动
- 结束时间：未启动
- 角色：学校管理员、教师、学生、开课助教、班级助教
- 截图：未启动
- 失败点：前两次彩排已经暴露 P1 缺陷和强制项阻塞；在不进入修复阶段的前提下，第三次完整彩排没有可成功通过的路线。按合同保持 `阻塞`，不得记为成功。
- 是否完整通过：否

### 计划路线

同彩排 1。若彩排 1 或 2 中断，本次必须使用修正后的演示数据或路线，并记录差异。
