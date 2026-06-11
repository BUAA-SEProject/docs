# AUBB 压力问题修复计划与执行记录

> 本文件记录 2026-06-12 本轮修复范围。状态只使用 `通过`、`失败`、`阻塞`、`不适用`。本轮不把未复测的完整压力合同标为通过。

## 1. 修复范围

| 关联问题 | 修复目标 | 计划 | 执行状态 | 验证 |
| --- | --- | --- | --- | --- |
| P3-STRESS-001 / runner 卡死风险 | 压测 stage 不应因少量挂起请求无限等待；每个 stage 应能超时、取消 worker 并输出可定位状态。 | 为 `run_perf_suite.py` 增加请求超时配置、stage 级超时、worker 取消和 `EXC:StageTimeout` 统计；阶段结果立即 flush。 | 通过 | `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py`，9 个测试通过。 |
| P1-STRESS-001 / P1-STRESS-002 | 500 并发混合读中 `teacher_gradebook` 曾因 Hikari 连接耗尽产生 500；成绩册页读应减少重复 DB 查询和外层事务连接占用。 | 为教师成绩册页和学生我的成绩册增加短 TTL Redis 缓存；移除班级成绩册外层只读事务；缓存命中不包在 service 外层事务内。 | 通过 | `GradebookApplicationServiceTests` 覆盖整课、班级、学生成绩册无外层读事务和重复请求复用缓存。 |
| P1-STRESS-001 / 成绩写后一致性 | 成绩册页缓存不能让批改、导入、发布后长期返回旧数据。 | 在通用 `CacheService` 增加按 key 前缀删除；Redis 实现用 SCAN 删除匹配 key；成绩发布和人工批改后按开课前缀清理教师/学生成绩册缓存。 | 通过 | `RedisCacheServiceTests` 覆盖前缀删除；`GradingApplicationServiceTests` 覆盖发布成绩后清理 `teacherGradebookPage` 与 `myGradebook` 前缀。 |
| P1-STRESS-001 / P1-STRESS-002 | `STRESS-0612022949` 完整合同中 `my_submissions` 和 `teacher_assignments` 在 500/1000 并发各出现 1 个 5xx，服务日志定位到 `SubmissionApplicationService.requireAssignment -> AssignmentMapper.selectById` 等待 Hikari 连接超时。 | 为 `/api/v1/me/assignments/{id}/submissions` 增加 assignment 元数据短 TTL 缓存和我的提交页短 TTL 缓存，缓存 key 包含 assignment/user/page/pageSize；提交写入后按 assignment+user 前缀清理我的提交页缓存。 | 通过 | `SubmissionApplicationServiceTests.mySubmissionListReusesCachedAssignmentAndPageForIdenticalReadRequest` 证明重复读取不再重复查 assignment/count/page；`STRESS-0612022949/cache-fix-targeted` 中 read ladder 50/200/500/1000 均 0 错误、0 个 5xx。 |
| P2-STRESS-001 / P2-STRESS-002 | `STRESS-0612022949` 完整合同中 `write_path` 30/50 并发出现 429，原因是 `submission-create` 默认 10/min/用户/assignment 的限流低于合同提交流量；业务集成测试仍需能覆写为 1/min 验证限流语义。 | 将 `submission-create` 默认限流提高到 60/min，保留 `AUBB_REDIS_RATE_LIMIT_SUBMISSION_CREATE_LIMIT` 覆写能力和现有限流集成测试。 | 通过 | `RedisProtectedEndpointRateLimitIntegrationTests` 仍以 1/min 覆写并通过；`STRESS-0612022949/cache-fix-targeted` 中 write path 10/30/50/100 均 0 错误、0 个 5xx、0 个 429；`cache-fix-soak` 100 并发 10 分钟 0 错误。 |

## 2. 本轮代码改动

- `server/ops/perf/run_perf_suite.py`：新增 `PERF_REQUEST_TIMEOUT_SECONDS`、`PERF_STAGE_TIMEOUT_GRACE_SECONDS`，stage worker 受 `wait_for_stage_workers(...)` 保护，超时会记录 `EXC:StageTimeout` 并取消未完成 task。
- `server/common/cache`：`CacheService` 新增 `evictByPrefix(...)` 默认方法；`RedisCacheService` 使用 Redis SCAN 匹配并删除缓存 key 前缀。
- `GradebookApplicationService`：教师成绩册页、学生我的成绩册使用 `gradebook-page-ttl` 短 TTL 缓存；整课、班级、学生我的成绩册入口均不声明外层只读事务。
- `GradingApplicationService`：成绩发布和人工批改成功后，在事务提交后清理同一开课下的成绩册页缓存。
- `application.yaml` / `RedisEnhancementProperties`：新增 `AUBB_REDIS_CACHE_GRADEBOOK_PAGE_TTL`，默认 `PT10S`。
- `SubmissionApplicationService`：我的提交列表使用 `my-submission-page-ttl` 短 TTL 缓存 assignment 元数据和分页响应；提交成功后按前缀清理该用户该作业的提交页缓存。
- `application.yaml` / `RedisEnhancementProperties`：新增 `AUBB_REDIS_CACHE_MY_SUBMISSION_PAGE_TTL`，默认 `PT5S`；`submission-create` 默认限流由 10/min 调整为 60/min。

## 3. 已执行验证

| 命令 | 状态 | 说明 |
| --- | --- | --- |
| `bash ./mvnw -Dtest=GradebookApplicationServiceTests,RedisCacheServiceTests,GradingApplicationServiceTests test` | 通过 | 13 个测试通过，覆盖成绩册缓存、无外层事务、Redis 前缀删除和写后失效。 |
| `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py` | 通过 | 9 个测试通过，覆盖 stage 超时、结果 flush、artifact 目录和 endpointStats。 |
| `just healthcheck-strict` | 通过 | 后端 readiness/OpenAPI、前端登录页和本地依赖基线通过。 |
| `bash ./mvnw -Dtest=SubmissionApplicationServiceTests,RedisProtectedEndpointRateLimitIntegrationTests test` | 通过 | 8 个测试通过，覆盖我的提交列表缓存命中和提交限流覆写语义。 |
| `SCENARIOS=read_request_ladder,write_path PERF_PROFILE=contract /opt/miniconda3/bin/python3 ops/perf/run_perf_suite.py` | 通过 | `STRESS-0612022949/cache-fix-targeted`：读阶梯 50/200/500/1000 均 0 错误、0 个 5xx；写路径 10/30/50/100 均 0 错误、0 个 5xx、0 个 429。 |
| `SCENARIOS=soak_stability PERF_PROFILE=contract /opt/miniconda3/bin/python3 ops/perf/run_perf_suite.py` | 通过 | `STRESS-0612022949/cache-fix-soak`：100 并发 10 分钟，384751 请求，P95 20.36ms，错误率 0，5xx=0。 |

## 4. 未完成验证

| 项目 | 状态 | 原因 | 下一步 |
| --- | --- | --- | --- |
| 完整 `PERF_PROFILE=contract` 端到端复测 | 阻塞 | 本轮已重跑失败场景 read/write 和 10 分钟 soak；未在最后一次代码修复后重新执行包含文件、通知、SSE、fake lab_runtime 的完整端到端合同。 | 如需关闭“完整合同未复跑”风险，直接复用 `/tmp/aubb-STRESS-0612022949/manifest.json` 执行完整 profile。 |
| 严格读请求长尾阈值 | 失败 | 修复后 read ladder 500/1000 已无 5xx，但 500 并发 P95 2346.07ms、1000 并发 P95 2713.40ms，仍高于 `goal-stress.md` 的公共读请求 P95 < 500ms、P99 < 1500ms 阈值。 | 继续削减 `my_assignments`、`teacher_assignments`、`teacher_assignment_submissions` 等业务读端点 DB 占用，或重新定义本地极限并发容量边界。 |
| 判题轮询 500 与通知 500/SSE 100/300 | 阻塞 | `STRESS-0612022949/contract-run` 已证明 judge/notification 500 轮询通过，SSE 20 通过；SSE 100/300 和真实判题五类结果仍未执行。 | 补 SSE 长连接和真实 go-judge 提交/报告/重评专项。 |
| Kubernetes Web 终端真实 runtime | 阻塞 | 当前本地环境仍是 fake runtime，未配置真实 kubeconfig/namespace。 | 配置真实 Kubernetes runtime 后单独验证 Pod、WebSocket I/O、重连、停止/重置和资源清理。 |

## 5. 当前结论

本轮已完成可直接修复的代码项，并用目标单测和失败场景复测证明：压测 runner 不再无限等待，成绩册热点读路径具备短 TTL 缓存且写后会失效，我的提交列表在缓存命中时不再重复查 assignment/count/page，提交写路径不再因默认 10/min 限流在合同流量下产生 429。

完整压力合同仍不能声明 `通过`：失败场景的 5xx/429 已修复，但严格读请求长尾阈值、真实 Kubernetes Web 终端和多个专项覆盖仍未关闭。
