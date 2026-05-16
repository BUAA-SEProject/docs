# 批改与成绩接口

## 1. 接口清单

### 1.1 教师批改

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/teacher/submissions/{submissionId}/answers/{answerId}/grade` | 人工批改单题 | 教师 / 助教 |

### 1.2 成绩管理

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/teacher/assignments/{assignmentId}/grades/batch-adjust` | 批量调分 | 教师 |
| GET | `/teacher/assignments/{assignmentId}/grades/import-template` | 下载成绩导入模板 | 教师 |
| POST | `/teacher/assignments/{assignmentId}/grades/import` | 导入成绩 | 教师 |
| POST | `/teacher/assignments/{assignmentId}/grades/publish` | 发布成绩 | 教师 |

### 1.3 教师成绩册

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/teacher/course-offerings/{offeringId}/gradebook` | 开课实例成绩册 | 教师 |
| GET | `/teacher/course-offerings/{offeringId}/gradebook/export` | 导出开课成绩册 | 教师 |
| GET | `/teacher/course-offerings/{offeringId}/gradebook/report` | 开课成绩统计 | 教师 |
| GET | `/teacher/teaching-classes/{teachingClassId}/gradebook` | 教学班成绩册 | 教师 / 助教 |
| GET | `/teacher/teaching-classes/{teachingClassId}/gradebook/export` | 导出教学班成绩册 | 教师 / 助教 |
| GET | `/teacher/teaching-classes/{teachingClassId}/gradebook/report` | 教学班成绩统计 | 教师 / 助教 |
| GET | `/teacher/course-offerings/{offeringId}/students/{studentUserId}/gradebook` | 单学生成绩册 | 教师 |

### 1.4 学生成绩册

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/me/course-offerings/{offeringId}/gradebook` | 我的成绩册 | 已登录 |
| GET | `/me/course-offerings/{offeringId}/gradebook/export` | 导出我的成绩册 | 已登录 |

## 2. 人工批改

`POST /api/v1/teacher/submissions/{submissionId}/answers/{answerId}/grade`

请求体：

```json
{
  "manualScore": 30,
  "commentText": "边界条件处理不完整"
}
```

## 3. 发布成绩

`POST /api/v1/teacher/assignments/{assignmentId}/grades/publish`

业务规则：

- 设置作业的 `grade_published_at` 时间戳，标志成绩已发布。
- 发布后会触发通知事件。
- 学生侧成绩册只在成绩发布后展示最终可见结果。

## 4. 成绩册说明

- 教师侧成绩册默认按每个学生每个作业最新正式提交聚合。
- offering 级成绩册只对教师 / 管理员开放。
- class 级成绩册额外对具备班级责任的 TA 开放。
- 学生侧仅展示已发布 assignment 的结构化作业成绩。
- 成绩册导出是文件下载，不是 JSON。
