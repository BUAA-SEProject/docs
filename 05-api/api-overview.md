# API 总览

## 1. 基本约定

- 基础路径：`/api/v1`
- 数据格式：JSON，文件上传使用 `multipart/form-data`
- 鉴权方式：JWT Bearer access token（`Authorization: Bearer <token>`）
- 时间格式：ISO 8601
- 编码：UTF-8

## 2. 响应结构

```json
{
  "code": 0,
  "message": "ok",
  "requestId": "req_123",
  "data": {}
}
```

## 3. 分页结构

```json
{
  "code": 0,
  "message": "ok",
  "requestId": "req_123",
  "data": {
    "items": [],
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```

## 4. 通用请求头

| Header | 用途 |
| --- | --- |
| `Content-Type` | 请求体类型 |
| `Authorization` | `Bearer <access-token>`，受保护接口必须携带 |
| `X-Request-Id` | 可选，客户端传入便于链路追踪 |

## 5. 分页与筛选

- 分页参数统一使用 `page`、`pageSize`。
- 列表筛选优先使用查询参数，如 `status=active`。
- 多条件筛选采用扁平参数，不使用嵌套 JSON。

## 6. 文件上传

- 文件上传接口统一返回对象存储引用信息。
- 单文件默认不超过 50 MB。
- 文件类型和大小以任务配置或平台配置为准。

## 7. 幂等与并发

- 成绩发布、重新评测、批量导入等接口建议支持幂等键。
- 重要写操作失败后必须返回稳定错误码，便于前端决定是否可重试。

## 8. 模块划分

- 认证与会话
- 平台治理与 IAM
- 课程主数据与教学组织
- 作业与题库
- 提交、工作区与评测
- 批改与成绩册
- 实验与实验报告
- 站内通知
