# 批改与成绩接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/submissions/:submissionId/review` | 查看批改信息 | 教师 / 助教 |
| POST | `/submissions/:submissionId/review` | 保存人工批改 | 教师 / 助教 |
| GET | `/courses/:courseId/grades` | 课程成绩列表 | 教师 / 助教 |
| POST | `/courses/:courseId/grades/publish` | 发布成绩 | 教师 |
| POST | `/courses/:courseId/grades/withdraw` | 撤回成绩 | 教师 |
| GET | `/courses/:courseId/grades/export` | 导出成绩 | 教师 |

## 2. 保存人工批改

请求体：

```json
{
  "manualScore": 30,
  "commentText": "边界条件处理不完整",
  "rubricItems": [
    { "rubricId": "rub_1", "score": 15 }
  ]
}
```

## 3. 发布成绩

`POST /api/v1/courses/:courseId/grades/publish`

请求体：

```json
{
  "taskId": "task_01"
}
```

业务规则：

- 任务内所有应发布成绩均已生成。
- 未完成人工批改的提交不能发布。
- 发布后会触发通知事件。
