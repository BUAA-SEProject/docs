# API 总览

## 目标

统一前后端协作的接口风格，降低联调与测试成本。

## 基本约定

- 基础路径：`/api/v1`
- 数据格式：JSON
- 鉴权方式：Bearer Token 或 Session Cookie
- 时间格式：ISO 8601

## 建议响应结构

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

## 分页建议

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [],
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```

## 模块划分

- 认证与用户
- 课程
- 作业与实验
- 批改与成绩
- 通知
