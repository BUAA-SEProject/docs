# AUBB 交付前压力测试场景清单

> 本清单为 2026-06-11 `goal-stress.md` 合同压测最终记录。最终状态只使用 `通过`、`失败`、`阻塞`、`不适用`。

## goal-stress.md 7.1-7.15 场景结果

| 合同编号 | 场景 | 阈值 | 实际负载 | 实际结果 | 状态 | 证据路径 |
| --- | --- | --- | --- | --- | --- | --- |
| 7.1 | 公共入口、认证与基础读请求 | 读请求 P95 < 500ms、P99 < 1500ms、错误率 < 1%、5xx=0；登录风暴单独统计 | 读请求 50/200/500 并发 2/3/3 分钟；第七批修复后补 read-label 端点级复测 | 首次合同压测 200/500 失败。第七批 no-tx 修复后 50 并发通过；200 并发 P95 252.73ms、错误率 0.01%、5xx 11、P99 2333.60ms；500 并发 P95 2405.31ms、错误率 6.67%、5xx 10791。`auth_me` 200/500 并发 5xx=0，`authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=0`，登录风暴未单独完成。 | 失败 | `product-stress-test-evidence/raw/STRESS-0611132804/contract-run/perf_results_contract.json`；`product-stress-test-evidence/raw/STRESS-06112118-principalnotx/read-label-results.json`；`product-stress-test-evidence/raw/STRESS-06112118-principalnotx/server-log-window-summary.log`；`server-log-stress-errors-excerpt.log` |
| 7.2 | 管理员治理、IAM 与审计压测 | 治理读 20/50/100，并发写 5/10/20，用户导入 100/500 | 数据准备阶段执行管理员创建和 80 学生导入；未执行治理专项阶梯 | 仅有功能/E2E 和数据准备证据；500 用户导入和审计专项压测未完成。 | 阻塞 | `product-stress-test-evidence/commands/17-setup-perf-data-contract.log`；`manifest.sanitized.json` |
| 7.3 | 课程主数据、教学组织与课堂内容压测 | 读 50/200/500，写 10/30/50，成员 100/500 导入 | 数据准备创建开课、2 个教学班和 80 名学生；混合读请求覆盖部分课程/成绩读取 | 未执行课程、成员导入、公告、讨论、回复、锁定等专项压力阶梯。 | 阻塞 | `manifest.sanitized.json`；`perf_results_contract.json` |
| 7.4 | 题库、判题环境与作业生命周期压测 | 题库/作业读 50/200/500，写 5/10/20，发布/关闭 | 数据准备创建并发布 `STRESS-*` 客观题、结构化作业和编程作业 | 未执行题库、判题环境、作业编辑/发布/关闭专项压力阶梯。 | 阻塞 | `manifest.sanitized.json`；`product-stress-test-evidence/commands/06-just-e2e-real.log` |
| 7.5 | 学生提交与师生回查压测 | 结构化提交 10/30/50/100，读 50/200/500，文件题 5/10/20 | 写入链路 10 并发 1 分钟 | P95 65.0ms、5xx=0，但 429=201、错误率 11.16%；未继续升压。 | 失败 | `perf_results_contract.json` |
| 7.6 | WebIDE 与代码工作区专项 | 工作区读写 20/50/100，样例运行 5/10/20，5 个真实浏览器学生会话 | Playwright MCP 前后页面回归未包含 WebIDE 5 并发；runner 缺少 workspace API 专项 | 无工作区保存、历史、恢复、重置、样例运行并发容量证据。 | 阻塞 | `playwright-mcp-pre-stress-baseline.md`；`playwright-mcp-post-stress-baseline.md` |
| 7.7 | 真实 go-judge 判题全链路专项 | 真实提交 5/10/20，轮询 50/200/500，重评 5/10，覆盖 5 类结果 | 判题轮询 50/200/500 并发；数据准备触发 1 次真实编程提交 | 50 并发轮询通过；200 并发出现 26 个 5xx；500 并发错误率 14.8%、5xx 7133。五类结果、报告下载、重评未完成。 | 失败 | `perf_results_contract.json`；`manifest.sanitized.json`；`server-log-stress-errors-excerpt.log` |
| 7.8 | 批改、成绩册、导入导出与报表压测 | 查询 50/200/500，批改/调分 5/10/20，成绩导入 100/500，导出 20/50/100 | 混合读请求包含教师/学生成绩册；E2E 功能基线通过 | 未执行成绩导入、导出、报告、人工批改/调分专项压力阶梯。 | 阻塞 | `perf_results_contract.json`；`product-stress-test-evidence/commands/06-just-e2e-real.log` |
| 7.9 | 文件上传下载与对象存储专项 | 上传 5/10/20，下载 20/100/300，三档文件大小，保存 SHA256 | 教师课程资源上传 5/10 并发；下载 20/100 并发 | 执行子集通过，但缺少学生附件、实验报告附件、判题报告、成绩册导出、20MiB 文件和 SHA256 记录。 | 阻塞 | `perf_results_contract.json`；`manifest.sanitized.json` |
| 7.10 | 通知、SSE 与实时恢复专项 | 轮询 50/200/500，SSE 20/100/300 连接保持 5/10/10 分钟 | 轮询 50/200/500；SSE 20 并发 1 分钟 | 50/200 轮询通过；500 轮询错误率 7.44%、5xx 5282。SSE 20 通过但未达到 100/300 和 10 分钟保持。 | 失败 | `perf_results_contract.json`；`playwright-mcp-post-stress-baseline.md` |
| 7.11 | 实验管理、实验报告与附件专项 | 实验读 50/200/500，报告提交 10/30/50，评阅 5/10/20 | 数据准备创建并发布 1 个终端实验；E2E 功能基线通过 | 未执行实验管理、报告草稿/提交、评阅/发布和附件专项压力阶梯。 | 阻塞 | `manifest.sanitized.json`；`product-stress-test-evidence/commands/06-just-e2e-real.log` |
| 7.12 | Web 终端与 Kubernetes 实验运行时专项 | Kubernetes session 5/10/20，WebSocket 5/10/20，命令 I/O、重连、停止/重置清理 | fake runtime 10 并发 1 分钟 | fake runtime P95 45.6ms、5xx=0；真实 Kubernetes runtime 未配置，未执行 Pod/WebSocket 命令 I/O/重连/清理。 | 阻塞 | `perf_results_contract.json`；`docs/06-testing-and-ops/environments-and-deployment.md`；`env/e2e.example` |
| 7.13 | 权限负例、限流与异常输入压测 | 50/200/500 并发，预期 401/403/404/409/413/429，无 5xx/泄漏 | E2E 功能基线覆盖部分未授权/禁止访问；压测自然出现部分 401/429 | 未执行非法 ID、超大分页、过期 token、超大文件、错误 Content-Type 等专项高并发负例。 | 阻塞 | `product-stress-test-evidence/commands/06-just-e2e-real.log`；`perf_results_contract.json` |
| 7.14 | 前端路由、静态资源与文档站压测 | 真实浏览器 5/10/20，静态资源/API docs 50/200/500，移动/桌面截图 | Playwright MCP 前后各 10 张关键页截图；docs build 和 Next build 通过 | 未执行 5/10/20 并发真实浏览器浏览、docs 静态预览和 `/v3/api-docs` 压测。 | 阻塞 | `playwright-mcp-pre-stress-baseline.md`；`playwright-mcp-post-stress-baseline.md`；`09-docs-build-pre-stress.log` |
| 7.15 | 全平台 Soak、混合流量与容量边界 | 读 100 并发 30 分钟，写 10 并发 10 分钟，go-judge/SSE/Web 终端/下载混合 | 100 并发 10 分钟 smoke soak | RPS 387.97，P95 271.26ms，P99 2281.26ms，5xx=0；但 429=3069，错误率 1.31%；完整 30 分钟和 Kubernetes/WebSocket 混合未完成。 | 失败 | `perf_results_contract.json`；`resource_samples.json`；`19-healthcheck-strict-post-stress.log`；`product-stress-test-screenshots/post-*.png` |

## 指标记录说明

- 资源采样：`product-stress-test-evidence/raw/STRESS-0611132804/contract-run/resource_samples.json`，共 358 个样本。
- 资源摘要：`product-stress-test-evidence/resources/resource-summary-STRESS-0611132804.md`。
- 高并发 5xx 根因摘录：`product-stress-test-evidence/raw/STRESS-0611132804/server-log-stress-errors-excerpt.log`。
- 端点级读请求诊断：`product-stress-test-evidence/raw/STRESS-06111820-readlabels/read-label-results.json`、`product-stress-test-evidence/raw/STRESS-06111832-readlabels-bulkfix/read-label-results.json`、`product-stress-test-evidence/raw/STRESS-06111855-authcache/read-label-results.json`、`product-stress-test-evidence/raw/STRESS-06111935-sessionactive/read-label-results.json`、`product-stress-test-evidence/raw/STRESS-06112012-submissionauth/read-label-results.json`、`product-stress-test-evidence/raw/STRESS-06112041-authactivettl/read-label-results.json`、`product-stress-test-evidence/raw/STRESS-06112051-authnotx/read-label-results.json` 与 `product-stress-test-evidence/raw/STRESS-06112118-principalnotx/read-label-results.json`。
- 前后真实页面证据：`product-stress-test-screenshots/pre-*.png` 与 `product-stress-test-screenshots/post-*.png`。
