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

- 结论：不通过合同容量目标。系统在低并发和若干专项链路可恢复可用，但高并发读请求、判题轮询、通知轮询触发 5xx，写入与 soak 出现 429，不能按本合同容量阈值直接对外交付。
- 2026-06-11 修复批次结论：已完成第一批 P1 高频读路径与压测脚本修复，并通过后端单测/集成门禁；但尚未复跑 `PERF_PROFILE=contract` 全量压力测试，故本报告总体验收结论仍保持“不通过”。
- 2026-06-11 P1 复测与第六批修复结论：已复跑读请求 / 判题轮询 / 通知轮询 P1 诊断和七轮 read-label 混合读诊断，证明认证 principal cache、提交列表批量答案加载、`/auth/me` 默认快照读取、access token 会话活跃缓存预热、教师提交列表敏感 scope 预解析、会话活跃缓存入口无事务均有收益；第六批 no-tx 复测 500 并发错误率从 13.09% 降到 8.04%、5xx 从 5830 降到 5114，但 200/500 并发仍有 5xx/P99 超阈值，P1 仍为失败。
- 已证明容量边界：读请求 50 并发 2 分钟通过；判题轮询 50 并发 2 分钟通过；文件上传 10 并发、文件下载 100 并发通过；通知查询 200 并发 3 分钟通过；SSE 20 并发 1 分钟通过；fake runtime 实验会话 10 并发 1 分钟通过。
- 未证明或失败范围：读请求 200/500 并发失败；写入链路 10 并发即出现 429；判题轮询 200/500 并发失败；通知查询 500 并发失败；soak 100 并发 10 分钟出现 429，未满足无错误稳定性要求；未证明 Kubernetes 实验运行时容量。
- 真实 go-judge 判题结论：失败。数据准备阶段触发了 1 次真实编程提交，判题轮询 50 并发通过，但 200/500 并发失败；未完成五类结果、报告下载和重评容量证明。
- Web 终端 / Kubernetes runtime 结论：阻塞。本轮只证明本地 fake runtime 10 并发 smoke，当前环境未配置真实 Kubernetes runtime，不能声明 Web 终端生产容量通过。
- 是否建议对外交付：不建议按当前合同容量目标交付；若必须演示或内测，应限定为低并发、明确限流，并先完成连接池/读路径优化与重测。
- 交付限制或建议：继续治理 JDBC 连接池耗尽；最新 8 分钟阶梯已确认 `isAccessTokenActive` 缓存入口不再打开事务，但 `AuthenticatedPrincipalLoader`、成绩册、提交和作业读路径仍会在高并发阶段耗尽连接池。下一批应继续削减认证 principal loader 与业务读端点连接占用。

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

## 5. 压测数据准备

- 数据前缀：正式压测数据集为 `STRESS-0611132804`。后端会把 username 归一化为小写，manifest 中学生账号显示为 `stress-0611132804-*`。
- 数据准备工具：`server/ops/perf/setup_perf_data.py`。本轮为满足合同场景，在 `server/ops/perf/` 内最小修复/扩展脚本：修复 username 归一化导致的学生查询缺失，增加导入失败检查，补充课程资源、fake runtime 终端实验和更高写入上限。
- 产物目录：`docs/06-testing-and-ops/artifacts/product-stress-test-evidence/raw/`
- manifest：脱敏版 `product-stress-test-evidence/raw/STRESS-0611132804/manifest.sanitized.json`；私有明文 manifest 仅保存在 `/tmp/aubb-STRESS-0611132804/manifest.json` 供本机 runner 使用，不提交。
- 凭据记录规则：命令日志和脱敏 manifest 中所有 `password` 字段均替换为 `[REDACTED]`。
- 数据规模：80 名学生、1 个教师、1 个开课、2 个教学班、客观题/写入题/编程题、1 个课程资源、1 个 fake runtime 终端实验。
- 数据准备证据：失败首轮 `product-stress-test-evidence/commands/10-setup-perf-data.log`；修复红绿测试 `11-setup-perf-data-test-red.log`、`12-setup-perf-data-test-green.log`；正式数据准备 `17-setup-perf-data-contract.log`。
- 完成审计补充：压测脚本单测在 `/opt/miniconda3/bin/python3` 下通过，证据为 `product-stress-test-evidence/commands/28-perf-script-tests-conda-completion-audit.log`。审计时默认 Homebrew Python 3.14 因本机未安装 `requests`/`aiohttp` 且受 PEP 668 管理，留下失败依赖检查日志 `25-perf-script-tests-completion-audit.log`、`29-python314-install-perf-deps.log`；该失败不改变正式压测结果和 runner 代码验证结论。

## 6. 场景结果总览

完整覆盖矩阵见 `product-stress-test-coverage-matrix.md`，7.1-7.15 场景矩阵见 `product-stress-test-scenario-matrix.md`。本节只保留已执行压测结果摘要；未执行但必测的专项在矩阵中标为 `阻塞`，不再隐含为通过。

| 场景 | 并发 | 持续时间 | RPS/TPS | P95 | P99 | 错误率 | 5xx | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 读请求阶梯压测 | 50/200/500 | 2/3/3 分钟 | 343.39 / 412.42 / 561.39 | 163.45 / 2358.92 / 2719.35 ms | 259.3 / 2658.49 / 3106.37 ms | 0 / 2.07% / 29.03% | 0 / 478 / 9514 | 失败 | `raw/STRESS-0611132804/contract-run/perf_results_contract.json`；50 并发通过，200 起失败。 |
| 读请求端点级复测 | 50/200/500 | 2/3/3 分钟 | 564.97 / 823.20 / 881.72 | 23.85 / 296.02 / 2418.54 ms | 39.24 / 2352.53 / 2781.20 ms | 0 / 0.02% / 8.04% | 0 / 9 / 5114 | 失败 | `raw/STRESS-06112051-authnotx/read-label-results.json`；第六批修复后 200 并发 P95 通过但仍有 5xx/P99 未达标，500 仍失败。 |
| 写入链路压测 | 10 | 1 分钟 | 29.63 TPS | 65.0 ms | 72.36 ms | 11.16% | 0 | 失败 | `perf_results_contract.json`；201=160，429=201。 |
| 判题与轮询压测 | 50/200/500 | 2/3/3 分钟 | 458.1 / 636.57 / 719.32 | 43.29 / 430.98 / 2525.36 ms | 56.5 / 2425.23 / 2886.32 ms | 0 / 0.07% / 14.8% | 0 / 26 / 7133 | 失败 | 50 并发通过，200 起出现 5xx。 |
| 文件上传下载压测 | 上传 5/10；下载 20/100 | 上传各 1 分钟；下载各 2 分钟 | 上传 16.21/31.32；下载 209.61/494.95 | 上传 20.56/28.41 ms；下载 25.07/132.02 ms | 上传 22.8/37.63 ms；下载 29.63/2272.05 ms | 0 | 0 | 阻塞 | `perf_results_contract.json`；教师课程资源子集通过，但缺少全部文件类型、20MiB 文件和 SHA256 记录。 |
| 通知与 SSE / 轮询专项 | 轮询 50/200/500；SSE 20 | 2/3/3 分钟；SSE 1 分钟 | 592.12 / 959.11 / 1036.95；SSE 28.17 | 14.85 / 219.73 / 2344.92 ms；SSE 39.35 ms | 26.25 / 2300.85 / 2692.38 ms；SSE 46.28 ms | 0 / 0 / 7.44%；SSE 0 | 0 / 0 / 5282；SSE 0 | 失败 | 50/200 轮询和 SSE 通过，500 轮询失败。 |
| 实验运行时专项 | 10 | 1 分钟 | 48.72 | 45.6 ms | 51.85 ms | 0 | 0 | 阻塞 | fake runtime：201=1520，200=1520；真实 Kubernetes runtime、WebSocket 命令 I/O、重连和清理未执行。 |
| Soak 稳定性测试 | 100 | 10 分钟 | 387.97 | 271.26 ms | 2281.26 ms | 1.31% | 0 | 失败 | 200=228798，201=1600，429=3069；服务压后健康检查和 MCP 页面回归通过。 |

## 7. 资源采样与瓶颈分析

资源原始样本见 `product-stress-test-evidence/raw/STRESS-0611132804/contract-run/resource_samples.json`，摘要见 `product-stress-test-evidence/resources/resource-summary-STRESS-0611132804.md`。

- 样本数：358。
- PostgreSQL 活跃连接峰值：49。
- 容器峰值：PostgreSQL CPU 102.66%、内存 706.9 MiB；RabbitMQ CPU 67.8%、内存 215.0 MiB；MinIO CPU 14.48%、内存 311.7 MiB；Redis CPU 8.21%、内存 10.42 MiB；go-judge CPU 2.03%、内存 20.11 MiB。
- 主要瓶颈：后端日志显示高并发失败期间 Hikari 连接池耗尽，`total=48, active=48, idle=0, waiting=...`，导致 `CannotCreateTransactionException` 和 500。证据：`raw/STRESS-0611132804/server-log-stress-errors-excerpt.log`。
- 复测资源：`STRESS-06111800-diagnose` PostgreSQL 连接采样峰值 49、平均 48.30；`STRESS-06111820-readlabels`、`STRESS-06111832-readlabels-bulkfix`、`STRESS-06111855-authcache` 均记录 Hikari 等待峰值 274；第四批 `STRESS-06111935-sessionactive` PostgreSQL 连接采样 min/max/avg 均为 49，Hikari 等待峰值 275，Redis 错误计数为 0；第五批 `STRESS-06112012-submissionauth` PostgreSQL 连接 min/max/avg 为 14/49/45.36，日志窗口中 `connectionTimeout=21953`、`authSessionActiveStack=15117`；第六批 TTL-only `STRESS-06112041-authactivettl` PostgreSQL 连接 min/max/avg 为 14/49/45.99，日志窗口 `authSessionActiveStack=17788`；第六批 no-tx `STRESS-06112051-authnotx` PostgreSQL 连接 min/max/avg 为 13/49/45.10，日志窗口 `authSessionActiveStack=0`、`authenticatedPrincipalLoaderStack=7780`、`gradebookStack=4245`、`submissionServiceStack=1389`、`assignmentServiceStack=1277`，Redis 错误计数为 0。证据：`raw/STRESS-06111800-diagnose/resource-summary.json`、`raw/STRESS-06111820-readlabels/server-log-window-summary.log`、`raw/STRESS-06111832-readlabels-bulkfix/server-log-window-summary.log`、`raw/STRESS-06111855-authcache/server-log-window-summary.log`、`raw/STRESS-06111935-sessionactive/resource-summary.json`、`raw/STRESS-06111935-sessionactive/server-log-window-summary.log`、`raw/STRESS-06112012-submissionauth/resource-summary.json`、`raw/STRESS-06112012-submissionauth/server-log-window-summary.log`、`raw/STRESS-06112041-authactivettl/resource-summary.json`、`raw/STRESS-06112041-authactivettl/server-log-window-summary.log`、`raw/STRESS-06112051-authnotx/resource-summary.json`、`raw/STRESS-06112051-authnotx/server-log-window-summary.log`。

## 8. Playwright MCP 压测前后页面回归

- 压测前页面基线：通过。Playwright MCP 已操作真实登录页并分别进入管理员、教师、学生核心页面，共保存 10 张截图；console warning/error 为 0，未观察到 5xx。证据见 `product-stress-test-evidence/raw/playwright-mcp-pre-stress-baseline.md`、`product-stress-test-evidence/raw/playwright-mcp-pre-stress-console.log`、`product-stress-test-evidence/raw/playwright-mcp-pre-stress-network.log`、`product-stress-test-screenshots/pre-*.png`。
- 压测后页面回归：通过。`just healthcheck-strict` 通过；Playwright MCP 再次打开登录页、管理员、教师、学生核心页面，共保存 10 张 `post-*.png` 截图；console warning/error 为 0，MCP 监听期间未观察到 5xx。证据见 `product-stress-test-evidence/commands/19-healthcheck-strict-post-stress.log`、`product-stress-test-evidence/raw/playwright-mcp-post-stress-baseline.md`、`product-stress-test-screenshots/post-*.png`。

## 9. 问题清单

详见 `product-stress-test-issue-list.md`。

## 10. 数据残留与清理建议

- `STRESS-0611131857`：首轮数据准备失败，已创建的学院/教师等部分对象可能残留；失败证据见 `10-setup-perf-data.log`。
- `STRESS-0611132135`：中间成功数据集，未用于正式合同压测，包含 80 名学生和课程/作业等对象。
- `STRESS-0611132804`：正式压测数据集，包含 80 名学生、课程/班级、作业、编程提交、课程资源、fake runtime 终端实验，以及压测过程中产生的提交、资源上传、实验会话和通知读请求记录。
- 私有 manifest：`/tmp/aubb-STRESS-0611132804/manifest.json`，含本地临时压测账号密码，仅供本机复跑；不提交。
- 清理建议：以 `STRESS-0611131857`、`STRESS-0611132135`、`STRESS-0611132804` 前缀清理本地压测组织、账号、课程、作业、资源和实验数据；清理前保留当前 artifacts 作为失败证据。

## 11. 最终建议

最终建议：不通过。当前系统可以支撑低并发演示和部分专项能力，但不满足交付前压力测试合同中读、写、判题、通知和 soak 的容量/错误率阈值。第六批修复证明会话活跃缓存入口事务是有效热点，`isAccessTokenActive` 已不再在缓存命中时占用连接；但最新 8 分钟阶梯仍显示认证 principal loader、`GradebookApplicationService`、提交/作业列表等读路径会耗尽连接池。下一轮应继续削减这些读路径的事务与查询占用，然后使用同一 runner 和场景矩阵复测。
