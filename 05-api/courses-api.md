# 课程接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/courses` | 课程列表 | 已登录 |
| POST | `/courses` | 创建课程 | 教师 |
| GET | `/courses/:courseId` | 课程详情 | 已登录 |
| PATCH | `/courses/:courseId` | 更新课程 | 教师 / 管理员 |
| POST | `/courses/:courseId/join` | 通过邀请码加入课程 | 学员 |
| GET | `/courses/:courseId/members` | 课程成员列表 | 教师 / 助教 |
| POST | `/courses/:courseId/resources` | 上传课程资源 | 教师 / 助教 |

## 2. 创建课程

`POST /api/v1/courses`

请求体：

```json
{
  "name": "软件工程基础实训",
  "term": "2026-Spring",
  "orgUnitId": "org_01",
  "description": "课程简介"
}
```

## 3. 加入课程

`POST /api/v1/courses/:courseId/join`

请求体：

```json
{
  "inviteCode": "ABC123"
}
```

返回：课程成员关系与加入时间。

## 4. 课程资源上传

上传字段：

- `file`
- `name`
- `type`
- `visibility`

返回字段：

- `resourceId`
- `fileKey`
- `downloadUrl`
