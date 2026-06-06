---
title: "前端产品化审计与整改计划（2026-06-05）"
section: "06-testing-and-ops"
status: current
---
# 前端产品化审计与整改计划（2026-06-05）

本文把“前端很乱、功能和界面混乱、存在空功能、列表页表单位置不合理”等问题转成 agent 可执行的审计与整改计划。

## 1. 目标

让 AUBB 前端从“功能堆叠可见”整理成“真实用户可理解、可完成任务、可验证闭环”的产品界面。

本计划不要求一次性修完整个前端。正确方式是先审计，再按 UI 模式和业务域分批整改。

当前阶段以桌面端教学、管理和实验操作为主要使用场景，不要求移动端适配。审计与整改默认面向 1440x900、1280x800 等桌面视口；390px/375px 小屏专项问题不作为本阶段验收目标，除非同一缺陷也影响桌面端核心流程。

## 2. 不做什么

- 不在第一轮直接全站重构。
- 不用现有 E2E 通过率替代真实页面审计。
- 不把“页面能打开”“按钮能点击”“接口返回 200”当作功能正常。
- 不在列表页继续堆叠新增、编辑、导入等长表单。
- 不保留无反馈按钮、假按钮或只有开发状态说明的用户界面。
- 不把移动端或小屏适配作为本阶段整改目标。

## 3. 审计范围

当前前端页面主要位于 `/Users/moorefoss/Code/AUBB/web/src/app`，按角色分组：

| 角色 | 重点页面 |
| --- | --- |
| 管理员 | `/admin`、`/admin/users`、`/admin/org-units`、`/admin/academic-terms`、`/admin/course-catalogs`、`/admin/course-offerings`、`/admin/platform-config`、`/admin/audit-logs`、`/admin/auth-explain` |
| 教师 | `/teacher`、`/teacher/courses`、课程详情及成员/公告/资源/讨论/题库/判题环境、作业、提交、成绩册、实验、通知 |
| 学生 | `/student`、课程、作业、编程工作区、提交详情、成绩、实验、通知 |
| 公共 | `/login`、`/unauthorized`、`/me/notifications`、根路径重定向 |

## 4. 问题分类

| 编号 | 类别 | 判定标准 | 典型修复 |
| --- | --- | --- | --- |
| UX-CRUD | CRUD 结构混乱 | 列表页顶部或底部长期显示新增/编辑表单 | 改为 Dialog 或 Drawer；列表只保留主按钮和行操作 |
| UX-EMPTY | 空功能 / 假功能 | 按钮无动作、动作无反馈、入口不可达 | 删除入口、禁用并说明，或补齐真实实现 |
| UX-FLOW | 功能不闭环 | 新增后不刷新、编辑后不可验证、删除无确认、上传无状态 | 补成功/失败反馈、刷新、持久化验证 |
| UX-INFO | 信息架构混乱 | 主次信息不清，开发状态暴露给用户 | 重排页面区域，移除实现状态类信息 |
| UX-COPY | 文案不清 | 用户无法判断当前对象、操作后果或错误原因 | 改写标题、按钮、空态、错误提示 |
| UX-STATE | 状态缺失 | 无加载态、空态、错误态、禁用态 | 使用统一 `ApiState` / skeleton / toast / inline error |
| UX-DESKTOP | 桌面端效率问题 | 桌面视口下主操作不突出、表格/筛选/详情布局浪费空间或相互挤压 | 检查 1440x900 和 1280x800 桌面视口，调整信息密度、导航层级和表格策略 |
| UX-A11Y | 可访问性 / 可测性 | 输入框无 label，按钮无稳定名称 | 补 label、aria-label、语义化按钮 |

## 5. 只读审计流程

第一轮只读，不改代码。

执行步骤：

1. 运行：

```bash
cd /Users/moorefoss/Code/AUBB
just status
```

2. 如需真实页面，启动：

```bash
cd /Users/moorefoss/Code/AUBB
just dev-up
just healthcheck-strict
```

3. 使用 Playwright MCP 登录管理员、教师、学生账号，逐角色检查侧边栏入口和主要页面。
   - 真实浏览器测试主证据必须来自 Playwright MCP 操作真实页面；本地 Playwright 脚本只能作为辅助诊断或补充验证，不能替代 MCP 回归证据。
   - 默认使用 1440x900 桌面视口；布局密集或列表复杂页面补充 1280x800 桌面视口。不要求 375px/390px 移动端回归。
4. 每页记录：
   - 页面目标是否清楚。
   - 主操作是否清楚。
   - 列表、详情、新增、编辑、删除、导入、导出是否各在合理位置。
   - 按钮是否真实有反馈。
   - 是否存在开发状态、实现说明或空功能。
   - 错误态、空态、加载态和桌面端布局效率是否可用。
5. 把问题写入审计报告或 [前端人工走查意见记录](frontend-manual-review-notes-2026-06-05.md)。

审计记录格式：

```md
### AUDIT-YYYYMMDD-NNN：<问题标题>

- 角色：
- 页面：
- 控件 / 区域：
- 问题分类：
- 现象：
- 预期：
- 严重级别：
- 建议整改模式：
- 证据：
- 状态：
```

## 6. 整改优先级

| 优先级 | 标准 | 处理时机 |
| --- | --- | --- |
| P0 | 登录、核心路由、主要角色完全不可用 | 立即处理 |
| P1 | 核心业务链路受阻，演示或验收明显失败 | 第一批处理 |
| P2 | 功能能用但体验混乱、闭环不足、效率低 | 按业务域处理 |
| P3 | 文案、视觉一致性、低风险可访问性问题 | 合并小批处理 |

## 7. 推荐整改批次

### 批次 1：管理端 CRUD 模式

目标：建立后续页面可复用的列表页和表单交互标准。

页面：

- `/admin/org-units`
- `/admin/users`
- `/admin/academic-terms`
- `/admin/course-catalogs`
- `/admin/course-offerings`

验收：

- 列表页不再长期展示新增/编辑长表单。
- 新增/编辑使用 Dialog 或 Drawer。
- 删除、禁用、撤销等危险操作有确认。
- 新增或编辑成功后列表刷新，且用户能看到明确反馈。
- 空态和错误态不是空白或静默失败。

### 批次 2：教师端课程内容管理

页面：

- `/teacher/courses/[offeringId]/members`
- `/teacher/courses/[offeringId]/announcements`
- `/teacher/courses/[offeringId]/resources`
- `/teacher/courses/[offeringId]/discussions`
- `/teacher/courses/[offeringId]/question-bank`
- `/teacher/courses/[offeringId]/judge-environments`

验收：

- 内容列表、创建入口、行操作一致。
- 上传、下载、删除和归档都有可见反馈。
- 空输入、非法文件、重复数据有明确错误提示。

### 批次 3：作业、提交、成绩和实验长链路

页面：

- `/teacher/assignments`
- `/teacher/assignments/create`
- `/teacher/assignments/[assignmentId]/edit`
- `/student/assignments`
- `/student/assignments/[assignmentId]`
- `/student/assignments/[assignmentId]/workspace/[questionId]`
- `/teacher/submissions`
- `/teacher/grading/gradebook`
- `/teacher/labs`
- `/student/labs`

验收：

- 教师创建、发布、关闭作业的状态链路清楚。
- 学生提交、教师批改、学生查看成绩闭环可用。
- 编程工作区主操作稳定，不因布局挤压或状态不明影响使用。

### 批次 4：首页、导航和全局体验

页面：

- `/admin`
- `/teacher`
- `/student`
- 顶栏、侧边栏、通知入口、用户菜单。

验收：

- 首页不展示开发过程信息。
- 快捷入口只保留真实用户高频动作。
- 顶栏搜索、通知、用户菜单有明确反馈。
- 桌面端顶栏、侧边栏、通知入口和用户菜单在 1280px 及以上视口可用且层级清楚。

## 8. UI 模式约定

| 场景 | 推荐模式 |
| --- | --- |
| 新增短表单 | Dialog |
| 编辑短表单 | Dialog |
| 新增或编辑复杂对象 | Drawer 或独立页面 |
| 批量导入 / 上传 | Dialog，包含文件选择、校验结果和错误列表 |
| 删除 / 禁用 / 关闭 | Confirm Dialog |
| 详情查看 | 独立详情页或右侧详情区域，不和创建表单混放 |
| 表格行操作 | 行内 icon/text 操作，危险动作二次确认 |
| 搜索筛选 | 列表顶部轻量筛选条，不挤占主内容 |

## 9. 每批整改执行模板

```md
## 整改批次：<名称>

- 目标：
- 页面：
- 问题来源：
- 涉及文件：
- 不做范围：
- UI 模式：
- 回归步骤：
- 验证命令：
- 提交记录：
- 残留风险：
```

## 10. 验证要求

前端代码修改后至少运行：

```bash
cd /Users/moorefoss/Code/AUBB/web
npm run lint
npm run typecheck
```

涉及真实用户链路时运行：

```bash
cd /Users/moorefoss/Code/AUBB
just dev-up
just healthcheck-strict
just e2e-real
```

真实浏览器逐页/逐按钮回归必须使用 Playwright MCP 操作页面并记录证据。本地 Playwright 脚本只允许作为辅助诊断或补充验证。

每批测试与修复完成后，必须在涉及的子仓库分别提交 commit。提交后再次运行：

```bash
cd /Users/moorefoss/Code/AUBB
just status
```

下一批开始前，`server/`、`web/`、`docs/` 应保持干净；若用户明确要求暂不提交，必须在交接中列出剩余 dirty 文件和原因。

只改文档时运行：

```bash
cd /Users/moorefoss/Code/AUBB/docs
npm run docs:build
```

## 11. 当前已知问题入口

当前已记录的前端整理线索包括：

- [前端人工走查意见记录](frontend-manual-review-notes-2026-06-05.md)：用户直接指出的页面问题。
- [全量用户侧功能测试报告](full-user-function-test-report-2026-06-05.md)：真实操作中发现的问题和复核结论。
- [前端 Playwright MCP 全面审计报告](frontend-audit-2026-06-01.md)：早期页面级审计结果。

后续整改时，以这些文件作为问题来源，不要只凭印象改页面。
