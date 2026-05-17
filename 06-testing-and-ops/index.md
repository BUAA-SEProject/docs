---
title: "测试与运维"
section: "06-testing-and-ops"
status: current
---
# 测试与运维

本部分关注“系统是否可靠可交付”。如果过程文档回答的是“该做什么”和“怎么设计”，本部分回答的是“如何验证”和“如何稳定运行”。

## 文档清单

| 文档 | 作用 |
| --- | --- |
| 测试策略 | 规定测试分层、范围和证据要求 |
| 环境与部署基线 | 规定不同环境的差异与上线前检查 |
| 可观测性 | 规定日志、指标、仪表盘和告警 |
| 验收清单 | 规定答辩前最终核对项 |
| 计划执行记录 | 记录本轮文档同步、审计、修复和联调进度 |
| Agent 持续迭代交接 | 固定 agent 接手、dirty 状态、验证证据和跨轮交接模板 |
| 全栈审计报告 | 记录前端、后端、文档和测试的主要问题与修复 |
| 按钮级 E2E 验证报告 | 记录真实浏览器按钮级验收范围、证据和阻塞 |

## 使用顺序

1. 开发启动前阅读 [测试策略](testing-strategy.md)。
2. 环境准备时阅读 [环境与部署基线](environments-and-deployment.md)。
3. 观测与排障时阅读 [可观测性](observability.md)。
4. 提交前和答辩前使用 [验收清单](acceptance-checklist.md)。
5. Agent 接手和跨轮压缩阅读 [Agent 持续迭代交接](agent-iteration-handoff.md)。
6. 本轮交付核对阅读 [计划执行记录](plan-execution-log.md)、[全栈审计报告](full-stack-audit-report.md) 和 [按钮级 E2E 验证报告](button-level-e2e-verification-report.md)。
