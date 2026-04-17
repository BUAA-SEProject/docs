# 平台治理接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| GET | `/admin/platform-config/current` | 获取当前生效平台配置 | 学校管理员 |
| PUT | `/admin/platform-config/current` | 更新当前平台配置并立即生效 | 学校管理员 |
| GET | `/admin/org-units/tree` | 获取当前管理员可见的组织树 | 分层管理员 |
| POST | `/admin/org-units` | 新建组织节点 | 学校 / 学院 / 课程管理员 |
| GET | `/admin/users` | 分页查询当前作用域内用户 | 分层管理员 |
| GET | `/admin/users/:userId` | 查看当前作用域内用户详情 | 分层管理员 |
| POST | `/admin/users` | 新建用户 | 分层管理员 |
| POST | `/admin/users/import` | 批量导入用户 | 分层管理员 |
| PUT | `/admin/users/:userId/identities` | 更新用户作用域身份 | 分层管理员 |
| PUT | `/admin/users/:userId/profile` | 更新用户教务画像 | 分层管理员 |
| PUT | `/admin/users/:userId/memberships` | 更新用户组织成员关系 | 分层管理员 |
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

## 4. 用户查询

### 4.1 列表

`GET /api/v1/admin/users`

查询参数：

- `keyword`
- `academicId`
- `identityType`
- `accountStatus`
- `roleCode`
- `orgUnitId`
- `page`
- `pageSize`

返回字段摘要：

```json
{
  "items": [
    {
      "id": 12,
      "username": "teacher01",
      "displayName": "张老师",
      "email": "teacher01@example.com",
      "phone": null,
      "academicProfile": {
        "academicId": "T2026001",
        "realName": "张老师",
        "identityType": "TEACHER",
        "profileStatus": "ACTIVE",
        "phone": "13800000001"
      },
      "primaryOrgUnitId": 401,
      "primaryOrgUnit": {
        "id": 401,
        "code": "CLS-SE-1",
        "name": "软件工程 1 班",
        "type": "CLASS"
      },
      "accountStatus": "ACTIVE",
      "lastLoginAt": "2026-04-15T10:30:00Z",
      "lockedUntil": null,
      "expiresAt": null,
      "identities": [
        {
          "roleCode": "CLASS_ADMIN",
          "scopeOrgUnitId": 401,
          "scopeOrgType": "CLASS",
          "scopeOrgName": "软件工程 1 班"
        }
      ],
      "memberships": [
        {
          "orgUnitId": 401,
          "membershipType": "TEACHES",
          "membershipStatus": "ACTIVE",
          "sourceType": "MANUAL"
        }
      ]
    }
  ],
  "total": 1,
  "page": 1,
  "pageSize": 20
}
```

### 4.2 详情

`GET /api/v1/admin/users/:userId`

业务规则：

- 只允许查看当前管理员作用域内的用户。
- 返回用户基础资料、画像、默认归属组织摘要、账号生命周期字段、治理身份和成员关系。
- 超出作用域的访问必须返回 `403`。

## 5. 用户导入与身份分配

上传字段：

- `file`
- `importType`，当前仅支持 `csv`

CSV 推荐字段：

- `username`
- `displayName`
- `email`
- `password`
- `primaryOrgCode`
- `identities`
- `status`
- `phone`，可选
- `academicId`，可选；若填写则需同时提供 `realName` 与 `identityType`
- `realName`，可选
- `identityType`，可选，`TEACHER / STUDENT / ADMIN`
- `memberships`，可选，格式为 `TYPE@ORG_CODE|TYPE@ORG_CODE`

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

## 6. 账号状态与生命周期

当前状态包括：

- `ACTIVE`
- `DISABLED`
- `LOCKED`
- `EXPIRED`

说明：

- “解锁”通过将账号状态恢复为 `ACTIVE` 完成。
- 连续 5 次登录失败后，系统自动锁定 30 分钟。
- `lastLoginAt`、`lockedUntil`、`expiresAt` 用于管理员核对账号生命周期。

## 7. 用户画像与成员关系

- `PUT /api/v1/admin/users/:userId/profile`
  - 更新学号/工号、真实姓名、身份类型、画像状态和画像手机号。
- `PUT /api/v1/admin/users/:userId/memberships`
  - 更新用户在课程、班级等组织下的业务成员关系。
- 成员关系不等于治理权限，不能替代 `user_scope_roles`。

## 8. 审计日志

查询参数：

- `actorUserId`
- `action`
- `targetType`
- `startAt`
- `endAt`
- `page`
- `pageSize`

当前实现边界：

- 审计日志先保留学校管理员的全局查询能力。
- 学院级或课程级审计过滤视图留待后续增强。
