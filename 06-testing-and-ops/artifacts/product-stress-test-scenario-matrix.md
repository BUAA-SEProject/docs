# AUBB 交付前压力测试场景清单

> 本清单为 2026-06-11 `goal-stress.md` 合同压测最终记录。最终状态只使用 `通过`、`失败`、`阻塞`、`不适用`。

## 场景结果

| 编号 | 场景 | 必测链路 | 阈值 | 实际负载 | 实际结果 | 状态 | 证据路径 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STRESS-READ-001 | 读请求阶梯压测 | 登录、`auth/me`、学生课程/作业/提交/成绩、教师作业/提交/成绩、通知未读数 | 读请求 P95 < 500ms、P99 < 1500ms、错误率 < 1%、5xx = 0；登录 P95 < 500ms | 50 并发 2 分钟；200 并发 3 分钟；500 并发 3 分钟 | 50 并发通过：RPS 343.39，P95 163.45ms，P99 259.3ms，错误率 0，5xx 0。200 并发失败：P95 2358.92ms，错误率 2.07%，5xx 478。500 并发失败：P95 2719.35ms，错误率 29.03%，5xx 9514。 | 失败 | `product-stress-test-evidence/raw/STRESS-0611132804/contract-run/perf_results_contract.json`；`server-log-stress-errors-excerpt.log` |
| STRESS-WRITE-001 | 写入链路压测 | 学生提交结构化作业、学生提交列表、教师提交列表 | P95 < 1000ms、P99 < 3000ms、错误率 < 1%、5xx = 0 | 10 并发 1 分钟；因错误率超阈未继续 30/50/100 并发 | RPS 29.63，P95 65.0ms，P99 72.36ms，5xx 0；但 429=201，错误率 11.16%。 | 失败 | `perf_results_contract.json` |
| STRESS-JUDGE-001 | 判题与轮询压测 | 学生判题任务列表、判题报告 | P95 < 800ms、P99 < 2000ms、错误率 < 1%、5xx = 0 | 50 并发 2 分钟；200 并发 3 分钟；500 并发 3 分钟 | 50 并发通过：RPS 458.1，P95 43.29ms，错误率 0，5xx 0。200 并发失败：P99 2425.23ms，5xx 26。500 并发失败：P95 2525.36ms，错误率 14.8%，5xx 7133。 | 失败 | `perf_results_contract.json`；`server-log-stress-errors-excerpt.log` |
| STRESS-FILE-001 | 文件上传下载压测 | 教师资源上传；教师/学生资源下载 | 上传 P95 < 3000ms；下载 P95 < 2000ms；错误率 < 1%、5xx = 0 | 上传 5/10 并发各 1 分钟；下载 20/100 并发各 2 分钟 | 上传 5/10 并发 P95 20.56/28.41ms，错误率 0，5xx 0；下载 20/100 并发 P95 25.07/132.02ms，错误率 0，5xx 0。 | 通过 | `perf_results_contract.json`；`manifest.sanitized.json` |
| STRESS-NOTIFY-001 | 通知与 SSE / 轮询专项 | 通知未读数、通知列表、SSE 连接；压后页面通知中心可恢复 | 通知查询 P95 < 500ms、错误率 < 1%、5xx = 0 | 轮询 50/200/500 并发 2/3/3 分钟；SSE 20 并发 1 分钟 | 50/200 轮询通过：P95 14.85/219.73ms，5xx 0。500 轮询失败：P95 2344.92ms，错误率 7.44%，5xx 5282。SSE 20 并发通过：P95 39.35ms，错误率 0，5xx 0。 | 失败 | `perf_results_contract.json`；`playwright-mcp-post-stress-baseline.md` |
| STRESS-LAB-001 | 实验运行时专项 | 学生启动 fake runtime 终端实验会话、查看当前会话、获取连接票据、停止会话 | 成功率 >= 99%，无持续不可恢复会话 | fake runtime 10 并发 1 分钟 | RPS 48.72，P95 45.6ms，P99 51.85ms，错误率 0，5xx 0；201=1520，200=1520。本结果仅证明本地 fake runtime，不代表 Kubernetes runtime 容量。 | 通过 | `perf_results_contract.json`；`manifest.sanitized.json` |
| STRESS-SOAK-001 | Soak 稳定性测试 | 读请求、写提交、判题轮询混合持续运行与资源曲线 | 资源曲线无持续上升到耗尽，服务无重启，核心页面压测后可打开，错误率 < 1%、5xx = 0 | 100 并发 10 分钟 smoke soak | RPS 387.97，P95 271.26ms，P99 2281.26ms，5xx 0；但 429=3069，错误率 1.31%。压后 `healthcheck-strict` 和 Playwright MCP 页面回归通过。 | 失败 | `perf_results_contract.json`；`resource_samples.json`；`19-healthcheck-strict-post-stress.log`；`product-stress-test-screenshots/post-*.png` |

## 指标记录说明

- 资源采样：`product-stress-test-evidence/raw/STRESS-0611132804/contract-run/resource_samples.json`，共 358 个样本。
- 资源摘要：`product-stress-test-evidence/resources/resource-summary-STRESS-0611132804.md`。
- 高并发 5xx 根因摘录：`product-stress-test-evidence/raw/STRESS-0611132804/server-log-stress-errors-excerpt.log`。
- 前后真实页面证据：`product-stress-test-screenshots/pre-*.png` 与 `product-stress-test-screenshots/post-*.png`。
