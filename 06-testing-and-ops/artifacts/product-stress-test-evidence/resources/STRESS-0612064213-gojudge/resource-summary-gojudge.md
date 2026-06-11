# STRESS-0612064213-gojudge 真实 go-judge 专项资源摘要

- 运行环境：本地 Docker 依赖，`server-go-judge-1`、`server-rabbitmq-1`、`server-postgres-1` 等容器运行中；`just healthcheck-strict` 在专项前通过。
- 数据集：80 名学生，结构化编程作业 `judgeAssignmentId=434`，题目 `judgeQuestionId=912`；作业绑定 A 班，runner 使用 `judgeStudentUsernames` 过滤后的 40 名可访问学生。
- sample-run：5/10/20 并发各 120 秒，分别 130 / 260 / 520 次请求，错误率 0，5xx=0；P95 为 2961.07 / 2990.27 / 3003.34 ms，P99 为 3289.41 / 3209.16 / 3190.96 ms。
- 真实提交链路：5/10/20 并发各 300 秒，分别 916 / 1646 / 2060 次提交，学生和教师报告下载均与提交数相同，错误率 0，5xx=0；接口 P95 为 30.17 / 30.85 / 58.09 ms，P99 为 36.55 / 38.82 / 69.77 ms。
- 五类结果：SQL 后验汇总 `judge_jobs` 证明 `ACCEPTED=916`、`WRONG_ANSWER=919`、`COMPILE_ERROR=925`、`RUNTIME_ERROR=931`、`TIME_LIMIT_EXCEEDED=932`；当前产品 verdict 枚举没有 `COMPILE_ERROR`，编译/语法失败以 `RUNTIME_ERROR` verdict 和“编译失败”摘要表示。
- 重评链路：5/10 并发各 120 秒，分别创建 380 / 640 个 `MANUAL_REJUDGE` job，均 `SUCCEEDED` 且 verdict 为 `ACCEPTED`，错误率 0，5xx=0；P99 为 61.99 / 2837.33 ms。
- PostgreSQL 连接采样：提交链路 5/10/20 并发 max 连接数为 24 / 28 / 41；重评 5/10 并发 max 连接数为 34 / 30。
- go-judge 容器采样：提交链路 5/10 并发尾部样本 CPU 分别可达 138.54% / 282.22%，20 并发尾部样本已回落为 0.00%；内存尾部样本约 79.07 / 107.7 / 106.8 MiB。
- RabbitMQ：runner 已采样 `rabbitmqctl list_queues`，本次记录中未观察到持久队列堆积；队列瞬时处理可能快于采样周期。
- 原始证据：`raw/STRESS-0612064213-gojudge/go-judge-specialty-summary.json`、`raw/STRESS-0612064213-gojudge/go-judge-result-class-summary.json`、`raw/STRESS-0612064213-gojudge/go-judge-sample-fixed-*`、`raw/STRESS-0612064213-gojudge/go-judge-submission-chain-*`、`raw/STRESS-0612064213-gojudge/go-judge-requeue-*`。
