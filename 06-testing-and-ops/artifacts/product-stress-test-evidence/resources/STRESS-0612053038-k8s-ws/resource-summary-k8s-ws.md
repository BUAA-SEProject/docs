# STRESS-0612053038-k8s-ws Kubernetes WebSocket 资源摘要

- 运行时间：2026-06-12
- 运行时：`AUBB_LAB_RUNTIME_MODE=kubernetes`
- Kubernetes context：`kind-aubb-lab-dev`
- Namespace：`aubb-labs`
- 场景：`lab_terminal_websocket`

| 并发 | 持续时间 | 总请求 | RPS | P95 | P99 | 错误率 | 5xx | WebSocket 连接成功 | 命令成功 | 初连/重连/重置成功 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 600s | 155 | 0.26 | 79.10ms | 365.25ms | 0 | 0 | 115 | 115 | 5 / 5 / 5 |
| 10 | 600s | 310 | 0.51 | 93.82ms | 2223.45ms | 0 | 0 | 230 | 230 | 10 / 10 / 10 |
| 20 | 600s | 657 | 1.09 | 142.91ms | 2230.11ms | 0 | 0 | 460 | 460 | 20 / 20 / 20 |

## Pod 采样摘要

| 并发 | 样本数 | Pod 峰值 | Phase 记录 | 最大重启数 | Ready 状态 | 清理结果 |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 62 | 5 | Running 295 | 0 | 全部 ready | 压测后 namespace 无残留 Pod |
| 10 | 61 | 10 | Running 590 | 0 | 全部 ready | 压测后 namespace 无残留 Pod |
| 20 | 61 | 20 | Running 1180 | 0 | 全部 ready | 压测后 namespace 无残留 Pod |

## 证据路径

- `product-stress-test-evidence/raw/STRESS-0612053038-k8s-ws/k8s-ws-5/perf_results_k8s_ws_5.json`
- `product-stress-test-evidence/raw/STRESS-0612053038-k8s-ws/k8s-ws-10/perf_results_k8s_ws_10.json`
- `product-stress-test-evidence/raw/STRESS-0612053038-k8s-ws/k8s-ws-20/perf_results_k8s_ws_20.json`
- `product-stress-test-evidence/resources/STRESS-0612053038-k8s-ws/k8s-pod-samples-5.jsonl`
- `product-stress-test-evidence/resources/STRESS-0612053038-k8s-ws/k8s-pod-samples-10.jsonl`
- `product-stress-test-evidence/resources/STRESS-0612053038-k8s-ws/k8s-pod-samples-20.jsonl`
- `product-stress-test-evidence/commands/STRESS-0612053038-k8s-ws/21-browser-k8s-terminal-regression.log`
- `product-stress-test-evidence/commands/STRESS-0612053038-k8s-ws/22-k8s-pods-after-browser-cleanup.log`
- `product-stress-test-screenshots/STRESS-0612053038-k8s-ws/browser-k8s-terminal-connected.png`

## 限制

- 当前 kind 集群未提供可用 Metrics API，`kubectl top` 返回 metrics unavailable，因此本轮只记录 Pod phase、Ready、重启次数、事件和清理状态，不声明 Kubernetes CPU/内存曲线。
- 浏览器 console 日志使用 `all=true` 导出，包含本轮前开发服务器重启和旧会话产生的历史错误；本轮页面主断言以“运行中”、“已连接”和 `UI-K8S-WS-OK` echo 回显为准。
