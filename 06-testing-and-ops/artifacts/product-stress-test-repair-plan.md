# AUBB 压力问题修复计划与执行记录

> 本文件记录 2026-06-12 本轮修复范围。状态只使用 `通过`、`失败`、`阻塞`、`不适用`。本轮不把未复测的完整压力合同标为通过。

## 1. 修复范围

| 关联问题 | 修复目标 | 计划 | 执行状态 | 验证 |
| --- | --- | --- | --- | --- |
| P3-STRESS-001 / runner 卡死风险 | 压测 stage 不应因少量挂起请求无限等待；每个 stage 应能超时、取消 worker 并输出可定位状态。 | 为 `run_perf_suite.py` 增加请求超时配置、stage 级超时、worker 取消和 `EXC:StageTimeout` 统计；阶段结果立即 flush。 | 通过 | `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py`，9 个测试通过。 |
| P1-STRESS-001 / P1-STRESS-002 | 500 并发混合读中 `teacher_gradebook` 曾因 Hikari 连接耗尽产生 500；成绩册页读应减少重复 DB 查询和外层事务连接占用。 | 为教师成绩册页和学生我的成绩册增加短 TTL Redis 缓存；移除班级成绩册外层只读事务；缓存命中不包在 service 外层事务内。 | 通过 | `GradebookApplicationServiceTests` 覆盖整课、班级、学生成绩册无外层读事务和重复请求复用缓存。 |
| P1-STRESS-001 / 成绩写后一致性 | 成绩册页缓存不能让批改、导入、发布后长期返回旧数据。 | 在通用 `CacheService` 增加按 key 前缀删除；Redis 实现用 SCAN 删除匹配 key；成绩发布和人工批改后按开课前缀清理教师/学生成绩册缓存。 | 通过 | `RedisCacheServiceTests` 覆盖前缀删除；`GradingApplicationServiceTests` 覆盖发布成绩后清理 `teacherGradebookPage` 与 `myGradebook` 前缀。 |

## 2. 本轮代码改动

- `server/ops/perf/run_perf_suite.py`：新增 `PERF_REQUEST_TIMEOUT_SECONDS`、`PERF_STAGE_TIMEOUT_GRACE_SECONDS`，stage worker 受 `wait_for_stage_workers(...)` 保护，超时会记录 `EXC:StageTimeout` 并取消未完成 task。
- `server/common/cache`：`CacheService` 新增 `evictByPrefix(...)` 默认方法；`RedisCacheService` 使用 Redis SCAN 匹配并删除缓存 key 前缀。
- `GradebookApplicationService`：教师成绩册页、学生我的成绩册使用 `gradebook-page-ttl` 短 TTL 缓存；整课、班级、学生我的成绩册入口均不声明外层只读事务。
- `GradingApplicationService`：成绩发布和人工批改成功后，在事务提交后清理同一开课下的成绩册页缓存。
- `application.yaml` / `RedisEnhancementProperties`：新增 `AUBB_REDIS_CACHE_GRADEBOOK_PAGE_TTL`，默认 `PT10S`。

## 3. 已执行验证

| 命令 | 状态 | 说明 |
| --- | --- | --- |
| `bash ./mvnw -Dtest=GradebookApplicationServiceTests,RedisCacheServiceTests,GradingApplicationServiceTests test` | 通过 | 13 个测试通过，覆盖成绩册缓存、无外层事务、Redis 前缀删除和写后失效。 |
| `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py` | 通过 | 9 个测试通过，覆盖 stage 超时、结果 flush、artifact 目录和 endpointStats。 |
| `just healthcheck-strict` | 通过 | 后端 readiness/OpenAPI、前端登录页和本地依赖基线通过。 |

## 4. 未完成验证

| 项目 | 状态 | 原因 | 下一步 |
| --- | --- | --- | --- |
| 修复后 `read_request_ladder` 500/1000 | 失败 | 第十批代码修复后尚未重跑完整压力阶梯；本轮只有修复前 `STRESS-06120151-read500-after-stage-timeout` 证明 500 阶段仍有 1 个 `teacher_gradebook` 500。 | 重启后端后执行完整 `PERF_PROFILE=contract` 或至少 `read_request_ladder` 50/200/500，采集 endpointStats、Hikari、PostgreSQL、Redis 命中率。 |
| 判题轮询 500 与通知 500/SSE 100/300 | 失败 | 第九批只证明 50/200；第十批未重跑压力。 | 按 `goal-stress.md` 重跑专项，保留资源采样与服务日志。 |
| 写入 429 与 soak | 失败 | 本轮未修改限流/写入容量策略。 | 复跑写入和 soak，区分产品允许限流与容量缺陷。 |
| Kubernetes Web 终端真实 runtime | 阻塞 | 当前本地环境仍是 fake runtime，未配置真实 kubeconfig/namespace。 | 配置真实 Kubernetes runtime 后单独验证 Pod、WebSocket I/O、重连、停止/重置和资源清理。 |

## 5. 当前结论

本轮已完成可直接修复的代码项，并用目标单测证明：压测 runner 不再无限等待，成绩册热点读路径具备短 TTL 缓存且写后会失效，班级成绩册缓存命中不会被外层只读事务提前占用连接。

完整压力合同仍为 `失败`，因为修复后 500/1000 阶段、写入、soak、真实 Kubernetes Web 终端和多个专项尚未重新执行。
