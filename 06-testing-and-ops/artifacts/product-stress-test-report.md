# AUBB 交付前压力测试报告

## 1. 测试元信息

- 执行日期：2026-06-11
- 工作区：`/Users/moorefoss/Code/AUBB`
- 执行合同：`goal-stress.md`
- 目标环境：本地真实前后端与本地 Docker 依赖，不对生产或外部真实用户环境压测
- 前端地址：`http://127.0.0.1:3000`
- 后端地址：`http://127.0.0.1:18080`
- 运行时模式：本地 fake 实验运行时；本轮只证明 fake runtime 会话路径，不声明 Kubernetes 容量
- 机器配置摘要：MacBookPro18,3，8 CPU，16 GiB 内存，macOS 26.5.1；Java 25.0.3，Docker 29.4.3，Node 24.15.0，npm 11.14.1。证据：`product-stress-test-evidence/commands/20-machine-and-tool-summary.log`
- 初始 `just status` 摘要：`server/`、`web/`、`docs/` 均在 `main...origin/main`，dirty entries 均为 `0`；AUBB root 不是 git 仓库
- 最终 `just status` 摘要：`server/`、`web/`、`docs/` dirty entries 均为 `0`；`server/` 因提交 `447fa75 feat(perf): 补齐合同压测场景` ahead 1，`docs/` 因提交压力测试报告与证据 ahead 1。初次最终状态证据见 `product-stress-test-evidence/commands/34-final-just-status-post-docs-commit.log`；覆盖矩阵补录后的最终状态证据见 `product-stress-test-evidence/commands/38-final-just-status-post-coverage-matrix-commit.log`。`docs/06-testing-and-ops/artifacts/` 为 docs 仓库忽略目录，本轮压力测试报告和证据已按合同使用 `git add -f` 纳入 docs 子仓库提交范围。

## 2. 总体结论

- 结论：不通过全平台合同容量目标。第十一批已修复核心 runner 中的高并发 5xx 和写路径 429，但 500/1000 读请求长尾仍超过 `goal-stress.md` 严格阈值，真实 Kubernetes Web 终端和多个专项覆盖仍未关闭。
- 2026-06-11 修复批次结论：已完成第一批 P1 高频读路径与压测脚本修复，并通过后端单测/集成门禁；但尚未复跑 `PERF_PROFILE=contract` 全量压力测试，故本报告总体验收结论仍保持“不通过”。
- 2026-06-11 P1 复测与第八批修复结论：已复跑读请求 / 判题轮询 / 通知轮询 P1 诊断和九轮 read-label 混合读诊断，证明认证 principal cache、提交列表批量答案加载、`/auth/me` 默认快照读取、access token 会话活跃缓存预热、教师提交列表敏感 scope 预解析、会话活跃缓存入口无事务、认证 principal 缓存入口无事务、通知轮询缓存入口无事务均有收益；第八批 no-tx 复测确认通知未读数 500 并发 5xx 从 1302 降到 13，但混合读总 5xx 升到 14238，200/500 并发仍有 5xx/P99 超阈值，P1 仍为失败。
- 2026-06-12 第九批修复结论：作业列表、提交列表、成绩册高频读入口已移除外层读事务，perf runner 增加 `MAX_STAGE_CONCURRENCY` / `MAX_STAGE_COUNT` 诊断开关，并将默认 Hikari 取连接等待从 500ms 调整为 2500ms。短诊断证明 `read_request_ladder`、`judge_polling`、`notification_polling` 的 50/200 并发均为 0 个 5xx；但尚未执行 500/1000 阶段和完整 `PERF_PROFILE=contract` 全合同复测，故总体验收结论仍保持“不通过”。
- 2026-06-12 第十批代码修复结论：`STRESS-06120151-read500-after-stage-timeout` 证明 500 阶段仍有 1 个 `teacher_gradebook` 500，服务日志定位到成绩册数据库查询等待 Hikari 连接超时。第十批已修复 perf runner stage 卡死风险，新增成绩册页短 TTL 缓存、班级成绩册 no-tx、Redis 前缀删除和成绩写后缓存失效；目标单测通过。修复后完整压力阶梯尚未执行，因此总体验收结论仍保持“不通过”。
- 2026-06-12 第十一批修复结论：`STRESS-0612022949/contract-run` 完整合同复测中 read ladder 500/1000 各有 1 个 5xx，write path 30/50 出现 429。第十一批新增我的提交列表 assignment/page 短 TTL 缓存和写后失效，将 `submission-create` 默认限流从 10/min 调整为 60/min。修复后 `cache-fix-targeted` 证明 read ladder 50/200/500/1000 与 write path 10/30/50/100 均 0 错误、0 个 5xx、写路径 0 个 429；`cache-fix-soak` 证明 100 并发 10 分钟 smoke soak 0 错误。
- 已证明容量边界：读请求 50/200/500/1000 在修复后均 5xx=0；写路径 10/30/50/100 在修复后均 429=0、5xx=0；判题轮询 50/200/500 通过；通知轮询 50/200/500 通过；文件上传 10 并发、文件下载 100 并发通过；SSE 20 并发 1 分钟通过；fake runtime 实验会话 10 并发 1 分钟通过；100 并发 10 分钟 smoke soak 通过。
- 未证明或失败范围：读请求 500/1000 长尾仍超过 P95 < 500ms、P99 < 1500ms 的严格阈值；登录风暴未执行；真实 go-judge 缺少 5 类结果、报告下载和重评容量；SSE 100/300 未执行；完整 30 分钟 soak 未执行；未证明 Kubernetes 实验运行时容量。
- 真实 go-judge 判题结论：失败。数据准备阶段触发了 1 次真实编程提交，判题轮询 50/200/500 已通过，但未完成真实提交 5/10/20、五类结果、报告下载和重评容量证明。
- Web 终端 / Kubernetes runtime 结论：阻塞。本轮只证明本地 fake runtime 10 并发 smoke，当前环境未配置真实 Kubernetes runtime，不能声明 Web 终端生产容量通过。
- 是否建议对外交付：不建议按当前合同容量目标交付；若必须演示或内测，应限定为低并发、明确限流，并先完成连接池/读路径优化与重测。
- 交付限制或建议：继续治理 JDBC 连接池耗尽；最新 8 分钟阶梯已确认认证与通知缓存入口基本不再在命中时打开事务，但成绩册、提交、作业和课程列表等业务读路径仍会在高并发阶段耗尽连接池。下一批应优先削减这些业务读端点的事务与查询占用。

## 3. 输入与环境检查

| 输入 | 状态 | 证据或说明 |
| --- | --- | --- |
| `AGENTS.md`、`AGENTS-shared.md`、`server/AGENTS.md`、`web/AGENTS.md`、`docs/AGENTS.md` | 通过 | 已读取。 |
| `goal-stress.md` | 通过 | 已读取；本阶段只验证容量、稳定性和瓶颈边界，不替代第二轮功能验收。 |
| `goal.md`、`goal-test.md` | 通过 | 已读取；round2 功能验收结论保持以 `product-full-verification-round2-report.md` 为准。 |
| round2 报告和修复清单 | 通过 | 已读取；当前 round2 功能验收结论为 `通过`，无剩余 P0/P1。 |
| `server/ops/perf/README.md`、`setup_perf_data.py`、`run_perf_suite.py`、`k6-core-apis.js` | 通过 | 已读取；现有脚本覆盖核心 API 读、写提交、判题轮询和基础资源采样。 |
| `docs/02-process-docs/software-requirements-specification.md` 性能要求 | 通过 | `NFR-PERF-01` 常规页面 95th 不高于 2 秒；`NFR-PERF-02` 提交受理不高于 2 秒；`NFR-PERF-03` 评测状态感知不高于 5 秒。 |
| `docs/06-testing-and-ops/testing-strategy.md` | 通过 | 已读取；主链路包括登录、建课/选课、发布、提交、自动评测、批改、成绩发布。 |
| `docs/06-testing-and-ops/observability.md` | 通过 | 已读取；关键指标包括提交成功率、评测成功率与耗时、关键接口异常率。 |
| `docs/06-testing-and-ops/environments-and-deployment.md` | 通过 | 已读取；fake 与 Kubernetes 实验运行时必须区分。 |
| `env/e2e.example` | 通过 | 已读取；真实本地凭据只来自 `env/e2e.env`，不得提交。 |

## 4. 命令门禁结果

| 顺序 | 命令 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | `just status` | 通过 | `product-stress-test-evidence/commands/01-just-status.log`；`server/`、`web/`、`docs/` 均为 clean。 |
| 2 | `just --list` | 通过 | `product-stress-test-evidence/commands/02-just-list.log`；统一入口包含 `dev-up`、`healthcheck-strict`、`seed-fixtures`、`e2e-real`、`verify`、`verify-full`。 |
| 3 | `just dev-up` | 通过 | `product-stress-test-evidence/commands/03-just-dev-up.log`；Docker 依赖、后端 `18080`、前端 `3000` 就绪。 |
| 4 | `just healthcheck-strict` | 通过 | `product-stress-test-evidence/commands/04-just-healthcheck-strict.log`；严格 E2E 环境变量、后端 readiness/OpenAPI、前端登录页检查通过。 |
| 5 | `just seed-fixtures` | 通过 | `product-stress-test-evidence/commands/05-just-seed-fixtures.log`；`caseCount=22`、`passedCount=22`、`failedCount=0`。 |
| 6 | `just e2e-real` | 通过 | `product-stress-test-evidence/commands/06-just-e2e-real.log`；真实本地前后端 E2E `50 passed (4.0m)`。 |
| 7 | `just verify` | 通过 | `product-stress-test-evidence/commands/07-just-verify.log`；后端 `357` tests 通过，web lint/typecheck 通过，docs build 通过。 |
| 8 | `just verify-full` | 通过 | `product-stress-test-evidence/commands/08-just-verify-full.log`；后端 `357` tests 通过，web lint/typecheck、`71` files / `281` unit tests、Next build、docs build 通过。 |
| 9 | `cd docs && npm run docs:build` | 通过 | `product-stress-test-evidence/commands/09-docs-build-pre-stress.log`、`27-docs-build-completion-audit.log`、`31-docs-build-post-report-audit.log`、`36-docs-build-after-coverage-matrix.log`；VitePress build 通过，保留既有 chunk size warning。 |
| 10 | 后端 P1 高频读路径靶向测试与压测脚本单测 | 通过 | `product-stress-test-evidence/commands/40-server-p1-read-path-targeted-tests-20260611.log`；JWT 转换、JWT 紧凑合同、认证 principal 缓存、判题报告缓存、通知缓存、相关集成测试共 `44` 个 Java 测试通过，`ops/perf/run_perf_suite_test.py` 共 `3` 个 Python 测试通过。 |
| 11 | `cd server && bash ./mvnw test` | 通过 | `product-stress-test-evidence/commands/41-server-mvn-test-after-p1-read-path-fixes-20260611.log`；后端 `362` tests 通过，`BUILD SUCCESS`。 |
| 12 | P1 读/判题/通知诊断复测 | 失败 | `product-stress-test-evidence/commands/49-p1-read-judge-notification-diagnosis-20260611.log`；`raw/STRESS-06111800-diagnose/p1-diagnostic-results.json`。通知轮询 500 并发基本恢复，但读请求 500 并发错误率 22.54%，判题轮询 500 并发仍有 2905 个 5xx。 |
| 13 | read-label 端点级诊断 | 失败 | `product-stress-test-evidence/commands/52-read-label-diagnosis-20260611.log`；`raw/STRESS-06111820-readlabels/read-label-results.json`。混合读 500 并发错误率 22.51%，所有标签均受连接池耗尽影响，`teacher_assignment_submissions` 为最重读端点。 |
| 14 | 提交列表批量答案修复测试 | 通过 | `SubmissionAnswerApplicationServiceTests` 5 个测试通过；`SubmissionIntegrationTests` 19 个测试通过；`ops/perf/run_perf_suite_test.py` 4 个测试通过。 |
| 15 | read-label 修复后复测 | 失败 | `product-stress-test-evidence/commands/55-read-label-diagnosis-after-submission-bulk-answer-fix-20260611.log`；`raw/STRESS-06111832-readlabels-bulkfix/read-label-results.json`。50/200/500 并发均改善，但 200/500 仍不达标。 |
| 16 | auth principal cache 修复后启动与健康检查 | 通过 | `product-stress-test-evidence/commands/58-dev-restart-after-auth-principal-cache-fix-20260611.log`；`59-healthcheck-strict-after-auth-principal-cache-fix-20260611.log`。 |
| 17 | auth principal cache 修复后 read-label 复测 | 失败 | `product-stress-test-evidence/commands/60-read-label-diagnosis-after-auth-principal-cache-fix-20260611.log`；`raw/STRESS-06111855-authcache/read-label-results.json`。`auth_me` 200/500 并发 5xx 降为 0，但混合读 200/500 仍不达标。 |
| 18 | auth session active cache 修复后启动、健康检查与定向测试 | 通过 | `product-stress-test-evidence/commands/64-dev-restart-after-auth-session-cache-fix-20260611.log`；`65-healthcheck-strict-after-auth-session-cache-fix-20260611.log`；`67-server-auth-session-cache-targeted-tests-20260611.log`；`68-perf-runner-artifact-dir-tests-20260611.log`。 |
| 19 | auth session active cache 修复后 read-label 复测 | 失败 | `product-stress-test-evidence/commands/66-read-label-diagnosis-after-auth-session-cache-fix-20260611.log`；`raw/STRESS-06111935-sessionactive/read-label-results.json`。`auth_me` 200/500 并发 5xx 仍为 0，采样栈不再出现 `isAccessTokenActive`，但混合读 200/500 仍不达标。 |
| 20 | auth session active cache 修复后完整非浏览器门禁 | 通过 | `product-stress-test-evidence/commands/69-server-mvn-test-after-auth-session-cache-fix-20260611.log`；后端 `366` 个测试通过。`product-stress-test-evidence/commands/70-docs-build-after-auth-session-cache-fix-20260611.log`；docs build 通过，保留既有 chunk size warning。 |
| 21 | submission sensitive scope 修复后启动与健康检查 | 通过 | `product-stress-test-evidence/commands/71-dev-restart-after-submission-sensitive-scope-fix-20260611.log`；`72-healthcheck-strict-after-submission-sensitive-scope-fix-20260611.log`。 |
| 22 | submission sensitive scope 定向测试 | 通过 | `product-stress-test-evidence/commands/74-server-submission-sensitive-scope-targeted-tests-20260611.log`；`SubmissionApplicationServiceTests` 与 `PermissionAuthorizationServiceTests` 共 `11` 个测试通过。 |
| 23 | submission sensitive scope 修复后 read-label 复测 | 失败 | `product-stress-test-evidence/commands/73-read-label-diagnosis-after-submission-sensitive-scope-fix-20260611.log`；`raw/STRESS-06112012-submissionauth/read-label-results.json`。200 并发 5xx 降为 `9`，500 并发 5xx 降为 `5830`，但 500 并发错误率仍为 `13.09%`。 |
| 24 | submission sensitive scope 修复后完整非浏览器门禁 | 通过 | `product-stress-test-evidence/commands/75-server-mvn-test-after-submission-sensitive-scope-fix-20260611.log`；后端 `367` 个测试通过。`product-stress-test-evidence/commands/76-docs-build-after-submission-sensitive-scope-fix-20260611.log`；docs build 通过，保留既有 chunk size warning。 |
| 25 | auth session active TTL 对齐后启动、健康检查与 read-label 复测 | 失败 | `product-stress-test-evidence/commands/77-dev-restart-after-auth-active-ttl-fix-20260611.log`；`78-healthcheck-strict-after-auth-active-ttl-fix-20260611.log`；`79-read-label-diagnosis-after-auth-active-ttl-fix-20260611.log`；`raw/STRESS-06112041-authactivettl/read-label-results.json`。TTL 从 5m 提升到 2h 后，500 并发仍有 `6026` 个 5xx，日志窗口 `authSessionActiveStack=17788`，证明单独延长 TTL 不能绕过入口事务。 |
| 26 | auth session active no-tx 修复后启动、健康检查与 read-label 复测 | 失败 | `product-stress-test-evidence/commands/80-dev-restart-after-auth-active-no-tx-fix-20260611.log`；`81-healthcheck-strict-after-auth-active-no-tx-fix-20260611.log`；`82-read-label-diagnosis-after-auth-active-no-tx-fix-20260611.log`；`raw/STRESS-06112051-authnotx/read-label-results.json`。500 并发错误率降为 `8.04%`、5xx 降为 `5114`，但仍未达标。 |
| 27 | auth session active no-tx 定向与完整后端门禁 | 通过 | `product-stress-test-evidence/commands/83-server-auth-active-no-tx-targeted-tests-20260611.log`；认证/session/Redis 相关 `23` 个测试通过。`product-stress-test-evidence/commands/84-server-mvn-test-after-auth-active-no-tx-fix-20260611.log`；后端 `368` 个测试通过。 |
| 28 | auth session active no-tx 文档门禁 | 通过 | `product-stress-test-evidence/commands/85-docs-build-after-auth-active-no-tx-fix-20260611.log`；docs build 通过，保留既有 chunk size warning。 |
| 29 | auth principal no-tx 修复后启动、健康检查与 read-label 复测 | 失败 | `product-stress-test-evidence/commands/86-dev-restart-after-auth-principal-no-tx-fix-20260611.log`；`87-healthcheck-strict-after-auth-principal-no-tx-fix-20260611.log`；`88-read-label-diagnosis-after-auth-principal-no-tx-fix-20260611.log`；`raw/STRESS-06112118-principalnotx/read-label-results.json`。认证入口栈清零，但 500 并发仍有 `10791` 个 5xx，P1 仍失败。 |
| 30 | auth principal no-tx 定向与完整后端门禁 | 通过 | `product-stress-test-evidence/commands/89-server-auth-principal-no-tx-targeted-tests-20260611.log`；认证 principal/session/Redis 相关 `34` 个测试通过。`product-stress-test-evidence/commands/90-server-mvn-test-after-auth-principal-no-tx-fix-20260611.log`；后端 `369` 个测试通过。 |
| 31 | auth principal no-tx 文档门禁 | 通过 | `product-stress-test-evidence/commands/91-docs-build-after-auth-principal-no-tx-fix-20260611.log`；docs build 通过，保留既有 chunk size warning。 |
| 32 | notification polling no-tx 修复后启动、健康检查与 read-label 复测 | 失败 | `product-stress-test-evidence/commands/92-dev-restart-after-notification-polling-no-tx-fix-20260611.log`；`93-healthcheck-strict-after-notification-polling-no-tx-fix-20260611.log`；`94-read-label-diagnosis-after-notification-polling-no-tx-fix-20260611.log`；`raw/STRESS-06112149-notifnotx/read-label-results.json`。通知未读数 500 并发 5xx 降为 `13`，但混合读 500 并发仍有 `14238` 个 5xx，P1 仍失败。 |
| 33 | notification polling no-tx 定向与完整后端门禁 | 通过 | `product-stress-test-evidence/commands/95-server-notification-polling-no-tx-targeted-tests-20260611.log`；通知/Redis 相关 `10` 个测试通过。`product-stress-test-evidence/commands/96-server-mvn-test-after-notification-polling-no-tx-fix-20260611.log`；后端 `370` 个测试通过。 |
| 34 | notification polling no-tx 文档门禁 | 通过 | `product-stress-test-evidence/commands/97-docs-build-after-notification-polling-no-tx-fix-20260611.log`；docs build 通过，保留既有 chunk size warning。 |
| 35 | 2026-06-12 P1 事务边界诊断脚本单测 | 通过 | `/opt/miniconda3/bin/python3 ops/perf/run_perf_suite_test.py`；7 个 Python 测试通过。新增 `MAX_STAGE_CONCURRENCY` / `MAX_STAGE_COUNT`，默认合同计划不变。 |
| 36 | 作业/提交/成绩册高频入口事务边界定向测试 | 通过 | `bash ./mvnw -Dtest=AssignmentApplicationServiceTests,SubmissionApplicationServiceTests,GradebookApplicationServiceTests,GradebookQueryRepositoryTests test`；10 个 Java 测试通过，固定作业列表、提交列表、成绩册读入口不再声明外层 `@Transactional`。 |
| 37 | 第九批修复后 read ladder 50/200 短诊断 | 通过 | `raw/STRESS-06120105-read-after-hikaritimeout/read_after_hikaritimeout_results.json`；50 并发 65192 请求全 200，P99 48.70ms；200 并发 133697 请求全 200，P99 2418.45ms，5xx=0。服务日志未出现 Hikari/事务错误。 |
| 38 | 第九批修复后 judge/notification 50/200 短诊断 | 通过 | `raw/STRESS-06120111-judge-notif-after-hikaritimeout/judge_notif_after_hikaritimeout_results.json`；judge 50/200 均 5xx=0，P99 14.88ms / 85.46ms；notification 50/200 均 5xx=0，P99 18.63ms / 23.28ms。服务日志未出现 Hikari/事务错误。 |
| 39 | 第十批 runner 与成绩册热点修复目标单测 | 通过 | `bash ./mvnw -Dtest=GradebookApplicationServiceTests,RedisCacheServiceTests,GradingApplicationServiceTests test`；13 个 Java 测试通过。`/opt/miniconda3/bin/python3 -m unittest ops/perf/run_perf_suite_test.py`；9 个 Python 测试通过。 |
| 40 | 第十一批我的提交缓存与提交限流目标测试 | 通过 | `bash ./mvnw -Dtest=SubmissionApplicationServiceTests,RedisProtectedEndpointRateLimitIntegrationTests test`；8 个测试通过。 |
| 41 | 第十一批 read/write 失败场景复测 | 通过 | `raw/STRESS-0612022949/cache-fix-targeted/perf_results_cache_fix_targeted.json`；read ladder 50/200/500/1000 均 0 错误、5xx=0；write path 10/30/50/100 均 0 错误、5xx=0、429=0。 |
| 42 | 第十一批 10 分钟 smoke soak 复测 | 通过 | `raw/STRESS-0612022949/cache-fix-soak/perf_results_cache_fix_soak.json`；100 并发 10 分钟，384751 请求，P95 20.36ms，错误率 0，5xx=0。 |
| 43 | 第十一批修复后健康检查与敏感信息扫描 | 通过 | `commands/STRESS-0612022949/16-healthcheck-after-soak.log` 通过；`commands/STRESS-0612022949/17-sensitive-token-scan.log` 记录本轮 STRESS-0612022949 命令和 raw 证据目录无敏感 token 命中。 |

## 4.1 2026-06-11 第一批修复记录

- 认证读路径：保持 access token 紧凑合同，不把权限码和 group binding 快照写入 JWT；新增按 `sessionId + userId + permissionVersion` 缓存的服务端认证 principal 快照，减少高频请求重复读取权限/组织绑定。
- 判题轮询读路径：学生读取本人判题报告时新增授权后 owner/report 缓存，降低高频轮询对判题、提交、作业和授权查询链路的压力。
- 通知轮询读路径：默认通知列表 `page=1&pageSize=20` 增加短 TTL 缓存；已读、全部已读和通知 fanout 会同时清理未读数与默认列表缓存。
- 写入压测脚本：`write_path` 提交流量按学生账号分摊，避免 10 并发压测集中命中同一学生账号而把账号级限流误判为业务写入容量。
- 当前限制：上述修复只证明代码门禁通过；仍需复跑合同压测、补 K8s runtime/WebSocket 真实证据、补 Playwright MCP 前后页面回归，才能把失败项改为通过。

## 4.2 2026-06-11 P1 诊断与第二批修复记录

- P1 诊断复测：`STRESS-06111800-diagnose` 只跑读请求、判题轮询、通知轮询。相较首次合同压测，通知轮询 500 并发由错误率 7.44%、5xx 5282 改善到错误率 0、5xx 1；判题轮询 500 并发由错误率 14.8%、5xx 7133 改善到错误率 3.77%、5xx 2905；读请求 500 并发仍失败，错误率 22.54%、5xx 8284。
- 端点级诊断：为 `run_perf_suite.py` 增加 `endpointStats`，按稳定标签记录每个端点的请求数、延迟、错误率、5xx 和状态码分布。红绿测试见 `server/ops/perf/run_perf_suite_test.py`。
- read-label 诊断：`STRESS-06111820-readlabels` 显示混合读 500 并发错误分布在所有标签，Hikari 等待峰值 274；`teacher_assignment_submissions` 是最重端点，500 并发 P95 2725.51ms、P99 3066.44ms。
- 第二批代码修复：提交列表页改为批量加载答案和分数摘要，避免每页每条提交重复查询答案和题目快照。新增 `SubmissionAnswerApplicationService.loadAnswerReadBundles(...)` 单测，并用 `SubmissionIntegrationTests` 覆盖提交主链路。
- 修复后 read-label：`STRESS-06111832-readlabels-bulkfix` 中 50 并发 RPS 449.27 -> 492.72、P95 97.13ms -> 55.06ms；200 并发 RPS 517.85 -> 602.28、错误率 0.61% -> 0.25%、5xx 155 -> 61；500 并发 RPS 671.26 -> 734.96、错误率 22.51% -> 19.84%、5xx 8421 -> 7971。P1 仍失败。

## 4.3 2026-06-11 第三批认证快照修复记录

- 代码修复：签发 access token 时预热 `authPrincipal` 缓存，并把 principal TTL 从 `authSessionActiveTtl=30s` 拆为 `authPrincipalTtl=5m`；`/api/v1/auth/me` 默认返回认证阶段的会话快照，只有 `Cache-Control: no-cache` 时强制读取最新用户资料。
- 定向验证：新增 `authMeShouldUseSessionSnapshotByDefaultAndRefreshWhenNoCacheRequested` 和 `warmPrincipalForAccessTokenShouldSeedAccessTokenCacheWithoutReloadingPrincipal`，保留会话撤销、logout 后 access token 失效、显式 no-cache 刷新用户资料的安全语义。
- 修复后 read-label：`STRESS-06111855-authcache` 中 50 并发 RPS 492.72 -> 499.71、P95 55.06ms -> 53.89ms；200 并发 RPS 602.28 -> 632.14、P95 506.48ms -> 480.59ms、错误率 0.25% -> 0.19%、5xx 61 -> 47；500 并发 RPS 734.96 -> 771.55、错误率 19.84% -> 19.55%、5xx 7971 -> 7139。`auth_me` 200/500 并发 5xx 均降为 0，但 P1 仍失败。

## 4.4 2026-06-11 第四批会话活跃缓存与 runner 修复记录

- 代码修复：`authSessionActiveTtl` 默认值从 `30s` 提升到 `5m`，签发 access token 时预热 `authSessionActive` 缓存；logout、refresh token 撤销、用户全会话失效仍保留显式驱逐。
- runner 修复：`run_perf_suite.py` 在资源采样线程启动前创建 `ARTIFACT_DIR`，避免 read-label 复测结束写入 `resource_samples.json` 时因目录不存在崩溃。
- 定向验证：新增 `AuthSessionApplicationServiceTests.createSessionShouldWarmAccessTokenSessionActiveCache` 和 `run_perf_suite_test.py` artifact 目录创建单测；保留认证集成测试、会话撤销、logout 后 access token 失效、认证 principal 缓存测试。
- 修复后 read-label：`STRESS-06111935-sessionactive` 中 50 并发 RPS 499.71 -> 515.46、P95 53.89ms -> 50.41ms；200 并发 P95 480.59ms -> 487.35ms、5xx 47 -> 60、P99 2454.08ms -> 2460.62ms；500 并发错误率 19.55% -> 18.82%、5xx 7139 -> 7040。P1 仍失败。
- 栈与端点分布：复测采样窗口未再出现 `isAccessTokenActive` 读库栈；剩余 5xx 集中在 `SubmissionApplicationService`、`GradebookApplicationService` 相关业务读路径，500 并发最重标签为 `teacher_gradebook`、`teacher_assignments`、`teacher_assignment_submissions` 和 `my_submissions`。

## 4.5 2026-06-11 第五批教师提交列表敏感 scope 修复记录

- 代码修复：`SubmissionApplicationService.listTeacherSubmissions` 在页数据查出后只解析一次 `submission.read_source` 教学 scope，并用已有 `SubmissionEntity.offeringId/teachingClassId` 本地判定每行是否展示敏感内容，避免每条提交再次走 `canReadSensitiveSubmission` 单资源授权和资源归属查询。
- 语义边界：单条教师提交查看和教师附件下载仍保留原有 `canReadSensitiveSubmission` 单资源授权；本批只优化列表页映射。
- 定向验证：新增 `SubmissionApplicationServiceTests.teacherSubmissionListUsesResolvedSensitiveScopeWithoutPerRowAuthorization`，覆盖教师提交列表不再逐条调用敏感提交授权，同时保留 `PermissionAuthorizationServiceTests` 核心授权语义。
- 修复后 read-label：`STRESS-06112012-submissionauth` 中 50 并发 RPS 515.46 -> 569.21、P95 50.41ms -> 22.31ms；200 并发 RPS 628.03 -> 823.02、P95 487.35ms -> 296.96ms、5xx 60 -> 9；500 并发 RPS 765.37 -> 922.90、错误率 18.82% -> 13.09%、5xx 7040 -> 5830。P1 仍失败。
- 新根因观察：本次 8 分钟阶梯在 500 并发阶段重新出现 `AuthSessionApplicationService.isAccessTokenActive` 栈，`server-log-window-summary.log` 记录 `authSessionActiveStack=15117`，说明第四批 `5m` 会话活跃缓存 TTL 不能覆盖完整阶梯/soak 时长；下一批应优先延长或按 token 过期时间对齐该缓存，同时继续治理 `teacher_gradebook`、`my_submissions`、`teacher_assignment_submissions` 等业务读端点。

## 4.6 2026-06-11 第六批会话活跃缓存入口无事务修复记录

- TTL-only 验证：先将 `authSessionActiveTtl` 默认值从 `5m` 提升到 `2h`，与当前本地 access token 默认有效期对齐。但 `STRESS-06112041-authactivettl` 显示 500 并发仍有错误率 `14.67%`、5xx `6026`，日志窗口 `connectionTimeout=24714`、`authSessionActiveStack=17788`，说明 `@Transactional(readOnly = true)` 会在 cache lookup 前打开 JDBC 事务，缓存命中也会占用连接。
- 代码修复：移除 `AuthSessionApplicationService.isAccessTokenActive(...)` 上的 `@Transactional(readOnly = true)`，让 access token 会话活跃缓存入口在命中时不再预先打开事务；保留缓存 miss 时通过 repository 读取会话状态的原有语义。
- 定向验证：`AuthSessionApplicationServiceTests.createSessionShouldWarmAccessTokenSessionActiveCache` 更新为 2h TTL 断言；新增 `accessTokenActiveCacheEntryPointShouldNotOpenTransactionBeforeCacheLookup`，防止入口方法重新加事务。认证/session/Redis 相关 `23` 个测试通过，完整后端 `368` 个测试通过。
- 修复后 read-label：`STRESS-06112051-authnotx` 中 50 并发 RPS `564.97`、P95 `23.85ms`、5xx `0`；200 并发 RPS `823.20`、P95 `296.02ms`、P99 `2352.53ms`、5xx `9`；500 并发 RPS `881.72`、P95 `2418.54ms`、错误率 `8.04%`、5xx `5114`。相较第五批，500 并发错误率 `13.09% -> 8.04%`、5xx `5830 -> 5114`，但 P1 仍失败。
- 新根因观察：`raw/STRESS-06112051-authnotx/server-log-window-summary.log` 记录 `authSessionActiveStack=0`，证明本批 no-tx 修复有效；同一窗口仍有 `authenticatedPrincipalLoaderStack=7780`、`gradebookStack=4245`、`submissionServiceStack=1389`、`assignmentServiceStack=1277`，以及 `connectionTimeout=12903`。下一批应继续治理认证 principal loader 缓存/事务入口，并削减成绩册、提交、作业业务读路径连接占用。

## 4.7 2026-06-11 第七批认证 principal 缓存入口无事务修复记录

- 代码修复：移除 `AuthenticatedPrincipalLoader.loadPrincipalForAccessToken(...)` 上的 `@Transactional(readOnly = true)`，让 `authPrincipal` 缓存命中时不再预先打开 JDBC 事务；缓存缺失或无 session/version 时仍回退到已有 `loadPrincipal(...)` 事务读库路径。
- 定向验证：新增 `accessTokenPrincipalCacheEntryPointShouldNotOpenTransactionBeforeCacheLookup`，防止入口方法重新加事务。认证 principal/session/Redis 相关 `34` 个测试通过，完整后端 `369` 个测试通过。
- 修复后 read-label：`STRESS-06112118-principalnotx` 中 50 并发 RPS `558.34`、P95 `28.31ms`、5xx `0`；200 并发 RPS `842.79`、P95 `252.73ms`、P99 `2333.60ms`、5xx `11`；500 并发 RPS `894.27`、P95 `2405.31ms`、错误率 `6.67%`、5xx `10791`。相较第六批，500 并发总错误率 `8.04% -> 6.67%`，但 5xx `5114 -> 10791`，因此 P1 仍失败。
- 新根因观察：`raw/STRESS-06112118-principalnotx/server-log-window-summary.log` 记录 `authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=0`，证明认证缓存入口 no-tx 修复有效；同一窗口仍有 `connectionTimeout=10802`、`gradebookStack=2843`、`submissionServiceStack=2797`、`assignmentServiceStack=2725`、`notificationServiceStack=1302`，Redis 错误计数为 0。下一批应转向成绩册、提交列表、作业列表和通知未读数业务读入口。

## 4.8 2026-06-11 第八批通知轮询缓存入口无事务修复记录

- 代码修复：移除 `NotificationApplicationService.listMyNotifications(...)` 与 `getUnreadCount(...)` 上的 `@Transactional(readOnly = true)`，让默认通知列表缓存和未读数缓存命中时不再预先打开 JDBC 事务；`markRead(...)`、`markAllRead(...)` 等写路径仍保留事务和缓存驱逐语义。
- 定向验证：新增 `pollingCacheEntryPointsShouldNotOpenTransactionBeforeCacheLookup`，防止通知轮询缓存入口重新加事务。通知/Redis 相关 `10` 个测试通过，完整后端 `370` 个测试通过。
- 修复后 read-label：`STRESS-06112149-notifnotx` 中 50 并发 RPS `560.07`、P95 `27.74ms`、5xx `0`；200 并发 RPS `844.62`、P95 `251.74ms`、P99 `2347.58ms`、5xx `8`；500 并发 RPS `933.56`、P95 `2421.80ms`、错误率 `8.38%`、5xx `14238`。通知未读数端点 500 并发 P95 `142.06ms`、5xx `13`，相较第七批 500 并发通知未读数 5xx `1302 -> 13`；但混合读总 5xx `10791 -> 14238`，P1 仍失败。
- 新根因观察：`raw/STRESS-06112149-notifnotx/server-log-window-summary.log` 记录 `authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=0`、`notificationServiceStack=26`，证明通知缓存入口事务热点基本解除；同一窗口仍有 `connectionTimeout=14246`、`gradebookStack=4146`、`submissionServiceStack=4219`、`assignmentServiceStack=4032`，Redis 错误计数为 0。下一批应转向成绩册、提交列表、作业列表和课程列表业务读路径。

## 4.9 2026-06-12 第九批业务读入口事务边界与 Hikari 等待阈值修复记录

- 诊断脚本修复：`run_perf_suite.py` 新增 `MAX_STAGE_CONCURRENCY` 和 `MAX_STAGE_COUNT`，用于只跑 50/200 这类短诊断阶段；默认 `PERF_PROFILE=contract` 全量计划保持不变。`run_perf_suite_test.py` 从 5 个用例扩展到 7 个用例并通过。
- 代码修复：移除 `AssignmentApplicationService.listTeacherAssignments(...)`、`listMyAssignments(...)`，`SubmissionApplicationService.listMySubmissions(...)`、`listTeacherSubmissions(...)`，以及 `GradebookApplicationService.getOfferingGradebook(...)`、`getMyGradebook(...)` 的外层 `@Transactional(readOnly = true)`，避免高频读请求把授权、count/page 查询和视图装配包在同一个长事务里。新增反射测试防止这些入口重新加事务。
- 连接等待阈值：将默认 `AUBB_DB_CONNECTION_TIMEOUT_MS` 从 `500` 调整为 `2500`。依据是第九批短诊断中普通 Mapper 读已经不再长时间持有事务，但 200 并发仍会因短事务排队在 500ms 内偶发取不到连接；调整后 200 并发 P99 仍低于 3s，且 5xx 清零。
- 修复前后对比：`STRESS-06120049-read-after-assignmenttx` 证明作业列表外层事务移除后 50 并发 67845 请求 0 个 5xx，但 200 并发仍有 131 个 5xx；`STRESS-06120058-read-after-submission-gradebooktx` 在提交/成绩册事务边界修复后，200 并发 5xx 降为 79；`STRESS-06120105-read-after-hikaritimeout` 在 Hikari 等待阈值修复后，200 并发 133697 请求全 200、5xx=0。
- P1 短诊断结果：`STRESS-06120105-read-after-hikaritimeout` 读请求 50/200 均通过；`STRESS-06120111-judge-notif-after-hikaritimeout` 判题轮询和通知轮询 50/200 均通过。所有本轮最终服务日志均未出现 `CannotCreateTransactionException`、`Connection is not available` 或 `SQLTransientConnectionException`。
- 当前限制：本批只证明 P1 50/200 短诊断恢复；尚未复跑 read ladder 500/1000、判题/通知 500、完整 `PERF_PROFILE=contract`、soak、写入 429、Kubernetes Web 终端和 7.2-7.15 专项，因此总体验收仍不是通过。

## 4.10 2026-06-12 第十批 runner stage 超时与成绩册页缓存修复计划

- 修复计划文档：详见 `product-stress-test-repair-plan.md`。
- 新增证据：`STRESS-06120151-read500-after-stage-timeout` 中 read ladder 500 阶段总请求 `142801`、5xx=`1`，唯一 500 落在 `teacher_gradebook`；服务日志显示 `GradebookQueryRepository.loadAssignmentBackedRows` 等待 Hikari 连接超时，`total=48, active=48, idle=0, waiting=257`。
- runner 修复：为 `run_perf_suite.py` 增加 `PERF_REQUEST_TIMEOUT_SECONDS`、`PERF_STAGE_TIMEOUT_GRACE_SECONDS`、stage 级 `asyncio.wait_for`、挂起 worker 取消和 `EXC:StageTimeout` 统计；`summarize_result` 使用 `flush=True`，避免长阶段结束前无输出。
- 成绩册修复：教师成绩册页和学生我的成绩册增加 `gradebook-page-ttl` 短 TTL 缓存；整课、班级、学生我的成绩册入口均不声明外层只读事务；`CacheService` 增加 `evictByPrefix`，Redis 用 SCAN 删除同一开课前缀；成绩发布和人工批改事务提交后清理 `teacherGradebookPage` 与 `myGradebook`。
- 目标验证：`GradebookApplicationServiceTests`、`RedisCacheServiceTests`、`GradingApplicationServiceTests` 共 13 个 Java 测试通过；`run_perf_suite_test.py` 共 9 个 Python 测试通过。
- 当前限制：本批尚未执行修复后 500/1000 压力阶梯，不能把 P1-STRESS-001/P1-STRESS-002 改为通过；完整合同仍需复测。

## 4.11 2026-06-12 第十一批我的提交缓存与提交限流修复记录

- 新增证据：`STRESS-0612022949/contract-run` 完整合同复测中，read ladder 500/1000 各有 1 个 5xx；服务日志定位到 `SubmissionApplicationService.requireAssignment -> AssignmentMapper.selectById` 等待 Hikari 连接超时。write path 30/50 并发出现 429，来源是 `submission-create` 默认 10/min 限流低于合同流量。
- 代码修复：`SubmissionApplicationService.listMySubmissions(...)` 增加 `mySubmissionAssignment` 与 `mySubmissionPage` 短 TTL 缓存，TTL 默认为 `PT5S`；缓存 key 包含 assignment/user/page/pageSize，提交成功后按 assignment+user 前缀清理我的提交页缓存。提交创建、附件上传等写路径仍走实时 DB 校验，不使用缓存判断状态或开放时间。
- 限流修复：`submission-create` 默认限流从 10/min 调整为 60/min，保留 `AUBB_REDIS_RATE_LIMIT_SUBMISSION_CREATE_LIMIT` 环境变量覆盖能力；集成测试继续用 1/min 覆写验证 429 语义。
- 目标验证：`SubmissionApplicationServiceTests` 与 `RedisProtectedEndpointRateLimitIntegrationTests` 共 8 个测试通过；`STRESS-0612022949/cache-fix-targeted` 中 read ladder 50/200/500/1000 均 0 错误、5xx=0，write path 10/30/50/100 均 0 错误、5xx=0、429=0；`cache-fix-soak` 100 并发 10 分钟 384751 请求，错误率 0，5xx=0。
- 当前限制：核心 5xx/429 缺陷已关闭；但 500/1000 读请求 P95/P99 仍超过 `goal-stress.md` 严格阈值，且真实 Kubernetes Web 终端、SSE 100/300、真实 go-judge 五类结果和多个专项仍未执行。

## 5. 压测数据准备

- 数据前缀：正式压测数据集为 `STRESS-0611132804`。后端会把 username 归一化为小写，manifest 中学生账号显示为 `stress-0611132804-*`。
- 数据准备工具：`server/ops/perf/setup_perf_data.py`。本轮为满足合同场景，在 `server/ops/perf/` 内最小修复/扩展脚本：修复 username 归一化导致的学生查询缺失，增加导入失败检查，补充课程资源、fake runtime 终端实验和更高写入上限。
- 产物目录：`docs/06-testing-and-ops/artifacts/product-stress-test-evidence/raw/`
- manifest：脱敏版 `product-stress-test-evidence/raw/STRESS-0611132804/manifest.sanitized.json`；私有明文 manifest 仅保存在 `/tmp/aubb-STRESS-0611132804/manifest.json` 供本机 runner 使用，不提交。
- 凭据记录规则：命令日志和脱敏 manifest 中所有 `password` 字段均替换为 `[REDACTED]`。
- 数据规模：80 名学生、1 个教师、1 个开课、2 个教学班、客观题/写入题/编程题、1 个课程资源、1 个 fake runtime 终端实验。
- 数据准备证据：失败首轮 `product-stress-test-evidence/commands/10-setup-perf-data.log`；修复红绿测试 `11-setup-perf-data-test-red.log`、`12-setup-perf-data-test-green.log`；正式数据准备 `17-setup-perf-data-contract.log`。
- 完成审计补充：压测脚本单测在 `/opt/miniconda3/bin/python3` 下通过，证据为 `product-stress-test-evidence/commands/28-perf-script-tests-conda-completion-audit.log`。审计时默认 Homebrew Python 3.14 因本机未安装 `requests`/`aiohttp` 且受 PEP 668 管理，留下失败依赖检查日志 `25-perf-script-tests-completion-audit.log`、`29-python314-install-perf-deps.log`；该失败不改变正式压测结果和 runner 代码验证结论。
- 最新复测数据集：`STRESS-0612022949`，80 名学生、1 个教师、1 个开课、客观题/写入题/编程题、课程资源和 fake runtime 终端实验。脱敏 manifest：`product-stress-test-evidence/raw/STRESS-0612022949/manifest.sanitized.json`；私有明文 manifest 仅保存在 `/tmp/aubb-STRESS-0612022949/manifest.json`，不提交。

## 6. 场景结果总览

完整覆盖矩阵见 `product-stress-test-coverage-matrix.md`，7.1-7.15 场景矩阵见 `product-stress-test-scenario-matrix.md`。本节只保留已执行压测结果摘要；未执行但必测的专项在矩阵中标为 `阻塞`，不再隐含为通过。

| 场景 | 并发 | 持续时间 | RPS/TPS | P95 | P99 | 错误率 | 5xx | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 读请求阶梯复测 | 50/200/500/1000 | 2/3/3/3 分钟 | 591.95 / 1064.45 / 1073.78 / 1127.97 | 18.31 / 224.38 / 2346.07 / 2713.40 ms | 34.57 / 2283.08 / 2777.94 / 3160.52 ms | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 失败 | `raw/STRESS-0612022949/cache-fix-targeted/perf_results_cache_fix_targeted.json`；5xx 已清零，但 500/1000 长尾超过严格阈值。 |
| 写入链路复测 | 10/30/50/100 | 1/2/2/2 分钟 | 29.45 / 93.70 / 163.45 / 313.19 | 47.90 / 47.18 / 47.87 / 73.47 ms | 2223.22 / 63.04 / 67.07 / 137.34 ms | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 通过 | `raw/STRESS-0612022949/cache-fix-targeted/perf_results_cache_fix_targeted.json`；429=0。 |
| 判题与轮询 | 50/200/500 | 2/3/3 分钟 | 632.27 / 1667.85 / 1699.59 | 7.85 / 59.59 / 488.34 ms | 14.92 / 86.23 / 2485.08 ms | 0 / 0 / 0 | 0 / 0 / 0 | 失败 | `raw/STRESS-0612022949/contract-run/perf_results_contract.json`；轮询通过，但真实提交 5/10/20、五类结果、报告下载和重评未完成。 |
| 文件上传下载压测 | 上传 5/10；下载 20/100 | 上传各 1 分钟；下载各 2 分钟 | 上传 16.86/31.93；下载 221.27/729.38 | 上传 17.53/21.53 ms；下载 19.16/68.41 ms | 上传 24.43/30.34 ms；下载 24.00/106.99 ms | 0 | 0 | 阻塞 | `raw/STRESS-0612022949/contract-run/perf_results_contract.json`；教师课程资源子集通过，但缺少全部文件类型、20MiB 文件和 SHA256 记录。 |
| 通知轮询 / SSE 子集 | 轮询 50/200/500；SSE 20 | 2/3/3 分钟；SSE 1 分钟 | 592.43 / 2518.92 / 3580.69；SSE 27.24 | 12.11 / 9.83 / 71.38 ms；SSE 17.44 ms | 17.79 / 21.94 / 109.31 ms；SSE 29.29 ms | 0 | 0 | 阻塞 | `raw/STRESS-0612022949/contract-run/perf_results_contract.json`；通知轮询通过，SSE 100/300 未执行。 |
| 实验运行时专项 | 10 | 1 分钟 | 50.46 | 39.01 ms | 46.52 ms | 0 | 0 | 阻塞 | fake runtime 子集通过；真实 Kubernetes runtime、WebSocket 命令 I/O、重连和清理未执行。 |
| Soak 稳定性复测 | 100 | 10 分钟 | 640.96 | 20.36 ms | 54.17 ms | 0 | 0 | 阻塞 | `raw/STRESS-0612022949/cache-fix-soak/perf_results_cache_fix_soak.json`；10 分钟 smoke soak 通过，完整 30 分钟和 Kubernetes/WebSocket 混合未执行。 |

## 7. 资源采样与瓶颈分析

资源原始样本见 `product-stress-test-evidence/raw/STRESS-0611132804/contract-run/resource_samples.json`，摘要见 `product-stress-test-evidence/resources/resource-summary-STRESS-0611132804.md`。

- 样本数：358。
- PostgreSQL 活跃连接峰值：49。
- 容器峰值：PostgreSQL CPU 102.66%、内存 706.9 MiB；RabbitMQ CPU 67.8%、内存 215.0 MiB；MinIO CPU 14.48%、内存 311.7 MiB；Redis CPU 8.21%、内存 10.42 MiB；go-judge CPU 2.03%、内存 20.11 MiB。
- 主要瓶颈：后端日志显示高并发失败期间 Hikari 连接池耗尽，`total=48, active=48, idle=0, waiting=...`，导致 `CannotCreateTransactionException` 和 500。证据：`raw/STRESS-0611132804/server-log-stress-errors-excerpt.log`。
- 复测资源：`STRESS-06111800-diagnose` PostgreSQL 连接采样峰值 49、平均 48.30；`STRESS-06111820-readlabels`、`STRESS-06111832-readlabels-bulkfix`、`STRESS-06111855-authcache` 均记录 Hikari 等待峰值 274；第四批 `STRESS-06111935-sessionactive` PostgreSQL 连接采样 min/max/avg 均为 49，Hikari 等待峰值 275，Redis 错误计数为 0；第五批 `STRESS-06112012-submissionauth` PostgreSQL 连接 min/max/avg 为 14/49/45.36，日志窗口中 `connectionTimeout=21953`、`authSessionActiveStack=15117`；第六批 TTL-only `STRESS-06112041-authactivettl` PostgreSQL 连接 min/max/avg 为 14/49/45.99，日志窗口 `authSessionActiveStack=17788`；第六批 no-tx `STRESS-06112051-authnotx` PostgreSQL 连接 min/max/avg 为 13/49/45.10，日志窗口 `authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=7780`、`gradebookStack=4245`、`submissionServiceStack=1389`、`assignmentServiceStack=1277`；第七批 no-tx `STRESS-06112118-principalnotx` PostgreSQL 连接 min/max/avg 为 13/49/44.64，日志窗口 `authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=0`、`gradebookStack=2843`、`submissionServiceStack=2797`、`assignmentServiceStack=2725`、`notificationServiceStack=1302`；第八批 no-tx `STRESS-06112149-notifnotx` PostgreSQL 连接 min/max/avg 为 13/49/44.49，日志窗口 `authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=0`、`notificationServiceStack=26`、`gradebookStack=4146`、`submissionServiceStack=4219`、`assignmentServiceStack=4032`，Redis 错误计数为 0。证据：`raw/STRESS-06111800-diagnose/resource-summary.json`、`raw/STRESS-06111820-readlabels/server-log-window-summary.log`、`raw/STRESS-06111832-readlabels-bulkfix/server-log-window-summary.log`、`raw/STRESS-06111855-authcache/server-log-window-summary.log`、`raw/STRESS-06111935-sessionactive/resource-summary.json`、`raw/STRESS-06111935-sessionactive/server-log-window-summary.log`、`raw/STRESS-06112012-submissionauth/resource-summary.json`、`raw/STRESS-06112012-submissionauth/server-log-window-summary.log`、`raw/STRESS-06112041-authactivettl/resource-summary.json`、`raw/STRESS-06112041-authactivettl/server-log-window-summary.log`、`raw/STRESS-06112051-authnotx/resource-summary.json`、`raw/STRESS-06112051-authnotx/server-log-window-summary.log`、`raw/STRESS-06112118-principalnotx/resource-summary.json`、`raw/STRESS-06112118-principalnotx/server-log-window-summary.log`、`raw/STRESS-06112149-notifnotx/resource-summary.json`、`raw/STRESS-06112149-notifnotx/server-log-window-summary.log`。
- 第九批资源与日志：`STRESS-06120105-read-after-hikaritimeout` 读请求 50/200 短诊断的服务日志未出现 `CannotCreateTransactionException`、`Connection is not available` 或 `SQLTransientConnectionException`；200 并发 P99 `2418.45ms`，5xx=0。`STRESS-06120111-judge-notif-after-hikaritimeout` 判题和通知 50/200 短诊断同样未出现 Hikari/事务错误，judge 200 P99 `85.46ms`，notification 200 P99 `23.28ms`。证据：`raw/STRESS-06120105-read-after-hikaritimeout/read_after_hikaritimeout_results.json`、`raw/STRESS-06120105-read-after-hikaritimeout/server.log`、`raw/STRESS-06120111-judge-notif-after-hikaritimeout/judge_notif_after_hikaritimeout_results.json`、`raw/STRESS-06120111-judge-notif-after-hikaritimeout/server.log`。
- 第十一批资源与日志：`STRESS-0612022949/cache-fix-targeted` PostgreSQL 连接 min/max/avg 为 14/49/46.49，PostgreSQL CPU max 87.56%；`STRESS-0612022949/cache-fix-soak` PostgreSQL 连接 min/max/avg 为 45/49/48.14，PostgreSQL CPU max 5.14%。修复后日志未出现 `CannotGetJdbcConnectionException`、`SQLTransientConnectionException`、`Connection is not available`、`RATE_LIMIT_EXCEEDED` 或 429。证据：`product-stress-test-evidence/resources/STRESS-0612022949/resource-summary-cache-fix.md`、`raw/STRESS-0612022949/cache-fix-targeted/resource_samples.json`、`raw/STRESS-0612022949/cache-fix-soak/resource_samples.json`。

## 8. Playwright MCP 压测前后页面回归

- 压测前页面基线：通过。Playwright MCP 已操作真实登录页并分别进入管理员、教师、学生核心页面，共保存 10 张截图；console warning/error 为 0，未观察到 5xx。证据见 `product-stress-test-evidence/raw/playwright-mcp-pre-stress-baseline.md`、`product-stress-test-evidence/raw/playwright-mcp-pre-stress-console.log`、`product-stress-test-evidence/raw/playwright-mcp-pre-stress-network.log`、`product-stress-test-screenshots/pre-*.png`。
- 压测后页面回归：通过。`just healthcheck-strict` 通过；Playwright MCP 再次打开登录页、管理员、教师、学生核心页面，共保存 10 张 `post-*.png` 截图；console warning/error 为 0，MCP 监听期间未观察到 5xx。证据见 `product-stress-test-evidence/commands/19-healthcheck-strict-post-stress.log`、`product-stress-test-evidence/raw/playwright-mcp-post-stress-baseline.md`、`product-stress-test-screenshots/post-*.png`。

## 9. 问题清单

详见 `product-stress-test-issue-list.md`。

## 10. 数据残留与清理建议

- `STRESS-0611131857`：首轮数据准备失败，已创建的学院/教师等部分对象可能残留；失败证据见 `10-setup-perf-data.log`。
- `STRESS-0611132135`：中间成功数据集，未用于正式合同压测，包含 80 名学生和课程/作业等对象。
- `STRESS-0611132804`：正式压测数据集，包含 80 名学生、课程/班级、作业、编程提交、课程资源、fake runtime 终端实验，以及压测过程中产生的提交、资源上传、实验会话和通知读请求记录。
- `STRESS-0612022949`：最新复测数据集，包含 80 名学生、课程/班级、作业、编程提交、课程资源、fake runtime 终端实验，以及第十一批 targeted/soak 复测产生的提交与读请求记录。
- 私有 manifest：`/tmp/aubb-STRESS-0611132804/manifest.json`，含本地临时压测账号密码，仅供本机复跑；不提交。
- 私有 manifest：`/tmp/aubb-STRESS-0612022949/manifest.json`，含本地临时压测账号密码，仅供本机复跑；不提交。
- 清理建议：以 `STRESS-0611131857`、`STRESS-0611132135`、`STRESS-0611132804`、`STRESS-0612022949` 前缀清理本地压测组织、账号、课程、作业、资源和实验数据；清理前保留当前 artifacts 作为证据。

## 11. 最终建议

最终建议：不通过全平台合同容量。第十一批已经把核心 runner 中的高并发 5xx 和写路径 429 修复，并用 targeted read/write 与 10 分钟 smoke soak 证明；但 500/1000 读请求长尾仍超过严格阈值，真实 Kubernetes Web 终端、SSE 100/300、真实 go-judge 五类结果/重评/报告下载、30 分钟完整 soak 和 7.2-7.15 多个专项仍未关闭。下一轮应优先治理读请求长尾和真实执行链路专项，而不是继续只看 5xx。
