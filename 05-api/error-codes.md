# 错误码规范

## 1. 设计原则

- 业务错误与系统错误分层。
- 错误码使用字符串常量，稳定且便于前端映射文案和测试断言。
- 同一错误场景跨接口复用同一错误码。

## 2. 错误响应格式

```json
{
  "code": 1,
  "message": "FORBIDDEN",
  "requestId": "req_123",
  "data": null
}
```

- `code` 为 `0` 时表示成功，非 `0` 时表示错误。
- `message` 为错误码字符串，用于前端程序化判断。
- `requestId` 用于链路追踪和排查。

## 3. 核心错误码

| 错误码 | 含义 | 说明 |
| --- | --- | --- |
| `FORBIDDEN` | 无权限 | 角色或作用域无访问权限 |
| `INVALID_CREDENTIALS` | 认证失败 | 用户名或密码错误 |
| `INVALID_REFRESH_TOKEN` | 刷新令牌无效 | refresh token 无效或已过期 |
| `ACCOUNT_LOCKED` | 账号锁定 | 账号处于锁定期 |
| `ACCOUNT_DISABLED` | 账号停用 | 账号已停用 |
| `ACCOUNT_EXPIRED` | 账号失效 | 账号已失效 |
| `ORG_HIERARCHY_INVALID` | 组织层级非法 | 组织节点层级关系不合法 |
| `ANNOUNCEMENT_DISABLED` | 公告功能关闭 | 班级公告功能开关已关闭 |
| `RESOURCE_DISABLED` | 资源功能关闭 | 班级资源功能开关已关闭 |
| `DISCUSSION_DISABLED` | 讨论功能关闭 | 班级讨论功能开关已关闭 |
| `DISCUSSION_LOCKED` | 帖子已锁定 | 讨论帖子已被教师锁定 |
| `COURSE_DISCUSSION_NOT_FOUND` | 讨论不存在 | 课程讨论帖子不存在 |
| `COURSE_ANNOUNCEMENT_NOT_FOUND` | 公告不存在 | 课程公告不存在 |
| `COURSE_RESOURCE_NOT_FOUND` | 资源不存在 | 课程资源不存在 |
| `SUBMISSION_WINDOW_INVALID` | 提交窗口关闭 | 不在允许提交的时间窗口内 |
| `SUBMISSION_ASSIGNMENT_UNAVAILABLE` | 作业不可提交 | 作业状态不允许提交 |
| `LAB_STATUS_INVALID` | 实验状态非法 | 实验状态不允许当前操作 |
| `PROGRAMMING_WORKSPACE_CONFLICT` | 工作区冲突 | 基于旧修订写入，需要刷新 |

## 4. 前端处理建议

- `FORBIDDEN`：显示无权限页或提示，很多场景应直接转空态或禁用态。
- `INVALID_CREDENTIALS`：提示用户名或密码错误。
- `INVALID_REFRESH_TOKEN`：清空本地会话并跳回登录页。
- `*_DISABLED`：将对应功能区域切到功能关闭态。
- `DISCUSSION_LOCKED`：禁用输入框。
- `SUBMISSION_WINDOW_INVALID` / `SUBMISSION_ASSIGNMENT_UNAVAILABLE`：提示用户当前业务冲突原因。
- `PROGRAMMING_WORKSPACE_CONFLICT`：提示用户刷新工作区。
- 建议做统一错误字典层，不要把后端原始 message 直接散落到页面组件中。
