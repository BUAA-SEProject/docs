---
title: "环境与部署基线"
section: "06-testing-and-ops"
status: current
---
# 环境与部署基线

## 1. 环境划分

| 环境 | 用途 | 数据要求 |
| --- | --- | --- |
| 开发环境 | 本地开发与调试 | 可重置测试数据 |
| 测试环境 | 集成联调与回归 | 接近演示环境的数据结构 |
| 演示环境 | 答辩、录屏、验收 | 固定演示账号和演示数据 |

## 2. 环境差异控制

- 开发环境允许热更新和调试日志。
- 测试环境应启用接近生产的构建方式。
- 演示环境禁止临时改配置，所有变更必须提前彩排。

## 3. 部署关注点

- 前后端版本对齐
- 数据库初始化脚本可重复执行
- 演示数据预先准备
- 关键依赖可快速重启
- 判题服务与 Worker 状态可检查
- Web 终端实验运行时配置可追溯，fake 与 Kubernetes 验证结果必须区分

## 4. Web 终端实验运行时

Web 终端实验支持两类运行时：

| 运行时 | 用途 | 说明 |
| --- | --- | --- |
| `fake` | 本地开发、普通测试、无 Kubernetes 环境的 E2E | 默认运行时；启动后直接进入运行中，终端输出 `AUBB lab terminal ready.` 并做最小回显 |
| `kubernetes` | 真实实验环境验证和生产部署 | 需要显式配置集群连接、namespace、Pod 安全约束和镜像 |

本地默认配置建议：

```bash
AUBB_LAB_RUNTIME_ENABLED=true
AUBB_LAB_RUNTIME_MODE=fake
```

真实 Kubernetes smoke 验证时使用非提交 kubeconfig：

```bash
AUBB_LAB_RUNTIME_ENABLED=true
AUBB_LAB_RUNTIME_MODE=kubernetes
AUBB_LAB_K8S_NAMESPACE=aubb-labs
AUBB_LAB_K8S_KUBECONFIG_PATH=/path/to/local/kubeconfig
```

不得提交真实 kubeconfig、token、cookie、JWT、私钥或集群连接串。未执行 Kubernetes smoke 时，只能声明 fake runtime 路径已验证，不能声明生产 Kubernetes 链路已通过。

## 5. 运行检查项

- 登录是否正常
- 课程列表是否加载
- 提交与评测是否返回结果
- 成绩统计是否可查看
- 通知是否可触发
- 审计日志是否可检索
- 教师能创建并发布 Web 终端实验
- 学生能启动 fake 实验环境并打开 Web 终端
- 教师能查看学生实验环境会话状态
