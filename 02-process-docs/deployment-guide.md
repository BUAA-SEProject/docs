# 部署文档

## 1. 文档信息

- 文档名称：在线教学与实训平台部署文档
- 版本：v1.1
- 状态：正式基线
- 更新日期：2026-04-13
- 适用范围：本地开发、演示环境、课程答辩环境

## 2. 部署目标与环境说明

本文档定义一套可复现的最小可运行部署方式，保证团队可以在全新机器上完成：

1. 启动 Web、API、Worker、数据库、缓存、对象存储和沙箱服务。
2. 完成初始化数据导入与管理员账号创建。
3. 验证“登录 -> 建课 -> 发任务 -> 在线 IDE 编辑 / 运行 / 提交 -> 评测 -> 批改 -> 出成绩”主链路。

## 3. 运行依赖

- 宿主机：Linux（用于 `go-judge` 正式运行）
- 运行时：Node.js 22 LTS、Docker 27+、Docker Compose v2
- 数据库：PostgreSQL 16
- 存储服务：S3 兼容对象存储（开发 / 演示默认 MinIO）
- 缓存 / 队列：Redis 7
- 判题服务：`criyle/go-judge`

### 3.1 核心环境变量

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `APP_ENV` | 运行环境 | `dev` |
| `APP_PORT` | API 端口 | `3000` |
| `DATABASE_URL` | PostgreSQL 连接串 | `postgres://app:pwd@postgres:5432/otp` |
| `REDIS_URL` | Redis 连接串 | `redis://redis:6379/0` |
| `STORAGE_ENDPOINT` | S3 兼容对象存储地址 | `http://minio:9000` |
| `SESSION_SECRET` | 会话密钥 | `change-me` |
| `GO_JUDGE_URL` | `go-judge` API 地址 | `http://go-judge:5050` |
| `GO_JUDGE_TOKEN` | `go-judge` 访问令牌 | `change-me` |

## 4. 部署步骤

### 4.1 启动基础设施

```bash
docker compose up -d postgres redis minio go-judge
```

### 4.2 初始化数据库

```bash
docker compose run --rm platform-api npm run db:migrate
docker compose run --rm platform-api npm run db:seed
```

### 4.3 启动应用

```bash
docker compose up -d platform-api judge-worker platform-web
```

## 5. 初始化与验证

建议初始化以下数据：

- 1 个平台管理员账号
- 2 个教师账号
- 4 个学员账号
- 1 门演示课程
- 2 个演示任务：1 个编程任务（含模板工程）、1 个文档任务

验收前冒烟检查：

- 管理员可登录并进入平台概览
- 教师可创建课程并发布任务
- 学员可进入在线 IDE、编辑代码并完成试运行
- 学员可正式提交代码并获得评测结果
- 教师可批改并发布成绩

## 6. 常见问题与排障

| 现象 | 排查方向 |
| --- | --- |
| 登录成功但页面空白 | 检查前端环境变量和 API 基地址 |
| IDE 一直提示保存失败 | 检查 API 日志、数据库写权限和任务开放状态 |
| 试运行或评测一直不结束 | 检查 Redis 队列、Worker 日志和 `go-judge` 状态 |
| 文件上传失败 | 检查对象存储凭据、桶权限和对象大小限制 |
| 成绩发布后学生看不到结果 | 检查权限、成绩状态和通知事件 |

## 7. 回滚方案

- 代码版本回滚：回退到上一个已验证镜像标签。
- 数据库回滚：优先使用备份恢复，不做危险的手工表级回滚。
- 配置回滚：恢复上一版 `.env` 与平台配置版本。
