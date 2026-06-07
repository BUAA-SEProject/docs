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

## 4. 作业列表摘要

教师作业列表 `GET /api/v1/teacher/course-offerings/{offeringId}/assignments` 和学生作业列表 `GET /api/v1/me/assignments` 返回分页列表。

结构化作业的列表项包含 `paper` 摘要字段：

```json
{
  "id": 1,
  "title": "实验一：排序算法",
  "status": "PUBLISHED",
  "paper": {
    "sectionCount": 3,
    "questionCount": 5,
    "totalScore": 60,
    "sections": []
  }
}
```

列表页仅使用 `paper.totalScore`、`paper.questionCount` 和 `paper.sectionCount` 展示摘要。`paper.sections` 在列表响应中为空数组；完整题面、选项、答案裁剪和编程题判题配置只通过作业详情接口返回。

## 5. 题库管理

支持六种题型建模，题目存储在题库中，通过试卷快照挂接到作业。

`POST /api/v1/teacher/course-offerings/{offeringId}/question-bank/questions` 与
`PUT /api/v1/teacher/question-bank/questions/{questionId}` 使用同一题目请求体。除
`title`、`prompt`、`questionType`、`defaultScore`、`categoryName`、`tags` 外，不同题型应按下列规则提交专属字段：

| 题型 | 专属字段 |
| --- | --- |
| `SINGLE_CHOICE` | `options` 至少 2 项，每项包含 `optionKey`、`content`、`correct`，且必须且只能 1 项 `correct=true` |
| `MULTIPLE_CHOICE` | `options` 至少 2 项，每项包含 `optionKey`、`content`、`correct`，且至少 1 项 `correct=true` |
| `FILL_BLANK` | `config.referenceAnswer` 必填 |
| `SHORT_ANSWER` | `config.referenceAnswer` 可作为参考答案或评分说明 |
| `FILE_UPLOAD` | `config.maxFileCount`、`config.maxFileSizeMb` 必须为正整数；`config.acceptedExtensions` 可选 |
| `PROGRAMMING` | `config.supportedLanguages` 至少 1 项；`config.templateEntryFilePath`、`config.templateFiles` 可提供模板；`config.judgeCases` 至少 1 项，包含 `stdinText`、`expectedStdout`、`score`，且当前测试点分值合计应等于题目默认分值 |

后端校验失败时返回业务错误码和错误消息；前端题库弹窗应在弹窗错误区展示该消息，并保留当前草稿，便于教师修正字段后重试。

## 6. 教师查看提交

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/teacher/assignments/{assignmentId}/submissions` | 按作业查看提交列表 | 教师 |
| GET | `/teacher/submissions/{submissionId}` | 提交详情 | 教师 |
| GET | `/teacher/submission-artifacts/{artifactId}/download` | 下载提交附件 | 教师 |
