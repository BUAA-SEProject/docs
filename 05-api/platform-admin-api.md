# 平台治理接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/admin/platform-config/current` | 获取当前生效平台配置 | 学校管理员 |
| PUT | `/admin/platform-config/current` | 更新当前平台配置并立即生效 | 学校管理员 |
| GET | `/admin/org-units/tree` | 获取当前管理员可见的组织树 | 分层管理员 |
| POST | `/admin/org-units` | 新建组织节点 | 学校 / 学院 / 课程管理员 |
| POST | `/admin/users` | 新建用户 | 分层管理员 |
| POST | `/admin/users/import` | 批量导入用户 | 分层管理员 |
| PUT | `/admin/users/:userId/identities` | 更新用户作用域身份 | 分层管理员 |
| PATCH | `/admin/users/:userId/status` | 更新账号状态 | 分层管理员 |
| GET | `/admin/audit-logs` | 审计日志列表 | 学校管理员 |

## 2. 平台配置

`PUT /api/v1/admin/platform-config/current`

业务规则：

- 平台配置只有一份当前生效配置。
- 更新成功后立即生效，不存在草稿、发布和回退流程。
- 更新动作必须写入审计日志。

## 3. 组织结构

组织层级固定为：

- `SCHOOL`
- `COLLEGE`
- `COURSE`
- `CLASS`

业务规则：

- 只允许按上面的顺序创建子节点。
- 非法层级关系必须被拒绝。

## 4. 用户导入与身份分配

上传字段：

- `file`
- `importType`，当前默认 `csv`

CSV 推荐字段：

- `username`
- `displayName`
- `email`
- `password`
- `primaryOrgCode`
- `identities`
- `status`

其中 `identities` 的格式为：

```text
ROLE_CODE@ORG_CODE|ROLE_CODE@ORG_CODE
```

例如：

```text
COLLEGE_ADMIN@ENG|CLASS_ADMIN@SE-2026-1
```

响应字段：

```json
{
  "total": 100,
  "success": 98,
  "failed": 2,
  "errors": [
    { "row": 3, "username": "bad-user", "reason": "身份作用域与组织类型不匹配" }
  ]
}
```

## 5. 审计日志

查询参数：

- `actorUserId`
- `action`
- `targetType`
- `startAt`
- `endAt`
- `page`
- `pageSize`

当前实现边界：

- 审计日志先保留学校管理员的全局查询能力
- 学院级或课程级审计过滤视图留待后续增强
