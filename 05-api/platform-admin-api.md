# 平台治理接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/admin/platform-configs/current` | 获取当前生效配置 | 管理员 |
| POST | `/admin/platform-configs` | 创建配置草稿 | 管理员 |
| POST | `/admin/platform-configs/:configId/publish` | 发布配置 | 管理员 |
| GET | `/admin/org-units/tree` | 获取组织树 | 管理员 |
| POST | `/admin/org-units` | 新建组织节点 | 管理员 |
| POST | `/admin/users/import` | 批量导入用户 | 管理员 |
| PATCH | `/admin/users/:userId/status` | 启用 / 停用账号 | 管理员 |
| GET | `/admin/dashboard/summary` | 平台概览 | 管理员 / 运维 |
| GET | `/admin/audit-logs` | 审计日志列表 | 管理员 / 运维 |

## 2. 配置发布

`POST /api/v1/admin/platform-configs/:configId/publish`

业务规则：

- 同一时间只允许一个配置版本处于 `published`。
- 发布动作必须写入审计日志。

## 3. 批量导入用户

上传字段：

- `file`
- `importType`，例如 `teacher`、`student`

响应字段：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "total": 100,
    "success": 98,
    "failed": 2,
    "errors": [
      { "row": 3, "reason": "username duplicated" }
    ]
  }
}
```

## 4. 平台概览

返回字段建议：

- `activeCourseCount`
- `activeUserCount`
- `submissionCountToday`
- `judgeSuccessRate`
- `pendingAlerts`

## 5. 审计日志

查询参数：

- `actorUserId`
- `action`
- `targetType`
- `startAt`
- `endAt`
- `page`
- `pageSize`
