---
title: "Agent 前端整理与全量测试入口（2026-06-05）"
section: "06-testing-and-ops"
status: current
---
# Agent 前端整理与全量测试入口（2026-06-05）

本文是后续 agent 接手 AUBB 前端整理、真实 E2E 数据重置、产品化审计和分批整改的入口文件。执行时先读本文，再按链接进入专项文档。

## 1. 当前目标

当前阶段不是直接追求“全站逐按钮一次性测完并修完”，而是先把工作区整理成可持续迭代状态：

1. 清理或重置本地真实 E2E 数据，避免历史测试数据干扰全量测试。
2. 用真实浏览器做前端产品化审计，识别空功能、混乱布局、表单位置错误、假按钮和功能闭环缺口。
3. 按 UI 模式和业务域拆分整改批次，而不是在全站随机修补。
4. 每批整改后用定向 Playwright MCP 回归和仓库验证命令确认结果。
5. 每轮测试与修复完成后，在涉及的子仓库分别提交 commit；进入下一轮测试前工作区应保持干净。

当前整改以桌面端体验为主，不要求移动端适配。默认使用 1440x900、1280x800 等桌面视口做审计和回归；390px/375px 小屏专项问题只记录为非本阶段范围，除非它同时暴露桌面端核心流程问题。

## 2. 必读顺序

1. 工作区规则：`/Users/moorefoss/Code/AUBB/AGENTS.md` 和 `AGENTS-shared.md`。
2. 前端规则：`/Users/moorefoss/Code/AUBB/web/AGENTS.md`。
3. 前端设计规范：[前端设计规范](../04-development/frontend-design.md)。
4. 本地 E2E 数据处理：[本地 E2E 数据重置与清理规范](local-e2e-data-reset-2026-06-05.md)。
5. 审计与整改计划：[前端产品化审计与整改计划](frontend-product-audit-and-refactor-plan-2026-06-05.md)。
6. 已有审计证据：
   - [前端 Playwright MCP 全面审计报告](frontend-audit-2026-06-01.md)
   - [前端人工走查意见记录](frontend-manual-review-notes-2026-06-05.md)
   - [全量用户侧功能测试矩阵](full-user-function-test-matrix-2026-06-04.md)
   - [全量用户侧功能测试报告](full-user-function-test-report-2026-06-05.md)

## 3. 工作区边界

根目录 `/Users/moorefoss/Code/AUBB` 不是 Git 仓库，三个子目录分别是独立仓库：

| 仓库 | 路径 | 当前任务中的角色 |
| --- | --- | --- |
| `web/` | `/Users/moorefoss/Code/AUBB/web` | 前端页面、组件、E2E 测试 |
| `server/` | `/Users/moorefoss/Code/AUBB/server` | 后端 API、数据库、fixture、清理脚本 |
| `docs/` | `/Users/moorefoss/Code/AUBB/docs` | 审计报告、计划、验收记录 |

开始任何修改前运行：

```bash
cd /Users/moorefoss/Code/AUBB
just status
```

如果发现已有 dirty 文件，先判断是否属于本轮任务。不要回退或覆盖无关改动。

真实浏览器测试必须使用 Playwright MCP 操作运行中的前端页面；本地 Playwright 脚本只能作为辅助诊断或补充验证，不能替代真实浏览器回归证据。

## 4. 阶段路线

### 阶段 A：整理基线

目标：确认工作区状态、数据策略和现有问题记录。

必做：

- 运行 `just status`。
- 阅读本入口文件和上方必读文档。
- 检查 `env/e2e.env` 是否存在，只记录变量名，不打印密码、token 或 JWT。
- 决定数据处理方式：优先整套 volume reset；如果需要保留本地数据，先做 dry-run 式定向清理计划。

产出：

- 不改代码时，只在回复或交接文档中记录状态。
- 若更新长期规则，只改 `docs/06-testing-and-ops/*`。

### 阶段 B：数据重置

目标：让全量测试从干净、可解释的本地数据基线开始。

优先使用 [本地 E2E 数据重置与清理规范](local-e2e-data-reset-2026-06-05.md) 中的“整套本地依赖重置”。

不允许：

- 直接在未知环境执行 `DELETE` / `TRUNCATE`。
- 打印真实数据库连接串、密码、token、cookie 或 JWT。
- 把数据库清理当成功能测试通过证据。

### 阶段 C：只读产品化审计

目标：先找清楚前端混乱在哪里，不在审计阶段修代码。

检查重点：

- 列表页是否把新增、编辑、导入表单堆在列表顶部或底部。
- 主操作、行操作、批量操作是否层级清楚。
- 按钮是否真实触发动作，是否有反馈、错误态和持久化结果。
- 空功能、假按钮、不可达入口、实现状态暴露给用户的问题。
- 文案、空态、加载态、错误态、桌面端布局密度和操作效率是否符合产品使用场景。

产出：

- `docs/06-testing-and-ops/frontend-product-audit-YYYY-MM-DD.md`
- 或追加到 [前端人工走查意见记录](frontend-manual-review-notes-2026-06-05.md)。

### 阶段 D：按批次整改

目标：按模式和业务域小批量修复。

推荐顺序：

1. 管理端 CRUD 模式：`/admin/users`、`/admin/org-units`、`/admin/academic-terms`、`/admin/course-catalogs`、`/admin/course-offerings`。
2. 教师端课程内容：成员、公告、资源、讨论、题库、判题环境。
3. 作业、提交、成绩、实验、通知等长链路页面。
4. 学生端课程、作业、工作区、成绩、实验、通知页面。

每批必须有：

- 问题来源。
- 涉及页面和文件。
- UI 模式选择。
- 回归方式。
- 验证命令。

### 阶段 E：回归与交接

每批整改后至少执行：

```bash
cd /Users/moorefoss/Code/AUBB/web
npm run lint
npm run typecheck
```

如果改动影响真实链路，再执行：

```bash
cd /Users/moorefoss/Code/AUBB
just dev-up
just healthcheck-strict
just e2e-real
```

逐页、逐按钮或产品化真实浏览器回归必须使用 Playwright MCP 操作页面并记录页面状态、网络请求或交互结果。

结束前运行：

```bash
cd /Users/moorefoss/Code/AUBB
just status
```

本轮验证通过后，必须进入涉及的子仓库分别提交 commit；提交后再次运行 `just status`，确认 `server/`、`web/`、`docs/` 在下一轮开始前是干净的。若用户明确要求暂不提交，交接中必须列出剩余 dirty 文件和原因。

## 5. 前端整改原则

- 列表页只承载浏览、筛选、排序、分页、主操作入口和行操作。
- 新增、编辑、导入、上传等表单优先使用 Dialog 或 Drawer。
- 删除、禁用、关闭、撤销等危险动作必须使用确认弹窗。
- 空功能必须删除、禁用并说明，或补齐真实实现；不能保留无反馈按钮。
- 业务页面不展示“已接通模块”“实现状态”这类开发过程信息。
- 页面结构要符合 `docs/04-development/frontend-design.md` 的专业、严谨、高效定位。

## 6. Agent 执行提示词

后续可以用以下提示词启动下一轮 agent：

```markdown
请接手 AUBB 前端整理工作，工作目录是 `/Users/moorefoss/Code/AUBB`。

先阅读：
1. `AGENTS.md`
2. `AGENTS-shared.md`
3. `docs/06-testing-and-ops/agent-frontend-remediation-entry-2026-06-05.md`
4. `docs/06-testing-and-ops/local-e2e-data-reset-2026-06-05.md`
5. `docs/06-testing-and-ops/frontend-product-audit-and-refactor-plan-2026-06-05.md`

本轮先不要全站乱改。请先运行 `just status`，确认 dirty 状态，然后按文档选择一个小批次执行。若需要真实浏览器验证，启动 `just dev-up` 和 `just healthcheck-strict`，使用 Playwright MCP 操作真实页面；不要用本地 Playwright 脚本替代 Playwright MCP 回归证据。

完成时必须说明改了哪些子仓库、运行了哪些验证、哪些问题仍未处理；涉及的子仓库必须提交 commit，并在提交后确认下一轮开始前工作区干净。
```
