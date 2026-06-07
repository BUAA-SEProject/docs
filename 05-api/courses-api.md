---
title: "课程接口"
section: "05-api"
status: current
---
# 课程接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/admin/academic-terms` | 创建学期 | 学校管理员 |
| GET | `/admin/academic-terms` | 学期列表 | 学校管理员 |
| POST | `/admin/course-catalogs` | 创建课程模板 | 学校/学院管理员 |
| GET | `/admin/course-catalogs` | 课程模板列表 | 学校/学院管理员 |
| POST | `/admin/course-offerings` | 创建开课实例 | 学校/学院管理员 |
| GET | `/admin/course-offerings` | 开课实例列表 | 学校/学院/课程管理员 |
| GET | `/admin/course-offerings/:offeringId` | 开课实例详情 | 学校/学院/课程管理员 |
| POST | `/teacher/course-offerings/:offeringId/classes` | 创建教学班 | 教师 / 具备课程治理权限的管理员 |
| GET | `/teacher/course-offerings/:offeringId/classes` | 教学班列表 | 教师 / 管理员 |
| PUT | `/teacher/course-classes/:teachingClassId/features` | 更新班级功能开关 | 教师 / 管理员 |
| POST | `/teacher/course-offerings/:offeringId/members/batch` | 批量添加课程成员 | 教师 / 管理员 |
| POST | `/teacher/course-offerings/:offeringId/members/import` | 通过 CSV 导入既有系统用户 | 教师 / 管理员 |
| GET | `/teacher/course-offerings/:offeringId/members` | 课程成员列表 | 教师 / 管理员 / 受限助教 |
| POST | `/teacher/course-offerings/:offeringId/resources` | 上传课程资源 | 教师 / 整课助教 |
| GET | `/teacher/course-offerings/:offeringId/resources` | 教师侧课程资源列表 | 教师 / 整课助教 / 受限助教 |
| PUT | `/teacher/course-resources/:resourceId` | 更新资源标题和说明 | 教师 / 整课助教 |
| GET | `/me/course-classes/:teachingClassId/resources` | 学生侧可见资源列表 | 已加入教学班的学生 |
| GET | `/me/courses` | 我的课程 | 已登录 |

## 2. 关键规则

- 学生不能自主选课，当前版本不提供 `/student/.../enroll` 接口。
- 课程成员只能由教师从系统既有用户中批量添加或导入。
- 助教可以查看自己协助教学班的成员，但不能批量加人或修改班级功能开关。
- 同一用户可在一个班级中是学生，在另一个班级中是助教。
- 课程公告正文、讨论正文和课程资源说明保存原始 Markdown；API 不返回预渲染 HTML。
- 前端阅读区负责安全 Markdown 渲染，支持标题、列表、引用、表格、代码块、行内代码和链接，默认忽略原始 HTML。

## 3. 创建开课实例

`POST /api/v1/admin/course-offerings`

请求体示例：

```json
{
  "catalogId": 1,
  "termId": 1,
  "offeringCode": "CS101-2026SP-01",
  "offeringName": "数据结构（2026春）",
  "primaryCollegeUnitId": 2,
  "secondaryCollegeUnitIds": [3],
  "deliveryMode": "HYBRID",
  "language": "ZH",
  "capacity": 120,
  "instructorUserIds": [4],
  "startAt": "2026-02-20T08:00:00+08:00",
  "endAt": "2026-07-10T23:59:59+08:00"
}
```

返回重点字段：

- `orgCourseUnitId`
- `primaryCollege`
- `managingColleges`
- `instructors`
- `status`

## 4. 创建教学班

`POST /api/v1/teacher/course-offerings/:offeringId/classes`

请求体示例：

```json
{
  "classCode": "CLS-2024",
  "className": "24级班",
  "entryYear": 2024,
  "capacity": 60,
  "scheduleSummary": "周二 1-2 节"
}
```

返回重点字段：

- `orgClass.id`
- `entryYear`
- `features`

## 5. 批量添加课程成员

`POST /api/v1/teacher/course-offerings/:offeringId/members/batch`

请求体示例：

```json
{
  "members": [
    { "userId": 6, "memberRole": "STUDENT", "teachingClassId": 1, "remark": "24级学生" },
    { "userId": 5, "memberRole": "TA", "teachingClassId": 2, "remark": "25级助教" }
  ]
}
```

返回：

- `successCount`
- `failCount`
- `errors`

## 6. 导入课程成员

`POST /api/v1/teacher/course-offerings/:offeringId/members/import`

上传字段：

- `file`
- `importType`，当前仅支持 `csv`

CSV 字段：

- `username`
- `memberRole`
- `classCode`
- `remark`

说明：

- 导入只接受系统内已存在的用户名。
- 不会在导入时创建新用户。

## 7. 班级功能开关

`PUT /api/v1/teacher/course-classes/:teachingClassId/features`

支持字段：

- `announcementEnabled`
- `discussionEnabled`
- `resourceEnabled`
- `labEnabled`
- `assignmentEnabled`

## 8. 课程资源

`POST /api/v1/teacher/course-offerings/:offeringId/resources`

multipart 字段：

- `file`：资源文件，最大 50 MB。
- `title`：资源标题；前端标题为空时可用文件名兜底。
- `description`：可选资源说明，保存原始 Markdown，最长 5000 字。
- `teachingClassId`：可选，填写后仅定向到该教学班。

`PUT /api/v1/teacher/course-resources/:resourceId`

请求体示例：

```json
{
  "title": "第一章实验指导",
  "description": "## 下载说明\n\n- 先阅读指导书\n- 再完成实验"
}
```

教师和学生资源列表返回 `CourseResourceView`，其中 `description` 为可选原始 Markdown；前端负责安全渲染，危险链接和原始 HTML 不作为可执行内容输出。

## 9. 我的课程

`GET /api/v1/me/courses`

返回字段摘要：

- `offeringId`
- `offeringCode`
- `offeringName`
- `roles`
- `classes`
