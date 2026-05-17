---
title: "部署文档"
section: "02-process-docs"
status: current
---
# 部署文档

## 1. 文档信息

- 文档名称：AUBB（Academic Unified Builder Bench）部署文档
- 版本：v1.2
- 状态：正式基线
- 更新日期：2026-04-14
- 适用范围：本地开发、演示环境、课程答辩环境

## 2. 部署目标与环境说明

本文档定义一套可复现的最小可运行部署方式，保证团队可以在全新机器上完成：

1. 启动 Web、API、Worker、数据库、缓存、对象存储和沙箱服务。
2. 完成数据库迁移、初始化数据导入与管理员账号创建。
3. 验证“登录 -> 建课 -> 发任务 -> 在线 IDE 编辑 / 运行 / 提交 -> 评测 -> 批改 -> 出成绩”主链路。

## 3. 运行依赖

- 宿主机：Linux（用于 `go-judge` 正式运行）
- 运行时：Java 21、Maven 3.9+、Docker 27+、Docker Compose v2
- 数据库：PostgreSQL 16
- 存储服务：S3 兼容对象存储（开发 / 演示默认 MinIO）
- 缓存 / 消息流：Redis 7
- 判题服务：`criyle/go-judge`

### 3.1 核心环境变量

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `SPRING_PROFILES_ACTIVE` | Spring Profile | `dev` |
| `SERVER_PORT` | API 端口 | `8080` |
| `SPRING_DATASOURCE_URL` | PostgreSQL 连接串 | `jdbc:postgresql://postgres:5432/otp` |
| `SPRING_DATASOURCE_USERNAME` | 数据库用户名 | `app` |
| `SPRING_DATASOURCE_PASSWORD` | 数据库密码 | `change-me` |
| `SPRING_DATA_REDIS_HOST` | Redis 地址 | `redis` |
| `STORAGE_ENDPOINT` | S3 兼容对象存储地址 | `http://minio:9000` |
| `SPRING_SESSION_REDIS_NAMESPACE` | Session 命名空间 | `otp:session` |
| `GO_JUDGE_URL` | `go-judge` API 地址 | `http://go-judge:5050` |
| `GO_JUDGE_TOKEN` | `go-judge` 访问令牌 | `change-me` |

## 4. 部署步骤

### 4.1 启动基础设施

```bash
docker compose up -d postgres redis minio go-judge
```

### 4.2 数据库迁移

数据库迁移由 Flyway 管理，首次部署执行：

```bash
cd backend/platform-api
./mvnw flyway:migrate
```

### 4.3 初始化种子数据

开发 / 答辩环境可执行：

```bash
psql "$SPRING_DATASOURCE_URL" -f ../../infra/sql/seed-dev.sql
```

### 4.4 启动应用

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
| Session 登录不稳定 | 检查 Redis、Cookie 域和 Spring Session 配置 |
| IDE 一直提示保存失败 | 检查 API 日志、数据库写权限和任务开放状态 |
| 试运行或评测一直不结束 | 检查 Redis Stream、Worker 日志和 `go-judge` 状态 |
| Flyway 迁移失败 | 检查数据库版本、脚本顺序和历史表 `flyway_schema_history` |
| 成绩发布后学生看不到结果 | 检查权限、成绩状态和通知事件 |

## 7. 回滚方案

- 代码版本回滚：回退到上一个已验证镜像标签。
- 数据库回滚：优先使用备份恢复，不做危险的手工表级回滚。
- 配置回滚：恢复上一版环境变量与平台配置版本。
