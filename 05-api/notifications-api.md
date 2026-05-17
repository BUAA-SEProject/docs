---
title: "通知接口"
section: "05-api"
status: current
---
# 通知接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/me/notifications` | 通知列表 | 已登录 |
| GET | `/me/notifications/unread-count` | 未读通知数 | 已登录 |
| GET | `/me/notifications/stream` | SSE 实时通知订阅 | 已登录 |
| POST | `/me/notifications/{notificationId}/read` | 单条已读 | 已登录 |
| POST | `/me/notifications/read-all` | 全部已读 | 已登录 |

## 2. 通知列表

`GET /api/v1/me/notifications`

查询参数：

- `page`
- `pageSize`

返回字段：

- `id`
- `type`
- `title`
- `content`
- `isRead`
- `createdAt`

## 3. 未读通知数

`GET /api/v1/me/notifications/unread-count`

返回当前用户的未读通知数量。

## 4. SSE 实时通知订阅

`GET /api/v1/me/notifications/stream`

说明：

- HTTP SSE 单实例 best-effort 通道。
- 不承诺跨节点续传、断线补发或消息总线级可靠性。
- 客户端在 SSE 不可用、断线或超时后，必须回退到列表轮询 + 未读数查询。

## 5. 单条已读

`POST /api/v1/me/notifications/{notificationId}/read`

标记指定通知为已读。

## 6. 全部已读

`POST /api/v1/me/notifications/read-all`

标记所有通知为已读。

## 7. 公告接口

公告通过课程域接口管理：

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/teacher/course-offerings/{offeringId}/announcements` | 创建公告 | 教师 |
| GET | `/teacher/course-offerings/{offeringId}/announcements` | 教师公告列表 | 教师 |
| GET | `/me/course-classes/{teachingClassId}/announcements` | 学生班级公告列表 | 学生 |
| GET | `/me/announcements/{announcementId}` | 学生公告详情 | 学生 |

## 8. 默认触发事件

- 作业发布
- 提交受理
- 评测完成
- 成绩发布
- 复核结果
- 实验发布
- 实验报告评阅

## 9. 前端集成建议

- 默认每 30 到 60 秒轮询一次 `list + unread-count`。
- 若项目已接入 SSE，可增量接入 `/stream`。
- SSE 断连后必须自动退回轮询，不要把通知能力绑定在单一实时通道上。
