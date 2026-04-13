# 通知与公告接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/notifications` | 通知列表 | 已登录 |
| POST | `/notifications/read` | 批量已读 | 已登录 |
| GET | `/announcements` | 公告列表 | 已登录 |
| POST | `/announcements` | 发布公告 | 教师 / 管理员 |

## 2. 通知列表

查询参数：

- `page`
- `pageSize`
- `isRead`
- `type`

返回字段：

- `id`
- `type`
- `title`
- `content`
- `isRead`
- `createdAt`

## 3. 公告发布

请求体：

```json
{
  "title": "第 3 周实验安排",
  "content": "请在本周五前完成实验一",
  "scopeType": "course",
  "scopeValue": "course_01"
}
```

## 4. 默认触发事件

- 任务发布
- 提交受理
- 评测完成
- 成绩发布
- 复核结果
