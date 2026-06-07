---
title: "批改与成绩接口"
section: "05-api"
status: current
---
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
| POST | `/teacher/assignments/{assignmentId}/grades/publish` | 发布 / 重新发布成绩 | 教师 / 整课助教 |

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
  "score": 30,
  "feedbackText": "边界条件处理不完整"
}
```

## 3. 发布成绩

`POST /api/v1/teacher/assignments/{assignmentId}/grades/publish`

业务规则：

- 设置作业的 `grade_published_at` 时间戳，标志成绩已发布。
- 首次发布返回 `initialPublication=true`；重新发布返回 `initialPublication=false`，不重置首次发布时间。
- 响应包含 `assignmentId`、`publishedByUserId`、`publishedAt` 和 `initialPublication`。
- 发布后会触发通知事件；重新发布会写入审计记录。
- 学生侧成绩册只在成绩发布后展示最终可见结果。

## 4. 成绩册说明

- 教师侧成绩册默认按每个学生每个作业最新正式提交聚合。
- offering 级成绩册只对教师 / 管理员开放。
- class 级成绩册额外对具备班级责任的 TA 开放。
- 教师侧成绩册 `assignmentColumns[]` 返回 `gradePublished`、`gradePublishedAt`、`gradePublishedByUserId`，用于页面展示已发布状态、发布时间、发布人和重新发布语义。
- 教师侧成绩统计 `assignments[]` 返回 `applicableStudentCount`、`publishedStudentCount` 和 `publicationRate`，用于展示学生可见范围。
- 学生侧仅展示已发布 assignment 的结构化作业成绩。
- 成绩册导出是文件下载，不是 JSON。
