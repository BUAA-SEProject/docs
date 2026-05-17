---
title: "认证接口"
section: "05-api"
status: current
---
# 认证接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/auth/login` | 用户登录并获取 JWT | 公开 |
| POST | `/auth/logout` | 退出登录 | 已登录 |
| POST | `/auth/refresh` | 刷新 access token | 已登录 |
| POST | `/auth/revoke` | 撤销 refresh token | 已登录 |
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

- 登录成功后服务端签发 JWT Bearer access token。
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

## 4. 刷新令牌

`POST /api/v1/auth/refresh`

请求体：

```json
{
  "refreshToken": "opaque-refresh-token"
}
```

响应体：

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
  "tokenType": "Bearer",
  "expiresInSeconds": 7200
}
```

业务规则：

- refresh token 使用 opaque token，仅保存 hash，不提供设备列表或自助会话管理。
- 刷新成功后旧 refresh token 失效，实现 refresh token 轮换。

## 5. 撤销令牌

`POST /api/v1/auth/revoke`

请求头：

```http
Authorization: Bearer <access-token>
```

说明：

- 主动撤销当前会话的 refresh token。
- 撤销后该会话的 access token 仍有效至过期，但 refresh token 即时失效。
- 管理员强制失效和账号停用也会让旧会话即时失效。

## 6. 退出登录

`POST /api/v1/auth/logout`

请求头：

```http
Authorization: Bearer <access-token>
```

说明：

- 退出当前会话，记录审计日志。
- 当前会话即时失效。

## 7. 常见拒绝结果

- `INVALID_CREDENTIALS`：用户名或密码错误
- `ACCOUNT_LOCKED`：账号处于锁定期
- `ACCOUNT_DISABLED`：账号已停用
- `ACCOUNT_EXPIRED`：账号已失效
- `INVALID_REFRESH_TOKEN`：refresh token 无效或已过期
