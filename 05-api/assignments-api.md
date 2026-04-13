# 任务、提交与评测接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/courses/:courseId/tasks` | 课程任务列表 | 已登录 |
| POST | `/courses/:courseId/tasks` | 创建任务 | 教师 |
| GET | `/tasks/:taskId` | 任务详情 | 已登录 |
| PATCH | `/tasks/:taskId` | 更新任务 | 教师 |
| POST | `/tasks/:taskId/publish` | 发布任务 | 教师 |
| POST | `/tasks/:taskId/submissions` | 创建提交 | 学员 |
| GET | `/tasks/:taskId/submissions` | 我的提交列表 / 课程提交列表 | 已登录 |
| GET | `/submissions/:submissionId` | 提交详情 | 已登录 |
| POST | `/submissions/:submissionId/rejudge` | 重新评测 | 教师 / 管理员 |

## 2. 创建任务

请求体关键字段：

```json
{
  "type": "programming",
  "title": "实验一：排序算法",
  "contentMd": "请完成快速排序",
  "openAt": "2026-04-20T08:00:00Z",
  "dueAt": "2026-04-27T15:59:59Z",
  "submissionLimit": 10,
  "gradingMode": "hybrid"
}
```

## 3. 创建提交

支持两种提交方式：

- `sourceText`：在线编辑器代码
- `files[]`：上传文件

响应字段：

- `submissionId`
- `submitNo`
- `status`
- `acceptedAt`

## 4. 提交详情

返回字段：

- 提交元信息
- 文件列表
- 当前评测状态
- 当前评测结果摘要
- 历史评测记录

## 5. 重新评测

业务规则：

- 仅教师或管理员可触发。
- 会追加新的评测记录，不覆盖旧记录。
