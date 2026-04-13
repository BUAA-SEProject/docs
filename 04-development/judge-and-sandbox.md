# 判题与沙箱设计

## 1. 设计目标

- 将代码执行与主业务 API 隔离。
- 对评测结果进行统一归一化，屏蔽第三方判题实现细节。
- 支持重评、超时、编译失败、运行失败等典型场景。

## 2. 组件组成

| 组件 | 职责 |
| --- | --- |
| `submissionService` | 接收提交并投递判题任务 |
| `judge-worker` | 消费队列、调用 Judge0、归一化结果 |
| `Judge0 CE` | 在隔离容器中执行代码 |
| `judge_runs` 表 | 保存历史评测任务与结果 |

## 3. 队列任务模型

```json
{
  "submissionId": "sub_xxx",
  "taskId": "task_xxx",
  "language": "python",
  "sourceCode": "print('hello')",
  "testcases": [
    { "id": "tc1", "input": "1 2", "expectedOutput": "3" }
  ],
  "limits": {
    "cpuTimeMs": 2000,
    "memoryMb": 256
  }
}
```

## 4. 结果归一化模型

| 字段 | 说明 |
| --- | --- |
| `status` | `success` / `failed` / `timeout` / `compile_error` / `runtime_error` |
| `score` | 归一化后的总分 |
| `passedCount` | 通过测试点数量 |
| `totalCount` | 测试点总数 |
| `compileMessage` | 编译错误摘要 |
| `runtimeMessage` | 运行错误摘要 |
| `caseResults` | 每个测试点的输入、输出、判定结果 |

## 5. 资源限制建议

| 维度 | 默认值 |
| --- | --- |
| 单次执行时间 | 2 秒 |
| 单题总评测时间 | 60 秒 |
| 内存限制 | 256 MB |
| 输出限制 | 1 MB |
| 并发限制 | 同一学员同一时刻默认 1 个运行中任务 |

## 6. 故障恢复

- Judge0 不可用：任务标记为失败，可重试。
- Worker 崩溃：依赖队列确认机制重新消费未确认任务。
- 归一化失败：保留原始响应并写入错误日志，供人工排查。

## 7. 安全要求

- 运行容器默认禁用外网访问。
- 禁止挂载主机敏感目录。
- 限制 CPU、内存、进程数和临时文件空间。
- 对任务输入、代码和输出统一做大小限制。
