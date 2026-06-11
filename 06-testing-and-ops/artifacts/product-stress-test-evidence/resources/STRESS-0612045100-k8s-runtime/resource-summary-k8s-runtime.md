# STRESS-0612045100-k8s-runtime Kubernetes runtime 资源摘要

## 结论

- 本批只覆盖真实 Kubernetes Web 终端单会话 smoke，不是压力测试。
- API + WebSocket smoke 创建的 `aubb-lab-stress-1533` 与 Playwright MCP 页面回归创建的 `aubb-lab-stress-1535` 均成功调度到 `aubb-lab-dev-control-plane`。
- 两次会话停止后，`aubb-labs` namespace 均无残留 Pod。
- 当前 Metrics API 不可用，本批未采集 Kubernetes CPU/内存曲线，只记录 Pod phase、事件、重启次数和清理状态。

## 证据

- 环境与 RBAC：`../../commands/STRESS-0612045100-k8s-runtime/02-k8s-current-state.log`
- 健康检查：`../../commands/STRESS-0612045100-k8s-runtime/04-healthcheck-strict-k8s-runtime.log`
- API + WebSocket smoke：`../../raw/STRESS-0612045100-k8s-runtime/k8s-terminal-smoke.json`
- API smoke 后清理：`../../commands/STRESS-0612045100-k8s-runtime/07-k8s-pods-after-cleanup.log`
- 页面回归后清理：`../../commands/STRESS-0612045100-k8s-runtime/11-k8s-pods-after-playwright-cleanup.log`
- 页面截图：`../../../product-stress-test-screenshots/STRESS-0612045100-k8s-runtime/student-terminal-connected.png`
