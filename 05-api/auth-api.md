# 认证与会话接口

## 1. 接口清单

| 方法 | 路径 | 说明 | 权限 |
| --- | --- | --- | --- |
| POST | `/auth/login` | 登录 | 公开 |
| POST | `/auth/logout` | 退出登录 | 已登录 |
| GET | `/auth/me` | 获取当前用户 | 已登录 |
| POST | `/auth/change-password` | 修改密码 | 已登录 |

## 2. 登录

`POST /api/v1/auth/login`

请求体：

```json
{
  "username": "teacher01",
  "password": "Password123"
}
```

响应体：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "user": {
      "id": "u_001",
      "displayName": "张老师",
      "platformRole": "teacher"
    }
  }
}
```

## 3. 当前用户

`GET /api/v1/auth/me`

返回字段：

- `id`
- `username`
- `displayName`
- `platformRole`
- `courseRoles`
- `status`

## 4. 修改密码

`POST /api/v1/auth/change-password`

请求体：

```json
{
  "oldPassword": "Password123",
  "newPassword": "NewPassword123"
}
```

业务规则：

- 新密码长度不少于 8 位。
- 修改成功后要求重新登录。
