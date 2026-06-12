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
| P1-STRESS-005 / Kubernetes Web 终端真实 runtime | 真实 Kubernetes runtime 完全未证明；页面启动终端实验后，如果首个 current session 响应仍是 `PROVISIONING`，学生端不会继续刷新，导致真实 Pod 已 Running 但页面仍停在“正在启动”，无法打开终端。 | 手工以 `AUBB_LAB_RUNTIME_MODE=kubernetes` 启动后端并跑真实 Pod/WebSocket smoke；为 `useMyCurrentLabSessionQuery` 增加 `REQUESTED` / `PROVISIONING` 期间 2 秒轮询，稳定态停止轮询。 | 通过 | `npm test -- use-lab-query` 通过；`STRESS-0612045100-k8s-runtime` API+WebSocket smoke 通过；Playwright MCP 学生页从“正在启动”自动刷新到“运行中”并打开 Web 终端，截图见 `product-stress-test-screenshots/STRESS-0612045100-k8s-runtime/student-terminal-connected.png`。 |
| P1-STRESS-005 / Kubernetes WebSocket 并发容量 | 第十二批只证明单会话真实 Pod/WebSocket/Playwright smoke，未证明 Kubernetes session / WebSocket 5/10/20 并发、10 分钟保持、重连、重置和清理。 | 为合同 runner 增加 `lab_terminal_websocket` 场景，5/10/20 并发各 600 秒；每个 worker 启动真实 Kubernetes session，执行初连 echo、重连 echo、周期 keepalive echo、reset echo，并采样 Pod phase/ready/restart/cleanup。 | 通过 | `STRESS-0612053038-k8s-ws` 三档错误率均为 0、5xx=0，初连/重连/重置分别 5/5/5、10/10/10、20/20/20 成功；Pod 峰值 5/10/20，最大重启 0，压测后和 Playwright MCP 回归后 namespace 无残留 Pod。 |
| P1-STRESS-003 / 真实 go-judge 全链路 | 判题轮询已通过，但真实提交 5/10/20、sample-run 5/10/20、五类结果、报告下载和重评 5/10 未闭环；初版 go-judge runner 把不可访问学生混入班级作业且 sample-run 紧循环触发 403/429。 | 为数据准备输出结构化编程题、`judgeQuestionId`、`judgeAnswerId` 和 `judgeStudentUsernames`；runner 增加 `go_judge_sample_runs`、`go_judge_submission_chain`、`go_judge_requeue`，按作业可访问学生过滤 token，并对 sample-run 加用户级间隔；结果统计保留真实 verdict，同时把“编译失败”摘要归类为 `COMPILE_ERROR` 合同结果类别。 | 通过 | `STRESS-0612064213-gojudge` 证明 sample-run 5/10/20、真实提交 5/10/20、学生/教师报告下载、五类结果 SQL 汇总和重评 5/10 均错误率 0、5xx=0；`/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py ops/perf/setup_perf_data_test.py` 共 24 个测试通过。 |
| P2-STRESS-005 / 文件与对象存储专项 | 原合同 runner 只覆盖教师课程资源上传 5/10、下载 20/100，并且普通下载请求读取后丢弃响应体，无法形成 `goal-stress.md` 要求的 size、Content-Type、SHA256 证据。第十五批把上传 payload 改为 64KiB、1MiB、20MiB 三档后，若继续使用通用循环 runner，20 并发 60 秒会反复写入 20MiB 对象，存在本地 MinIO/磁盘被压测工具自身打满的风险。`STRESS-06120804-filematrix` 首轮进一步暴露 20MiB 上传 413 和文件下载 300 并发下 Hikari 连接耗尽导致 3262 个 5xx。 | 扩展合同计划到上传 5/10/20、下载 20/100/300；下载改为专用 `run_file_download_scenario`，覆盖课程资源、判题报告、成绩册导出/报告、班级成绩册导出/报告、实验报告附件和提交附件。第十六批将上传改为专用 `run_file_upload_scenario`：默认每个 worker 上传 64KiB、1MiB、20MiB 各一次并等待阶段结束，可用 `PERF_FILE_UPLOADS_PER_WORKER` 覆写；每个上传阶段写出 `file_upload_integrity_<concurrency>.json`。第十七批补 `spring.servlet.multipart` 25/26MB 限制，移除下载/导出/报告入口外层只读事务，上传阶段不再因 20MiB 延迟跳过 20 并发，并让学生判题报告下载复用已授权缓存视图。 | 通过 | 定向 Java/Python 测试通过；`STRESS-06120804-filematrix` 证明上传 5/10/20 全 201，下载 20/100 全 200，最终下载 300 为 42472 次全 200、5xx=0。P2-STRESS-005 的容量子项关闭；权限负例、MinIO 指标和 gradebook 尾延迟仍不能改为通过。 |
| P1-STRESS-004 / SSE 长连接覆盖 | 原 `notification_sse` 只有 20 并发 60 秒，且 worker 读到短超时后关闭连接再重连，不能证明 20/100/300 的长连接保持。 | 将合同计划改为 SSE 20 并发 5 分钟、100/300 并发各 10 分钟；`run_sse_scenario` 每个 worker 建立一次 SSE 连接并保持到阶段结束，记录连接数、读取超时但未断连次数、读取 chunk 和保持至阶段结束计数。 | 通过 | `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py` 共 21 个测试通过，覆盖合同计划时长。实际 SSE 100/300 压测尚未执行，7.10 仍保持阻塞。 |
| P2-STRESS-002 / 30 分钟 soak 合同 | 旧合同 profile 中 `soak_stability` 仍是 100 并发 10 分钟 smoke，不能直接证明 `goal-stress.md` 7.15 要求的 30 分钟容量边界。 | 将合同 profile 的 `soak_stability` 调整为 100 并发 1800 秒；保留 `MAX_STAGE_COUNT`、`MAX_STAGE_CONCURRENCY`、`ONLY_STAGE_CONCURRENCY` 诊断开关用于短诊断。 | 通过 | `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py` 共 21 个测试通过，覆盖 1800 秒计划。实际 30 分钟 soak 尚未执行，7.15 仍保持阻塞。 |

## 2. 本轮代码改动

- `server/ops/perf/run_perf_suite.py`：新增 `PERF_REQUEST_TIMEOUT_SECONDS`、`PERF_STAGE_TIMEOUT_GRACE_SECONDS`，stage worker 受 `wait_for_stage_workers(...)` 保护，超时会记录 `EXC:StageTimeout` 并取消未完成 task。
- `server/common/cache`：`CacheService` 新增 `evictByPrefix(...)` 默认方法；`RedisCacheService` 使用 Redis SCAN 匹配并删除缓存 key 前缀。
- `GradebookApplicationService`：教师成绩册页、学生我的成绩册使用 `gradebook-page-ttl` 短 TTL 缓存；整课、班级、学生我的成绩册入口均不声明外层只读事务。
- `GradingApplicationService`：成绩发布和人工批改成功后，在事务提交后清理同一开课下的成绩册页缓存。
- `application.yaml` / `RedisEnhancementProperties`：新增 `AUBB_REDIS_CACHE_GRADEBOOK_PAGE_TTL`，默认 `PT10S`。
- `SubmissionApplicationService`：我的提交列表使用 `my-submission-page-ttl` 短 TTL 缓存 assignment 元数据和分页响应；提交成功后按前缀清理该用户该作业的提交页缓存。
- `application.yaml` / `RedisEnhancementProperties`：新增 `AUBB_REDIS_CACHE_MY_SUBMISSION_PAGE_TTL`，默认 `PT5S`；`submission-create` 默认限流由 10/min 调整为 60/min。
- `web/src/features/lab/hooks/use-lab-query.ts`：学生当前终端会话在 `REQUESTED` / `PROVISIONING` 状态下每 2 秒 refetch，`RUNNING` / `STOPPED` 等稳定态不继续轮询，避免真实 Kubernetes Pod 已 Running 但页面卡在“正在启动”。
- `server/ops/perf/run_perf_suite.py`：新增 `lab_terminal_websocket` 合同场景、`ONLY_STAGE_CONCURRENCY` 精确分段过滤和 WebSocket URL 构造；真实 Kubernetes runtime 下验证初连、重连、keepalive、reset 和 stop 清理。
- `server/ops/perf/run_perf_suite_test.py`：新增合同计划、600 秒时长、精确并发过滤、WebSocket URL 和缺少目标时失败测试。
- `server/ops/perf/setup_perf_data.py`：新增结构化 go-judge 编程作业、真实 seed 提交、`judgeQuestionId` / `judgeAnswerId` / `judgeStudentUsernames` manifest 字段，确保 go-judge 压测使用作业可访问学生。
- `server/ops/perf/run_perf_suite.py`：新增 `go_judge_sample_runs`、`go_judge_submission_chain`、`go_judge_requeue` 合同场景；sample-run 增加用户级间隔；真实提交链路下载学生/教师报告；统计保留真实 verdict 并输出合同结果类别。
- `server/ops/perf/setup_perf_data_test.py`、`server/ops/perf/run_perf_suite_test.py`：覆盖结构化编程作业、学生过滤、sample-run 间隔、五类代码变体和编译失败分类。
- `server/ops/perf/run_perf_suite.py`：合同 profile 补齐文件上传 20 并发、文件下载 300 并发、SSE 20/100/300 长连接保持和 30 分钟 soak；文件上传 payload 默认包含 64KiB、1MiB、20MiB 三档。
- `server/ops/perf/run_perf_suite.py`：新增专用 `run_file_upload_scenario`，默认每个 worker 上传一轮小/中/大文件并保持到阶段结束，写出 `file_upload_integrity_<concurrency>.json`，避免 20MiB payload 在 60 秒阶段内无限循环写入对象存储。
- `server/ops/perf/run_perf_suite.py`：文件上传 stage 即使 P95 超过 3000ms 也继续执行更高并发档位，只有错误率超过 5% 时才提前停止，避免 20MiB 上传延迟误跳过 20 并发合同项。
- `server/ops/perf/run_perf_suite.py`：新增文件下载目标矩阵和 `run_file_download_scenario`，下载成功后汇总 Content-Type、文件大小、SHA256，并写出 `file_download_integrity_<concurrency>.json`。
- `server/ops/perf/run_perf_suite.py`：`run_sse_scenario` 改为单连接保持到阶段结束，避免短连接反复重连误作 SSE 长连接容量证据。
- `server/ops/perf/run_perf_suite_test.py`：覆盖文件下载目标矩阵、SHA256 聚合、SSE/文件/soak 合同计划。
- `server/ops/perf/setup_perf_data.py`：为首个学生上传并提交一个作业附件，上传一个实验报告附件并保存报告，manifest 输出 `submissionArtifactId`、`submissionArtifactSubmissionId`、`labReportAttachmentId`；结构化作业附件放入 `answers[].artifactIds`，避免结构化提交校验拒绝顶层 `artifactIds`。
- `server/ops/perf/setup_perf_data_test.py`：覆盖压测附件内容生成，避免附件 fixture 大小不可控。
- `server/src/main/resources/application.yaml`：本地合同压测默认允许 25MB multipart 文件和 26MB 请求，覆盖 20MiB 上传矩阵。
- `CourseResourceApplicationService`、`SubmissionApplicationService`、`LabApplicationService`、`JudgeApplicationService`、`GradebookApplicationService`：下载、导出和报告入口不再持有外层 `@Transactional(readOnly = true)`，避免对象存储读取和报表生成期间占用 JDBC 连接。
- `JudgeApplicationService`：学生判题报告下载复用 `getMyJudgeJobReport(...)` 的已授权短 TTL 缓存视图，减少 300 并发下载下重复 job/submission/assignment 查询。

## 3. 已执行验证

| 命令 | 状态 | 说明 |
| --- | --- | --- |
| `bash ./mvnw -Dtest=GradebookApplicationServiceTests,RedisCacheServiceTests,GradingApplicationServiceTests test` | 通过 | 13 个测试通过，覆盖成绩册缓存、无外层事务、Redis 前缀删除和写后失效。 |
| `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py` | 通过 | 12 个测试通过，覆盖 stage 超时、结果 flush、artifact 目录、endpointStats、`lab_terminal_websocket` 合同计划和 WebSocket URL。 |
| `just healthcheck-strict` | 通过 | 后端 readiness/OpenAPI、前端登录页和本地依赖基线通过。 |
| `bash ./mvnw -Dtest=SubmissionApplicationServiceTests,RedisProtectedEndpointRateLimitIntegrationTests test` | 通过 | 8 个测试通过，覆盖我的提交列表缓存命中和提交限流覆写语义。 |
| `SCENARIOS=read_request_ladder,write_path PERF_PROFILE=contract /opt/miniconda3/bin/python3 ops/perf/run_perf_suite.py` | 通过 | `STRESS-0612022949/cache-fix-targeted`：读阶梯 50/200/500/1000 均 0 错误、0 个 5xx；写路径 10/30/50/100 均 0 错误、0 个 5xx、0 个 429。 |
| `SCENARIOS=soak_stability PERF_PROFILE=contract /opt/miniconda3/bin/python3 ops/perf/run_perf_suite.py` | 通过 | `STRESS-0612022949/cache-fix-soak`：100 并发 10 分钟，384751 请求，P95 20.36ms，错误率 0，5xx=0。 |
| `npm test -- use-lab-query` | 通过 | 3 个前端单元测试通过，覆盖学生实验报告 404 为空状态、终端会话 `PROVISIONING` 自动轮询、`RUNNING` 稳定态不继续轮询。 |
| `STRESS-0612045100-k8s-runtime` API + WebSocket smoke | 通过 | `aubb-lab-stress-1533` Pod Running，WebSocket 初连与重连均观察 `AUBB_K8S_EXEC_OK`，停止后 namespace 无残留 Pod。 |
| Playwright MCP 学生实验页真实 runtime 回归 | 通过 | 学生页创建 `aubb-lab-stress-1535` 后从“正在启动”自动刷新到“运行中”，打开 Web 终端并保存截图；页面停止后 DB 为 `STOPPED`，namespace 无残留 Pod。 |
| `STRESS-0612053038-k8s-ws` Kubernetes WebSocket 5/10/20 | 通过 | 三档各 600 秒，错误率均为 0、5xx=0；初连/重连/重置均成功；Pod 峰值 5/10/20，最大重启 0，结束后 namespace 无残留 Pod。 |
| Playwright MCP 学生实验页 Kubernetes WebSocket 回归 | 通过 | 学生页观察“运行中”“已连接”和 `UI-K8S-WS-OK` echo 回显；页面停止后 namespace 无残留 Pod。 |
| `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py ops/perf/setup_perf_data_test.py` | 通过 | 24 个测试通过，覆盖 go-judge 结构化数据准备、作业可访问学生过滤、sample-run 间隔、真实 go-judge 合同场景、五类代码变体和编译失败分类。 |
| `STRESS-0612064213-gojudge` sample-run 5/10/20 | 通过 | 三档各 120 秒，130 / 260 / 520 次请求，错误率 0、5xx=0。 |
| `STRESS-0612064213-gojudge` 真实提交 5/10/20 | 通过 | 三档各 300 秒，916 / 1646 / 2060 次提交，学生/教师报告下载均与提交数一致，错误率 0、5xx=0。 |
| `STRESS-0612064213-gojudge` 五类结果 SQL 汇总 | 通过 | `ACCEPTED=916`、`WRONG_ANSWER=919`、`COMPILE_ERROR=925`、`RUNTIME_ERROR=931`、`TIME_LIMIT_EXCEEDED=932`，4623 个 job 均有报告对象。 |
| `STRESS-0612064213-gojudge` requeue 5/10 | 通过 | 两档各 120 秒，创建 380 / 640 个 `MANUAL_REJUDGE` job，均 `SUCCEEDED`，错误率 0、5xx=0。 |
| `/opt/miniconda3/bin/python3 -m unittest ops/perf/setup_perf_data_test.py ops/perf/run_perf_suite_test.py` | 通过 | 31 个测试通过，覆盖文件上传上限、上传完整性聚合、文件下载矩阵、SHA256 聚合、SSE 长连接计划、30 分钟 soak 计划和附件 fixture 生成。 |
| `bash ./mvnw -Dtest=CourseResourceApplicationServiceTests,LabApplicationServiceTests,SubmissionApplicationServiceTests,JudgeApplicationServiceTests,GradebookApplicationServiceTests test` | 通过 | 19 个测试通过，覆盖下载/导出/报告入口不持有外层只读事务，以及学生判题报告下载复用已授权缓存视图。 |
| `/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py ops/perf/setup_perf_data_test.py` | 通过 | 34 个测试通过，覆盖结构化附件 payload、文件上传 20 阶段不中断、错误率触发中断和文件完整性聚合。 |
| `STRESS-06120804-filematrix` 文件矩阵首轮 | 失败 | 首轮暴露 20MiB 上传 413 和下载 300 并发 3262 个 5xx；证据保留为 `raw/STRESS-06120804-filematrix/file-matrix/perf_results_file_matrix.json`。 |
| `STRESS-06120804-filematrix` multipart/no-tx 后复测 | 失败 | 上传 5/10 全 201，下载 20/100 全 200，下载 300 仅剩 1 个 500；证据为 `raw/STRESS-06120804-filematrix/file-matrix-after-download-notx/perf_results_file_matrix_after_download_notx.json`。 |
| `STRESS-06120804-filematrix` 上传 20 补跑 | 通过 | 20 并发 60 次上传全 201，覆盖 64KiB、1MiB、20MiB 三档；证据为 `raw/STRESS-06120804-filematrix/file-upload-20-after-break-fix/perf_results_file_upload_20_after_break_fix.json`。 |
| `STRESS-06120804-filematrix` 下载 300 判题报告缓存修复后复测 | 通过 | 300 并发 120 秒，42472 次下载全 200，错误率 0，5xx=0；证据为 `raw/STRESS-06120804-filematrix/file-download-300-after-judge-cache/perf_results_file_download_300_after_judge_cache.json`。 |
| `bash ./mvnw test` | 通过 | 391 个后端测试通过，0 失败、0 错误。 |
| `cd docs && npm run docs:build` | 通过 | VitePress 文档构建通过，仅保留既有 chunk size warning。 |
| 本轮证据敏感信息扫描 | 通过 | `STRESS-0612053038-k8s-ws` 和 `STRESS-0612064213-gojudge` 证据目录未匹配 token、Authorization、cookie、私钥等敏感模式。 |

## 4. 未完成验证

| 项目 | 状态 | 原因 | 下一步 |
| --- | --- | --- | --- |
| 完整 `PERF_PROFILE=contract` 端到端复测 | 阻塞 | 本轮已重跑失败场景 read/write 和 10 分钟 smoke soak；第十五/十六批已把合同 profile 对齐到文件 20/300、SSE 20/100/300 和 30 分钟 soak，并控制文件上传写入量，但尚未执行新的完整端到端合同。 | 如需关闭“完整合同未复跑”风险，直接复用最新 manifest 执行完整 profile，并为文件矩阵保存 `file_upload_integrity_<concurrency>.json` 与 `file_download_integrity_<concurrency>.json`。 |
| 严格读请求长尾阈值 | 失败 | 修复后 read ladder 500/1000 已无 5xx，但 500 并发 P95 2346.07ms、1000 并发 P95 2713.40ms，仍高于 `goal-stress.md` 的公共读请求 P95 < 500ms、P99 < 1500ms 阈值。 | 继续削减 `my_assignments`、`teacher_assignments`、`teacher_assignment_submissions` 等业务读端点 DB 占用，或重新定义本地极限并发容量边界。 |
| 通知 500/SSE 100/300 | 阻塞 | `STRESS-0612022949/contract-run` 已证明通知 500 轮询和旧 SSE 20 子集通过；第十五批已修正 SSE runner 为长连接保持并补 20/100/300 计划，但尚未执行。 | 执行 `SCENARIOS=notification_sse PERF_PROFILE=contract`，记录 20/100/300 连接成功率、断线率和保持至阶段结束计数。 |
| 文件与对象存储权限负例和 MinIO 指标 | 阻塞 | 文件上传 5/10/20 和文件下载 20/100/300 容量矩阵已执行并修复到 0 个 5xx；但 7.9 仍要求权限负例、对象存储指标和异常输入证据，当前只保存了上传/下载完整性 JSON 和基础资源采样。 | 执行文件 401/403/413/错误 Content-Type 高并发负例，补 MinIO 指标和对象存储资源曲线；gradebook export/report 尾延迟单独进入后续优化。 |
| Kubernetes CPU/内存曲线与 runtime 启动治理 | 阻塞 | 第十三批已完成 WebSocket/Kubernetes 5/10/20 并发容量，但本地 Metrics API 不可用，`kubectl top` 无法记录 Pod CPU/内存；`just dev-up` 默认脚本仍未原生传入 Kubernetes runtime env。 | 启用 metrics-server 或替代 Pod 资源采样；整理 `just dev-up`/文档化命令，使真实 Kubernetes runtime 启动入口可复用。 |

## 5. 当前结论

本轮已完成可直接修复的代码项，并用目标单测和失败场景复测证明：压测 runner 不再无限等待，成绩册热点读路径具备短 TTL 缓存且写后会失效，我的提交列表在缓存命中时不再重复查 assignment/count/page，提交写路径不再因默认 10/min 限流在合同流量下产生 429。

完整压力合同仍不能声明 `通过`：失败场景的 5xx/429 已修复，真实 Kubernetes Web 终端单会话链路已打通并修复页面启动后不刷新的问题，Kubernetes/WebSocket 5/10/20 并发容量已关闭，真实 go-judge sample-run/提交/五类结果/报告下载/重评也已关闭，文件上传 5/10/20 与文件下载 20/100/300 已修复到 0 个 5xx；但严格读请求长尾阈值、SSE 100/300、30 分钟完整 soak、文件权限负例、MinIO 指标、Kubernetes CPU/内存曲线和多个专项覆盖仍未关闭。
