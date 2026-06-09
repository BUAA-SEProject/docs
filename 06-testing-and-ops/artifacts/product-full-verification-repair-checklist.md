# AUBB 产品全功能交付修复清单

## 1. 修复元信息

- 修复开始时间：2026-06-10 00:35 CST
- 修复阶段：第一阶段
- 依据报告：`docs/06-testing-and-ops/artifacts/product-full-verification-report.md`
- 依据功能清单：`docs/06-testing-and-ops/artifacts/product-full-verification-feature-inventory.md`
- 依据彩排记录：`docs/06-testing-and-ops/artifacts/product-full-verification-rehearsal-log.md`
- 初始 `just status` 摘要：`server/` clean；`web/` clean；`docs/` clean；`docs/` 分支 `main...origin/main [ahead 4]`；AUBB root 不是 git 仓库。
- 初始环境检查：`just healthcheck-strict` 通过，后端 `18080`、前端 `3000`、OpenAPI、登录页均可用。

## 2. 修复总览

| 编号 | 级别 | 角色 | 问题摘要 | 状态 | 回归证据 |
| --- | --- | --- | --- | --- | --- |
| E2E-GATE-001 | P1 | 学生/管理员/教师 | `just e2e-real` 辅助门禁失败 | 已回归 | 真实后端 E2E 定向 8 passed；完整 `just e2e-real` 50 passed |
| P1-002 | P1 | 学生 | 编程题自测和正式提交返回系统错误 | 已回归 | MCP WebIDE 自测与提交详情均显示通过 |
| P1-003 | P1 | 学生 | 实验 Web 终端连接和交互输出不稳定 | 已回归 | MCP 实验终端一次打开即连接且 echo 有独立输出 |
| P2-001 | P2 | 无登录用户 | 登录空表单缺少可见错误提示 | 未开始 | 待补充 |
| P2-005 | P2 | 教师 | 教师讨论列表长标题横向溢出 | 未开始 | 待补充 |
| P2-006 | P2 | 学生 | 简答提交详情顶部“无文本答案”与分题答案矛盾 | 未开始 | 待补充 |
| P2-007 | P2 | 开课助教 | 未授权开课页仍展示可执行入口 | 未开始 | 待补充 |
| P3-004 | P3 | 教师 | 成绩册导出按钮文案与实际文件格式不一致 | 未开始 | 待补充 |

## 3. P0 阻塞问题

第一轮报告未记录 P0 问题。

## 4. P1 高优先级问题

- [x] E2E-GATE-001 `just e2e-real` 辅助门禁失败（已回归）
- [x] P1-002 编程题自测和正式提交返回系统错误（已回归）
- [x] P1-003 实验 Web 终端连接和交互输出不稳定（已回归）

## 5. P2 体验问题

- [ ] P2-001 登录空表单缺少可见错误提示
- [ ] P2-005 教师讨论列表长标题横向溢出
- [ ] P2-006 简答提交详情顶部“无文本答案”与分题答案矛盾
- [ ] P2-007 未授权开课页仍展示可执行入口

## 6. P3 优化项

- [ ] P3-004 成绩册导出按钮文案与实际文件格式不一致

## 7. 每项修复记录

### E2E-GATE-001 `just e2e-real` 辅助门禁失败

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `E2E-GATE-001`
- 修复状态：已回归
- 修改文件：
  - `web/src/tests/e2e/assignment-submission.spec.ts`
  - `web/src/tests/e2e/full-organization-structure.spec.ts`
  - `web/src/tests/e2e/real-backend.ts`
  - `server/src/main/java/com/aubb/server/common/ratelimit/RedisRateLimitService.java`
  - `server/src/test/java/com/aubb/server/common/ratelimit/RedisRateLimitServiceTests.java`
- 修复说明：
  - 根因 1：学生作业 E2E 仍断言旧版主操作文案“开始做题”，而当前真实页面对已开始作业展示“继续作答 ${作业标题}”。
  - 根因 2：组织开课 E2E 直接点击“共同管理学院”，但 `MultiOptionPicker` 默认只展示前 6 个选项；历史 E2E 残留组织较多时目标学院需要先搜索。
  - 根因 3：教师登录 fixture 在快速真实 E2E 中可能触发 Redis 限流；Redis TTL 为 0 时服务端返回 `Retry-After: 0`，E2E 登录辅助逻辑也未对 `RATE_LIMIT_EXCEEDED` 提供兜底等待。
  - 学生作业 E2E 已改为按真实 `data-testid` 作业卡和“继续作答”链接定位；组织开课 E2E 已先搜索再选择多选项；登录辅助逻辑增加限流兜底重试；Redis 限流拒绝结果保证正数 `Retry-After`。
- Playwright MCP 回归：
  - 页面：不适用，E2E-GATE 是命令门禁问题；相关学生作业、组织开课、教师登录路径已由真实后端 Playwright E2E 回归。
  - 账号：真实 E2E fixture 账号。
  - 步骤：执行定向真实后端 Playwright E2E，再执行完整 `just e2e-real`。
  - 结果：定向 3 个失败相关 spec 共 8 passed；完整 `just e2e-real` 为 50 passed。
  - 截图：不适用；命令输出为本项主证据。
- 命令验证：
  - 命令：`cd web && set -a; source ../env/e2e.env; set +a; AUBB_E2E_REAL_BACKEND=1 ... npm run test:e2e -- src/tests/e2e/assignment-submission.spec.ts src/tests/e2e/full-organization-structure.spec.ts src/tests/e2e/teacher-course.spec.ts`
  - 结果：通过，`8 passed (32.2s)`。
  - 命令：`cd server && bash ./mvnw -Dtest=RedisRateLimitServiceTests test`
  - 结果：通过，`Tests run: 4, Failures: 0, Errors: 0, Skipped: 0`。
  - 命令：`cd web && npm test -- src/tests/unit/lab/lab-terminal.test.tsx src/tests/unit/submission/programming-workspace-page.test.tsx`
  - 结果：通过，`2 passed`、`14 tests passed`。
  - 命令：`just e2e-real`
  - 结果：通过，`50 passed (3.7m)`。
  - 命令：`just verify`
  - 结果：通过，后端 `357` tests passed，web lint/typecheck passed，docs build passed。
- Commit：按 `server/`、`web/`、`docs/` 子仓库分别提交；具体 hash 以 git 历史和最终回复为准。
- 剩余风险：E2E 辅助门禁已回归；全产品最终通过仍依赖第二阶段完整 MCP 验收和第三阶段三次演示彩排。

### P1-002 编程题自测和正式提交返回系统错误

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P1-002`
- 修复状态：已回归
- 修改文件：
  - `server/scripts/api-tests/permission/e2e_permission_realrun.py`
  - `server/scripts/api-tests/permission/e2e_permission_realrun_test.py`
  - `web/src/features/submission/hooks/use-programming-workspace-controller.ts`
  - `web/src/tests/unit/submission/programming-workspace-page.test.tsx`
- 修复说明：
  - 根因 1：演示编程题 fixture 仍使用旧版 `CUSTOM_SCRIPT` 协议，从 stdin 读取实际/期望输出并用进程退出码表达判定；当前后端要求自定义 checker 读取 `_aubb_actual_stdout.txt` / `_aubb_expected_stdout.txt` 并向 stdout 输出裁决 JSON。
  - 根因 2：WebIDE 自测默认未填入题目样例输入与期望输出，学生直接点击“运行自测”时示例代码会因 `input()` 无输入而产生 `EOFError`。
  - 后端 fixture 已改为当前 JSON 文件协议，并在刷新既有 `Question-A-Programming` 时同步更新题库题目与已发布作业题目快照中的 `customJudgeScript`。
  - 前端 WebIDE 已在题目加载后默认带入 `sampleStdinText` 和 `sampleExpectedStdout`，并在运行自测时使用题目样例作为兜底输入。
- Playwright MCP 回归：
  - 页面：`/student/assignments/7/workspace/11`、`/student/submissions/46?assignmentId=7`
  - 账号：学生 `U-ST1`
  - 步骤：登录学生端，打开 `Task-Programming-A1` 的 WebIDE，确认样例输入为 `1 2`、期望输出为 `3`，点击“运行自测”；随后“保存并返回”，在作业详情点击“提交答案”，刷新提交详情页。
  - 结果：WebIDE 自测显示 `ACCEPTED，样例输出与预期一致`；提交详情显示反馈 `ACCEPTED，2/2 个测试点通过，得分 100/100`，判题结果为“已完成 / 通过”。
  - 截图：`product-full-verification-screenshots/repair-p1-002-webide-sample-run-fixed.png`、`product-full-verification-screenshots/repair-p1-002-submission-accepted-fixed.png`
- 命令验证：
  - 命令：`cd server && python3 scripts/api-tests/permission/e2e_permission_realrun_test.py`
  - 结果：通过，`Ran 4 tests in ... OK`。
  - 命令：`just seed-fixtures`
  - 结果：通过，`fixtureCounts ... caseCount 22, passed 22, failed 0, status passed`，并刷新既有题目/作业题目快照。
  - 命令：`cd web && npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx`
  - 结果：通过，`11 tests passed`。
  - 命令：`docker exec -i server-postgres-1 psql ... where s.id = 46`
  - 结果：辅助查询显示 `submission_id=46`、`answer_id=129`、`job_id=34`，`job_status=SUCCEEDED`、`verdict=ACCEPTED`、`score=100`、`max_score=100`。
- Commit：按 `server/`、`web/`、`docs/` 子仓库分别提交；具体 hash 以 git 历史和最终回复为准。
- 剩余风险：当前已覆盖演示编程题、样例直跑、正式提交、`just e2e-real` 和 `just verify`；全产品最终通过仍依赖第二阶段完整 MCP 验收和第三阶段三次演示彩排。

### P1-003 实验 Web 终端连接和交互输出不稳定

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P1-003`
- 修复状态：已回归
- 修改文件：
  - `web/src/features/lab/components/lab-terminal.tsx`
  - `web/src/tests/unit/lab/lab-terminal.test.tsx`
  - `server/src/main/java/com/aubb/server/modules/lab/application/runtime/FakeLabRuntimeProvisioner.java`
  - `server/src/test/java/com/aubb/server/integration/LabTerminalIntegrationTests.java`
- 修复说明：
  - 根因 1：外层“打开终端”只挂载终端组件，内层组件还需要再次点击才实际获取 token 并打开 WebSocket，导致首次打开停留“未连接”。
  - 根因 2：`onIssueToken` callback identity 会随 token mutation 状态变化更新，自动连接 effect 若直接依赖该 callback 会触发重复取 token / WebSocket 重连。
  - 根因 3：fake runtime 只原样回显输入，没有按真实终端回车协议处理 `\r`，所以 `echo` 没有独立结果行。
  - 前端终端组件已在挂载后自动连接，每个 `sessionId` 只自动触发一次，连接中/已连接时防止重复连接，并在卸载时关闭 socket/释放 terminal。
  - fake runtime 已支持 `\r`、`\n`、`\r\n` 命令分隔，并对 `echo ...` 输出独立结果行，保持本地演示路径可解释。
- Playwright MCP 回归：
  - 页面：`/student/labs`
  - 账号：学生 `U-ST1`
  - 步骤：选择 `MCP 终端闭环复核 0608-1644`，确认会话 `运行中`，点击一次外层“打开终端”，等待 `已连接`，在 xterm 输入 `echo AUBB-MCP-TERMINAL` 并回车。
  - 结果：终端显示 `AUBB lab terminal ready.`、`resize accepted`、命令行 `echo AUBB-MCP-TERMINAL` 和独立输出行 `AUBB-MCP-TERMINAL`；`connection-token` 请求为单次，console 无 warning/error。
  - 截图：`product-full-verification-screenshots/repair-p1-003-lab-terminal-fixed.png`
- 命令验证：
  - 命令：`cd web && npm test -- src/tests/unit/lab/lab-terminal.test.tsx`
  - 结果：通过，`3 tests passed`。
  - 命令：`cd web && npm test -- src/tests/unit/lab/student-labs-page.test.tsx`
  - 结果：通过，`4 tests passed`。
  - 命令：`cd server && bash ./mvnw -Dtest=LabTerminalIntegrationTests#fakeTerminalWebSocketSendsWelcomeAndEchoesInput test`
  - 结果：通过，`Tests run: 1, Failures: 0, Errors: 0, Skipped: 0`。
  - 命令：`just healthcheck-strict`
  - 结果：通过，后端 readiness、OpenAPI、前端 login 均可用。
- Commit：按 `server/`、`web/`、`docs/` 子仓库分别提交；具体 hash 以 git 历史和最终回复为准。
- 剩余风险：当前回归覆盖 fake runtime 的演示实验、`just e2e-real` 和 `just verify`；Kubernetes exec runtime 的输入输出转发已有既有单测，第二阶段仍需在完整验收中覆盖实际运行时路径。

### P2-001 登录空表单缺少可见错误提示

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P2-001`
- 修复状态：未开始
- 修改文件：待补充
- 修复说明：低风险相邻问题，待 P1 修复后按时间处理。
- Playwright MCP 回归：
  - 页面：待补充
  - 账号：无登录用户
  - 步骤：待补充
  - 结果：待补充
  - 截图：待补充
- 命令验证：
  - 命令：待补充
  - 结果：待补充
- Commit：待补充
- 剩余风险：待补充

### P2-005 教师讨论列表长标题横向溢出

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P2-005`
- 修复状态：未开始
- 修改文件：待补充
- 修复说明：低风险相邻问题，待 P1 修复后按时间处理。
- Playwright MCP 回归：
  - 页面：待补充
  - 账号：待补充
  - 步骤：待补充
  - 结果：待补充
  - 截图：待补充
- 命令验证：
  - 命令：待补充
  - 结果：待补充
- Commit：待补充
- 剩余风险：待补充

### P2-006 简答提交详情顶部“无文本答案”与分题答案矛盾

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P2-006`
- 修复状态：未开始
- 修改文件：待补充
- 修复说明：低风险相邻问题，待 P1 修复后按时间处理。
- Playwright MCP 回归：
  - 页面：待补充
  - 账号：待补充
  - 步骤：待补充
  - 结果：待补充
  - 截图：待补充
- 命令验证：
  - 命令：待补充
  - 结果：待补充
- Commit：待补充
- 剩余风险：待补充

### P2-007 未授权开课页仍展示可执行入口

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P2-007`
- 修复状态：未开始
- 修改文件：待补充
- 修复说明：低风险相邻问题，待 P1 修复后按时间处理。
- Playwright MCP 回归：
  - 页面：待补充
  - 账号：待补充
  - 步骤：待补充
  - 结果：待补充
  - 截图：待补充
- 命令验证：
  - 命令：待补充
  - 结果：待补充
- Commit：待补充
- 剩余风险：待补充

### P3-004 成绩册导出按钮文案与实际文件格式不一致

- 报告链接或位置：`product-full-verification-report.md` 第 17 节 `P3-004`
- 修复状态：未开始
- 修改文件：待补充
- 修复说明：低风险文案问题，待 P1 修复后按时间处理。
- Playwright MCP 回归：
  - 页面：待补充
  - 账号：待补充
  - 步骤：待补充
  - 结果：待补充
  - 截图：待补充
- 命令验证：
  - 命令：待补充
  - 结果：待补充
- Commit：待补充
- 剩余风险：待补充
