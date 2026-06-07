---
title: "判题与沙箱设计"
section: "04-development"
status: current
---
# 判题与沙箱设计

## 1. 设计目标

- 将代码运行与正式评测完全隔离于主业务 API。
- 统一承载“在线 IDE 试运行”和“正式提交评测”两类执行任务。
- 对 `go-judge` 结果进行归一化，屏蔽第三方实现细节。
- 支持重评、超时、编译失败、运行失败、输出超限等典型场景。
- `STANDARD_IO` 默认采用日常竞赛教学常用的放宽比较规则，样例试运行和正式测试保持一致。

## 2. 组件组成

| 组件 | 职责 |
| --- | --- |
| `workspaceService` | 读取工作区文件并生成运行 / 提交快照 |
| `submissionService` | 接收正式提交并投递评测任务 |
| `judge-worker` | 消费运行 / 评测队列、调用 `go-judge`、归一化结果 |
| `go-judge` | 在隔离环境中执行编译和运行 |
| `sandbox_runs` 表 | 保存试运行历史与输出 |
| `judge_runs` 表 | 保存正式评测历史与结果 |

## 3. `go-judge` 选型原因

- 官方文档提供统一的 REST、WebSocket 和 gRPC 接口，便于后续扩展。
- 支持 Linux namespace 与 cgroup 限制，满足课程作业隔离执行要求。
- 支持 `copyIn` / `copyOut` / `copyOutCached`，可将编译产物缓存为 `fileId`，减少隐藏用例重复编译开销。
- 支持 `pipeMapping`，为后续交互题或多进程题型保留扩展空间。
- 支持容器池和并行度配置，适合“课程高峰期短时并发”的场景。

## 4. 执行模式设计

### 4.1 在线 IDE 试运行

- 输入来源：当前工作区快照 + 公开样例或学员自定义输入。
- 输出结果：`stdout`、`stderr`、退出状态、耗时、内存、编译输出摘要。
- 写入位置：`sandbox_runs`。
- 业务边界：不生成正式成绩，不触发教师通知，不进入正式评测统计。
- 标准输入允许为空；输出判定默认忽略行尾空白、末尾空行和最终换行差异。

### 4.2 正式提交评测

- 输入来源：正式提交绑定的不可变快照 + 隐藏用例 + 语言配置。
- 输出结果：结构化测试点结果、得分、判题摘要、原始响应。
- 写入位置：`judge_runs`、`submissions.current_judge_run_id`。
- 业务边界：作为自动评分依据，可被重评和人工批改引用。
- 标准输入允许为空；`STANDARD_IO` 输出判定与样例试运行使用同一套放宽比较规则，严格比较仅作为题目级可选策略。

## 5. 队列任务模型

### 5.1 试运行任务

```json
{
  "runId": "run_xxx",
  "workspaceId": "ws_xxx",
  "snapshotId": "snap_xxx",
  "taskId": "task_xxx",
  "languageProfile": {
    "language": "python3",
    "runCommand": ["/usr/bin/python3", "main.py"]
  },
  "stdin": "1 2",
  "limits": {
    "cpuTimeMs": 2000,
    "clockTimeMs": 3000,
    "memoryMb": 256,
    "outputKb": 1024
  }
}
```

### 5.2 正式评测任务

```json
{
  "judgeRunId": "jr_xxx",
  "submissionId": "sub_xxx",
  "snapshotId": "snap_xxx",
  "taskId": "task_xxx",
  "languageProfileId": "lang_xxx",
  "testcases": [
    { "id": "tc1", "inputKey": "cases/1.in", "outputKey": "cases/1.out", "weight": 20 }
  ],
  "limits": {
    "cpuTimeMs": 2000,
    "clockTimeMs": 4000,
    "memoryMb": 256,
    "outputKb": 1024
  }
}
```

## 6. `go-judge` 请求封装策略

### 6.1 编译阶段

- 对编译型语言先下发一次编译请求。
- `copyIn` 注入源文件与必要依赖文件。
- `copyOutCached` 导出可执行产物，记录返回的 `fileId`。
- 编译失败时直接结束本次评测，并将 `compile_error` 写入归一化结果。

### 6.2 执行阶段

- 执行请求通过 `copyIn.fileId` 引用编译产物，避免重复上传。
- 标准输入以匿名文件注入；标准输出和标准错误通过命名文件收集。
- 每个隐藏用例独立执行，便于输出逐测试点结果。
- 评测完成后主动清理编译缓存 `fileId`。

## 7. 结果归一化模型

| 字段 | 说明 |
| --- | --- |
| `status` | `success` / `failed` / `timeout` / `compile_error` / `runtime_error` / `output_limit_exceeded` |
| `score` | 归一化后的总分 |
| `passedCount` | 通过测试点数量 |
| `totalCount` | 测试点总数 |
| `compileMessage` | 编译错误摘要 |
| `runtimeMessage` | 运行错误摘要 |
| `caseResults` | 每个测试点的输入、输出、判定结果、耗时和内存 |

### 7.1 输出比较规则

`STANDARD_IO` 的默认比较规则面向日常竞赛教学场景：

- 规范化 CRLF / CR 为 LF。
- 忽略每一行的行尾空白。
- 忽略末尾多余空行。
- 忽略最终换行差异。
- 不忽略行内空格差异、大小写差异或数值误差；需要特殊判定时使用题目级 checker。

### 7.2 判定映射示例

| `go-judge` 状态 | 平台内部判定 |
| --- | --- |
| `Accepted` | `accepted` |
| `Time Limit Exceeded` | `time_limit_exceeded` |
| `Memory Limit Exceeded` | `memory_limit_exceeded` |
| `Output Limit Exceeded` | `output_limit_exceeded` |
| `Dangerous Syscall` | `system_error` |
| `Non Zero Exit Status` / `Signalled` | `runtime_error` |
| `Internal Error` / `File Error` | `system_error` |

## 8. 资源限制建议

| 维度 | 试运行默认值 | 正式评测默认值 |
| --- | --- | --- |
| 单次 CPU 时间 | 2 秒 | 2 秒 / 用例 |
| 单次时钟时间 | 3 秒 | 4 秒 / 用例 |
| 单题总评测时间 | 10 秒 | 60 秒 |
| 内存限制 | 256 MB | 256 MB |
| 输出限制 | 1 MB | 1 MB |
| 并发限制 | 同一学员同一时刻 1 个试运行 | 同一学员同一任务 1 个运行中评测 |

## 9. 部署与容量约束

- `go-judge` 生产部署要求 Linux Kernel >= 3.10，并可用 cgroup。
- 容器化部署时需保证嵌套容器 / cgroup 能力，避免资源限制失效。
- `go-judge` 默认并发度接近 CPU 数量，可通过 `-parallelism` 调整。
- 缓存文件存储在共享内存时，应根据并发和编译产物大小预留 `/dev/shm`。
- Windows / macOS 支持为实验性质，不作为正式交付环境。

## 10. 故障恢复

- `go-judge` 不可用：任务标记失败，进入重试或人工重评。
- Worker 崩溃：依赖队列确认机制重新消费未确认任务。
- 归一化失败：保留原始响应并写入错误日志，供人工排查。
- 编译缓存泄漏：通过后台清理任务和 `go-judge` 文件 TTL 回收。

## 11. 安全要求

- 运行环境默认禁用外网访问。
- 禁止挂载主机敏感目录。
- 限制 CPU、内存、进程数、打开文件数和临时文件空间。
- 对任务输入、源码、输出统一做大小限制。
- `go-judge` 原始接口只允许内网访问，浏览器永远不直接调用。
