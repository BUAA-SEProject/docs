# 认证接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/auth/login` | 用户登录并获取 JWT | 公开 |
| POST | `/auth/logout` | 退出登录 | 已登录 |
| GET | `/auth/me` | 获取当前用户 | 已登录 |

## 2. 登录

`POST /api/v1/auth/login`

请求体：

```json
{
  "username": "teacher01",
  "password": "Password123"
}
```

响应体示例：

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
  "tokenType": "Bearer",
  "expiresInSeconds": 7200,
  "user": {
    "userId": 12,
    "username": "teacher01",
    "displayName": "张老师",
    "primaryOrgUnitId": 401,
    "accountStatus": "ACTIVE",
    "academicProfile": {
      "academicId": "T2026001",
      "realName": "张老师",
      "identityType": "TEACHER",
      "profileStatus": "ACTIVE",
      "phone": "13800000001"
    },
    "identities": [
      {
        "roleCode": "CLASS_ADMIN",
        "scopeOrgUnitId": 401,
        "scopeOrgType": "CLASS",
        "scopeOrgName": "软件工程 1 班"
      }
    ]
  }
}
```

业务规则：

- 登录成功后服务端返回访问令牌，不再建立服务端 Session。
- 访问令牌默认有效期为 2 小时。
- 连续 5 次登录失败后，账号锁定 30 分钟。
- `DISABLED`、`LOCKED`、`EXPIRED` 账号不得成功登录。

## 3. 当前用户

`GET /api/v1/auth/me`

请求头：

```http
Authorization: Bearer <access-token>
```

返回字段：

- `userId`
- `username`
- `displayName`
- `primaryOrgUnitId`
- `accountStatus`
- `academicProfile`
- `identities`

## 4. 退出登录

`POST /api/v1/auth/logout`

说明：

- 当前实现为无状态 JWT，退出接口用于记录审计并通知客户端丢弃令牌。
- 当前版本不提供服务端撤销列表。

## 5. 常见拒绝结果

- `INVALID_CREDENTIALS`：用户名或密码错误
- `ACCOUNT_LOCKED`：账号处于锁定期
- `ACCOUNT_DISABLED`：账号已停用
- `ACCOUNT_EXPIRED`：账号已失效
