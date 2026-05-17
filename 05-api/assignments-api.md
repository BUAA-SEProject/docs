---
title: "作业与题库接口"
section: "05-api"
status: current
---
# 作业与题库接口

## 1. 接口清单

### 1.1 教师端

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/teacher/course-offerings/{offeringId}/assignments` | 创建作业 | 教师 |
| GET | `/teacher/course-offerings/{offeringId}/assignments` | 作业列表 | 教师 |
| GET | `/teacher/assignments/{assignmentId}` | 作业详情 | 教师 |
| PUT | `/teacher/assignments/{assignmentId}` | 更新作业 | 教师 |
| PUT | `/teacher/assignments/{assignmentId}/paper` | 更新试卷 | 教师 |
| POST | `/teacher/assignments/{assignmentId}/publish` | 发布作业 | 教师 |
| POST | `/teacher/assignments/{assignmentId}/close` | 关闭作业 | 教师 |
| POST | `/teacher/course-offerings/{offeringId}/question-bank/questions` | 创建题库题目 | 教师 |
| GET | `/teacher/course-offerings/{offeringId}/question-bank/questions` | 题库题目列表 | 教师 |
| GET | `/teacher/course-offerings/{offeringId}/question-bank/categories` | 题库分类列表 | 教师 |
| GET | `/teacher/question-bank/questions/{questionId}` | 题目详情 | 教师 |
| PUT | `/teacher/question-bank/questions/{questionId}` | 更新题目 | 教师 |
| POST | `/teacher/question-bank/questions/{questionId}/archive` | 归档题目 | 教师 |

### 1.2 学生端

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/me/assignments` | 我的作业列表 | 已登录 |
| GET | `/me/assignments/{assignmentId}` | 作业详情 | 已登录 |

## 2. 创建作业

`POST /api/v1/teacher/course-offerings/{offeringId}/assignments`

请求体关键字段：

```json
{
  "title": "实验一：排序算法",
  "description": "请完成快速排序",
  "openAt": "2026-04-20T08:00:00Z",
  "dueAt": "2026-04-27T15:59:59Z",
  "submissionLimit": 10,
  "gradingMode": "hybrid"
}
```

## 3. 作业状态流转

作业状态为：`DRAFT` -> `PUBLISHED` -> `CLOSED`

- `POST /teacher/assignments/{assignmentId}/publish`：发布作业
- `POST /teacher/assignments/{assignmentId}/close`：关闭作业

## 4. 题库管理

支持五种题型建模，题目存储在题库中，通过试卷快照挂接到作业。

## 5. 教师查看提交

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/teacher/assignments/{assignmentId}/submissions` | 按作业查看提交列表 | 教师 |
| GET | `/teacher/submissions/{submissionId}` | 提交详情 | 教师 |
| GET | `/teacher/submission-artifacts/{artifactId}/download` | 下载提交附件 | 教师 |
