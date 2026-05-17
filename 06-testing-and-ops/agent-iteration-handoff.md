---
title: "Agent 持续迭代交接"
section: "06-testing-and-ops"
status: current
---
# Agent 持续迭代交接

本文件固定 AUBB 工作区的 agent 接手、验证、交接格式。根目录不是 Git 仓库，`server/`、`web/`、`docs/` 必须独立检查和提交。

## 1. 接手入口

每轮开始先执行：

```bash
just status
just healthcheck
```

需要真实联调时：

```bash
cp env/e2e.example env/e2e.env
# 填写本地测试值，不提交 env/e2e.env
just dev-up
just healthcheck-strict
```

真实浏览器验证：

```bash
just e2e-real
```

收尾：

```bash
just dev-down
```

## 2. Dirty 工作区规则

- 如果 `just status` 显示已有未提交改动，先判断是否与当前任务相关。
- 只修改当前任务需要的文件；不要回滚、覆盖或整理无关 dirty 文件。
- 跨 `server/`、`web/`、`docs/` 的变更分别记录验证命令和提交建议。
- 如果必须提交，只 stage 当前任务相关文件，并在提交说明中写清仓库名和范围。

## 3. 每轮交接模板

复制以下模板追加到 `plan-execution-log.md` 或本文件末尾。

```markdown
## YYYY-MM-DD HH:mm 本轮交接

### 目标

- 本轮目标：
- 来源文件 / issue / 用户要求：

### 初始状态

| 仓库 | 分支 | 初始 dirty 状态 | 备注 |
| --- | --- | --- | --- |
| `server/` |  |  |  |
| `web/` |  |  |  |
| `docs/` |  |  |  |

### 改动范围

| 仓库 | 文件 | 改动说明 |
| --- | --- | --- |
| `server/` |  |  |
| `web/` |  |  |
| `docs/` |  |  |

### 验证证据

| 命令 | 结果 | 备注 |
| --- | --- | --- |
| `just healthcheck` |  |  |
| `just verify` |  |  |
| `just verify-full` |  |  |
| `just e2e-real` |  |  |

### 残留风险

- 

### 下一步

- 
```

## 4. 完成门禁

在声称完成前，至少满足以下条件：

1. 当前任务涉及的仓库已经运行对应验证命令。
2. 文档、API、测试与实现口径一致。
3. 真实 E2E 只连接本地前端、后端和 Docker 依赖，不 mock API 流量。
4. 残留风险已经记录，且没有被包装成“已完全无风险”。
5. 交接记录包含命令、结果、未做项和下一步。

## 5. 工作区级门禁

当前根目录不是 Git 仓库，因此没有根目录 GitHub Actions。多仓库一致性先由本地 `just` 门禁承担：

| 门禁 | 命令 | 覆盖 |
| --- | --- | --- |
| 状态门禁 | `just status` | 三个子仓库分支、dirty、untracked 状态 |
| 运行环境门禁 | `just healthcheck` / `just healthcheck-strict` | 工具、compose、环境变量、端口、readiness、OpenAPI、前端登录页 |
| 快速质量门禁 | `just verify` | 后端测试、前端 lint/typecheck、文档构建 |
| 完整非浏览器门禁 | `just verify-full` | 后端 verify、前端 lint/typecheck/test/build、文档构建 |
| 真实浏览器门禁 | `just e2e-real` | 真实本地前后端 Playwright E2E |

若未来将工作区本身纳入 Git 管理，可把这些命令直接接入根级 CI；在此之前，交接记录中必须写明本轮实际运行了哪些 `just` 门禁。
