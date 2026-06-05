---
title: "本地 E2E 数据重置与清理规范（2026-06-05）"
section: "06-testing-and-ops"
status: current
---
# 本地 E2E 数据重置与清理规范（2026-06-05）

本文规定全量测试前如何处理本地 E2E 历史数据。目标是让测试从干净、可重复、可解释的状态开始，同时避免误删非本地环境数据。

## 1. 结论

全量测试前优先执行“整套本地依赖重置”，即删除本地 Docker compose volumes。AUBB 真实 E2E 会写入 PostgreSQL、MinIO、Redis 和 RabbitMQ，只清数据库容易留下附件对象、缓存、队列或对象存储残留。

## 2. 当前事实

- `just dev-down` 只停止前端、后端和 Docker 依赖，不删除 volumes。
- `server/compose.yaml` 定义了以下持久化 volume：
  - `postgres-data`
  - `rabbitmq-data`
  - `minio-data`
  - `redis-data`
- `web/src/tests/e2e/README.md` 明确记录部分真实 E2E 会保留 `E2E-*` 业务记录。
- 本地真实 E2E 默认依赖：
  - 后端：`http://127.0.0.1:18080`
  - 前端：`http://127.0.0.1:3000`
  - 默认账号标识：`U-SA1`、`U-TA1`、`U-ST1`
  - 密码来自 `env/e2e.env`，不得写入报告。

## 3. 推荐流程：整套本地依赖重置

适用场景：

- 全量测试前。
- 本地数据库已经堆积大量 `E2E-*`、`MCP-*`、`FULLRUN-*` 数据。
- 不需要保留本地手工演示数据。

执行前检查：

```bash
cd /Users/moorefoss/Code/AUBB
just status
```

停止服务：

```bash
cd /Users/moorefoss/Code/AUBB
just dev-down
```

删除本地依赖 volumes：

```bash
cd /Users/moorefoss/Code/AUBB/server
docker compose down -v
```

重新启动：

```bash
cd /Users/moorefoss/Code/AUBB
just dev-up
just healthcheck-strict
```

重建基础 E2E fixture：

```bash
cd /Users/moorefoss/Code/AUBB
just seed-fixtures
```

完成后检查：

```bash
cd /Users/moorefoss/Code/AUBB
just healthcheck-strict
```

## 4. Bootstrap 注意事项

如果删除 volumes 后数据库为空，需要确保 `env/e2e.env` 具备可初始化首个学校和管理员的 bootstrap 配置。只记录变量名，不记录变量值。

需要关注的变量名：

```text
AUBB_BOOTSTRAP_ENABLED
AUBB_BOOTSTRAP_SCHOOL_CODE
AUBB_BOOTSTRAP_SCHOOL_NAME
AUBB_BOOTSTRAP_ADMIN_USERNAME
AUBB_BOOTSTRAP_ADMIN_DISPLAY_NAME
AUBB_BOOTSTRAP_ADMIN_EMAIL
AUBB_BOOTSTRAP_ADMIN_PASSWORD
AUBB_BOOTSTRAP_ADMIN_ACADEMIC_ID
AUBB_BOOTSTRAP_ADMIN_REAL_NAME
AUBB_E2E_ADMIN_USERNAME
AUBB_E2E_ADMIN_PASSWORD
AUBB_E2E_TEACHER_USERNAME
AUBB_E2E_TEACHER_PASSWORD
AUBB_E2E_STUDENT_USERNAME
AUBB_E2E_STUDENT_PASSWORD
AUBB_E2E_TEMP_USER_PASSWORD
```

建议：

- 只在空库初始化窗口打开 `AUBB_BOOTSTRAP_ENABLED=true`。
- 基础管理员和 fixture 准备好后，把 `AUBB_BOOTSTRAP_ENABLED` 改回 `false`。
- 不要把 `env/e2e.env` 提交到仓库。

## 5. 备选流程：定向清理 E2E 前缀数据

适用场景：

- 必须保留本地手工演示数据。
- 不适合删除 MinIO、Redis、RabbitMQ volume。
- 已经明确所有 E2E 数据都有稳定前缀。

定向清理必须先实现受保护脚本，不建议临时手写 SQL。脚本应满足：

1. 仅允许连接 `127.0.0.1` 或 `localhost` 的本地数据库。
2. 默认 dry-run，只输出将删除的记录数量和表名。
3. 需要显式 `--apply` 才真正删除。
4. 删除范围仅限测试前缀：
   - `E2E-*`
   - `E2E-FULLRUN-*`
   - `MCP-*`
   - 其他当轮明确记录的测试前缀。
5. 同步处理：
   - PostgreSQL 业务数据。
   - MinIO 测试附件对象。
   - Redis 测试 key。
   - RabbitMQ 测试队列和未消费消息。
6. 输出清理报告，不输出密码、token、cookie、JWT 或真实连接串。

建议将来新增统一命令：

```bash
just e2e-clean-dry-run
just e2e-reset
```

## 6. 不允许的操作

- 不确认环境就执行 `docker compose down -v`。
- 对非本地数据库执行 `DELETE`、`TRUNCATE` 或 schema drop。
- 只清 PostgreSQL 就声称 E2E 数据已完全清理。
- 在日志、报告、提交信息中记录真实密码、token、cookie、JWT、私钥或连接串。
- 把清理动作提交为功能通过证据。

## 7. 清理记录模板

```md
## E2E 数据重置记录

- 时间：
- 执行人 / Agent：
- 工作区：
- 选择方式：整套本地依赖重置 / 定向清理
- 执行命令：
- 是否删除 volumes：
- 是否执行 `just seed-fixtures`：
- 验证命令：
- 当前残留数据：
- 风险：
```
