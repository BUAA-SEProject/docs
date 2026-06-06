---
title: "全量用户侧功能测试报告"
section: "06-testing-and-ops"
date: "2026-06-05"
status: in-progress
---

# AUBB 全量用户侧功能测试报告

## 1. 执行摘要

- 测试日期：2026-06-05
- 测试方式：Playwright MCP 真实浏览器操作 + API/数据库辅助验证
- 测试范围：管理员、教师、学生三角色全页面全控件
- 当前状态：进行中
- 最新补充：2026-06-06 09:34 CST，学生访问非所属教学班课程内容的跨角色权限负例已补充真实后端 Playwright 辅助回归；公告、资源、讨论接口均返回 403，页面显示权限错误并隐藏讨论创建入口。Playwright MCP 当前 `Transport closed`，本项仍待 MCP 恢复后复核。

## 2. 环境与账号

| 项目 | 值 |
|------|------|
| 前端 | http://127.0.0.1:3000 (Next.js 16) |
| 后端 | http://127.0.0.1:18080 (Spring Boot 4) |
| 数据库 | PostgreSQL (Docker) |
| 对象存储 | MinIO (Docker) |
| 判题服务 | go-judge (Docker) |
| 管理员账号 | U-SA1 |
| 教师账号 | U-TA1 |
| 学生账号 | u-st1 |

## 3. 数据准备与残留

| 数据类型 | 来源 | 关键 ID | 可清理 |
|----------|------|---------|--------|
| 学校根节点 | 已有 | id=1 (SCH-REALRUN) | 否 |
| 测试学院 | API 创建 | id=213 (E2E-FULLRUN 测试学院) | 是 |
| 测试用户 | UI 创建 | e2e-fullrun-ml1-testuser | 是 |
| 测试学期 | UI 创建 | E2E-FULLRUN-ML1-TERM | 是 |
| 测试课程模板 | UI 创建 | E2E-FULLRUN-ML1-CS101 | 是 |
| 学生课程关联 | DB 更新 | user_id=9, offering_id=1 | 是 |

## 4. 功能覆盖矩阵

（见阶段 1 产出的测试矩阵文件）

## 5. 按钮/控件覆盖矩阵

### 5.1 管理员 - 平台配置

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/platform-config | 管理员 | 平台名称输入框 | input | 修改为"E2E-FULLRUN-ML1 修改后平台" | 输入框值变化 | 值已变化 | — | 已真实操作通过 | — |
| /admin/platform-config | 管理员 | 保存配置按钮 | button | 点击保存 | 保存成功 | 保存成功 | 刷新后值仍为修改后值 | 已真实操作通过 | — |
| /admin/platform-config | 管理员 | 取消重置按钮 | button | 修改平台名称→点击取消重置 | 表单恢复原值 | 平台名称恢复为 "Realrun School" | — | 已真实操作通过 | — |
| /admin/platform-config | 管理员 | 平台简称输入框 | input | — | — | 显示 SCH-REALRUN | — | 只读/无副作用已验证 | — |
| /admin/platform-config | 管理员 | Logo URL 输入框 | input | — | — | 显示空 | — | 只读/无副作用已验证 | — |
| /admin/platform-config | 管理员 | 页脚文字输入框 | input | — | — | 显示 E2E 历史值 | — | 只读/无副作用已验证 | — |
| /admin/platform-config | 管理员 | 清空按钮 | button | 点击清空 | 页脚文字清空 | 页脚文字输入框清空 | — | 已真实操作通过 | — |
| /admin/platform-config | 管理员 | 默认首页路径输入框 | input | — | — | 显示 /admin | — | 只读/无副作用已验证 | — |
| /admin/platform-config | 管理员 | 主题键输入框 | input | — | — | 显示 aubb-light | — | 只读/无副作用已验证 | — |
| /admin/platform-config | 管理员 | 登录公告文本框 | textarea | — | — | 显示空 | — | 只读/无副作用已验证 | — |

### 5.2 管理员 - 组织架构

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/org-units | 管理员 | 新增根节点按钮 | button | 点击"新增根节点" | 表单切到根节点创建 | 表单标题"新增根节点"，节点类型固定 SCHOOL | Playwright MCP 截图/DOM：`#org-unit-type=SCHOOL` | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 根节点提交创建按钮 | button | 填写 MCP-20260605-135309 测试学校后点击提交 | 已存在学校根节点时给出明确业务错误 | POST `/api/v1/admin/org-units` 返回 409 `ORG_ROOT_ALREADY_EXISTS`，响应消息"学校根节点已存在" | 网络响应体已核对；未新增重复根节点 | 已真实操作通过（负例） | — |
| /admin/org-units | 管理员 | Realrun School 行加号 | button | 点击树中 Realrun School 行加号 | 表单切到学校下新增子节点 | 表单标题"在 [Realrun School] 下新增子节点"，节点类型 COLLEGE 可选 | Playwright MCP DOM：`#org-unit-type=COLLEGE`，`disabled=false` | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 节点类型下拉 | select | 在学校下新增子节点时保持 COLLEGE | 类型符合层级规则 | 选中 COLLEGE | — | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 名称输入框 | input | 输入"MCP-20260605-135309 测试学院" | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 编码输入框 | input | 输入"MCP-20260605-135309-COL" | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 排序输入框 | input | 输入 902 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 子节点提交创建按钮 | button | 点击提交创建 | 创建成功并在树中显示 | POST `/api/v1/admin/org-units` 返回 201，页面包含新学院名称和编码 | 列表重新请求 `/api/v1/admin/org-units/tree` 返回 200，刷新前 DOM 已包含新节点 | 已真实操作通过 | — |
| /admin/org-units | 管理员 | 创建成功后的根节点表单 | select | 子节点创建成功后观察根节点表单 | 不再出现常驻根节点表单状态残留 | 本轮已改为 Dialog 创建模式，子节点创建成功后关闭弹窗并清空父节点上下文 | 单元测试覆盖初始页不常驻提交按钮、根节点 Dialog 固定 SCHOOL、子节点 Dialog 默认 COLLEGE | 已修复 | BUG-20260605-009 |

**BUG-20260605-001**：组织架构 UI 创建 COLLEGE 类型节点失败

- 复核时间：2026-06-05 13:55
- 角色：管理员
- 页面：/admin/org-units
- 相关控件：Realrun School 行加号、提交创建按钮
- 复核结论：非缺陷，原复现路径不符合当前层级规则；COLLEGE 必须通过学校节点行加号创建，不能作为根节点创建。
- 真实操作：点击 Realrun School 行加号→填写 `MCP-20260605-135309 测试学院` / `MCP-20260605-135309-COL`→点击提交创建。
- 实际结果：POST `/api/v1/admin/org-units` 返回 201，树中出现新学院名称和编码。
- 持久化校验：页面自动重新请求 `/api/v1/admin/org-units/tree` 返回 200。
- 当前状态：已关闭，按设计通过。

**BUG-20260605-009**：组织架构子节点创建成功后根节点表单类型残留 COLLEGE

- 发现时间：2026-06-05 13:56
- 角色：管理员
- 页面：/admin/org-units
- 相关控件：子节点提交创建按钮、节点类型下拉
- 复现步骤：点击 Realrun School 行加号→创建学院成功→观察右侧表单。
- 实际结果：本轮已取消右侧常驻创建表单，新增根节点 / 子节点均通过 Dialog 完成，创建成功后弹窗关闭并清空父节点上下文。
- 预期结果：不再出现根节点表单与子节点类型残留的自相矛盾状态。
- 影响范围：原状态残留风险已被 Dialog 模式消解。
- 严重级别：P3
- 证据：单元测试 `src/tests/unit/admin/org-units-page.test.tsx` 覆盖初始页不常驻 `提交创建`、根节点 Dialog 固定 `SCHOOL`、子节点 Dialog 默认 `COLLEGE`。
- 当前状态：已修复，真实后端 Playwright 辅助回归通过；Playwright MCP 当前 `Transport closed`，待 MCP 恢复后复核。

### 5.3 管理员 - 用户管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/users | 管理员 | 新增用户按钮 | button | 点击打开表单 | 弹出创建表单 | 弹出表单 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 用户名输入框 | input | 输入 e2e-fullrun-ml1-testuser | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 显示名输入框 | input | 输入 E2E-ML1 测试用户 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 邮箱输入框 | input | 输入 e2e-ml1@test.local | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 初始密码输入框 | input | 输入 Test123456! | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 创建按钮 | button | 点击创建 | 创建成功 | 创建成功，用户出现在列表 | 搜索可找到 | 已真实操作通过 | — |
| /admin/users | 管理员 | 关键词搜索输入框 | input | 输入 U-TA1 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 搜索按钮 | button | 点击搜索 | 筛选结果 | 搜索到 U-TA1 | — | 已真实操作通过 | — |
| /admin/users | 管理员 | 用户行链接 | link | 点击 U-TA1 行 | 跳转详情页 | 跳转到 /admin/users/4 | 详情页显示完整信息 | 已真实操作通过 | — |
| /admin/users | 管理员 | 批量导入按钮 | button/file upload | 点击批量导入，选择重复用户名 CSV | 打开文件选择器，上传后展示导入总数、成功数、失败数和行级错误 | 上传 `U-SA1` 重复用户名 CSV 后页面显示“导入 1 行，成功 0 行，失败 1 行。”并展示第 2 行错误 | `POST /api/v1/admin/users/import` 返回 200，响应 `total=1/success=0/failed=1` | 辅助回归通过，待 MCP 复核 | — |
| /admin/users | 管理员 | 重置按钮 | button | 输入关键词→点击重置 | 搜索条件清空 | 关键词输入框清空，列表恢复完整 | — | 已真实操作通过 | — |

### 5.4 管理员 - 学期管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/academic-terms | 管理员 | 学期名称输入框 | input | 输入 E2E-FULLRUN-ML1 测试学期 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 学期编码输入框 | input | 输入 E2E-FULLRUN-ML1-TERM | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 学年输入框 | input | 输入 2026-2027 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 季节下拉 | select | 选择 SPRING | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 开始日期 | input | 输入 2027-02-01 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 结束日期 | input | 输入 2027-07-31 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 创建按钮 | button | 点击创建 | 创建成功 | 创建成功，列表显示新学期 | 列表可见 | 已真实操作通过 | — |
| /admin/academic-terms | 管理员 | 新增学期空提交 | button | 点击新增学期→不填写直接点击创建 | 显示字段级错误且不发送创建请求 | 显示 6 个字段错误，6 个字段均为 `aria-invalid=true` 且关联错误说明 | 未产生新增数据 | 已真实操作通过 | — |

### 5.5 管理员 - 课程模板

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/course-catalogs | 管理员 | 课程名称输入框 | input | 输入 E2E-FULLRUN-ML1 测试课程 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 课程编码输入框 | input | 输入 E2E-FULLRUN-ML1-CS101 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 学院下拉 | select | 选择计算机学院 | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 学分输入框 | input | 输入 3 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 学时输入框 | input | 输入 48 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 课程类型下拉 | select | 选择必修 | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 描述文本框 | textarea | 输入测试描述 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 创建模板按钮 | button | 点击创建 | 创建成功 | 创建成功，列表显示 | 列表可见 | 已真实操作通过 | — |
| /admin/course-catalogs | 管理员 | 新增模板空提交 | button | 点击新增模板→不填写直接点击创建 | 显示字段级错误且不发送创建请求 | 显示 4 个字段错误，4 个字段均为 `aria-invalid=true` 且关联错误说明；所属学院下拉只包含学院节点 | 未产生新增数据 | 已真实操作通过 | — |

### 5.6 管理员 - 开课管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/course-offerings | 管理员 | collegeUnitId 输入框 | input | 输入 2 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 课程模板下拉 | select | 选择 E2E-FULLRUN-ML1 测试课程 | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 学期下拉 | select | 选择 E2E-FULLRUN-ML1 测试学期 | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 开课名称输入框 | input | 输入 E2E-FULLRUN-ML1 测试开课 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 开课编码输入框 | input | 输入 E2E-FULLRUN-ML1-OFF | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 开始时间 | input | 输入 2027-02-01T08:00 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 结束时间 | input | 输入 2027-07-31T23:59 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/course-offerings | 管理员 | 完成创建按钮 | button | 点击完成创建 | 创建成功 | 课程模板自动锁定主开课学院，缺主讲教师时显示字段错误；补选教师后创建成功 | POST `/api/v1/admin/course-offerings` 返回 201，Toast 显示“开课实例已创建” | 已真实操作通过 | BUG-20260605-002 |

**BUG-20260605-002**：开课管理 UI 创建失败

- 发现时间：2026-06-05 17:00
- 角色：管理员
- 页面：/admin/course-offerings
- 相关控件：完成创建按钮
- 输入数据：模板=E2E-FULLRUN-ML1-CS101，学期=E2E-FULLRUN-ML1-TERM，名称=E2E-FULLRUN-ML1 测试开课
- 复现步骤：点击新增→填写表单→点击完成创建
- 实际结果：已修复。课程模板选择后主开课学院自动同步为模板所属学院并禁用；缺少主讲教师时显示“请至少指定一名教师”，主讲教师控件设置 `aria-invalid=true` 且关联 `offering-instructors-error`；补选主讲教师后创建请求成功。
- 预期结果：创建成功并在列表显示
- 影响范围：管理员无法通过 UI 创建开课
- 严重级别：P1
- 修复证据：2026-06-05 21:45 CST，Playwright 真实登录管理员账号打开 `/admin/course-offerings`，选择课程模板“数据结构 (COURSE-A)”后主开课学院值为 `2` 且禁用；缺主讲教师时错误状态可见；补选教师后 `POST /api/v1/admin/course-offerings` 返回 201。
- 当前状态：已修复

### 5.7 管理员 - 用户详情

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/users/376 | 管理员 | 返回列表链接 | link | 点击 | 跳转用户列表 | 跳转到 /admin/users | — | 已真实操作通过 | — |
| /admin/users/621 | 管理员 | 强制下线按钮 | button | 点击强制下线→确认 | 注销该用户所有活跃会话并给出明确确认 | 显示“确认强制下线？”确认弹窗，确认后请求成功 | `POST /api/v1/admin/users/621/sessions/revoke` 返回 204 | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | 禁用账号按钮 | button | 点击禁用→确认 | 账号状态变禁用 | 弹出确认弹窗→确认后状态变"禁用" | 刷新后仍为禁用 | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | 启用账号按钮 | button | 点击启用→确认 | 账号状态恢复激活 | 弹出确认弹窗→确认后状态变"激活" | 刷新后仍为激活 | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | 角色下拉框 | select | 选择 COLLEGE_ADMIN | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | scopeOrgUnitId 输入框 | input | 输入 2 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | 保存身份按钮 | button | 点击保存 | 身份更新成功 | Toast"用户身份已更新"，页面显示 COLLEGE_ADMIN | 刷新后仍显示 | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | orgUnitId 输入框 | input | 输入 2 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/users/376 | 管理员 | 替换组织关系按钮 | button | 点击替换 | 组织关系更新 | Toast"组织成员关系已更新"，显示计算机学院 | 刷新后仍显示 | 已真实操作通过 | — |
| /admin/users/621 | 管理员 | 学籍资料编辑与保存 | form/button | 修改真实姓名、学号/工号、身份类型、联系电话→点击保存学籍资料 | 字段可编辑，保存后资料持久化 | 表单显示可编辑字段，保存后详情重新加载 | `PUT /api/v1/admin/users/621/profile` 返回 200，响应含 `academicId=MCP-REG-621`、`realName=MCP回归姓名-621`、`identityType=TEACHER`、`phone=13900000621` | 已真实操作通过 | — |

### 5.8 管理员 - 审计日志

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/audit-logs | 管理员 | 页面加载 | — | 打开页面 | 显示日志列表 | 292 页数据，含真实操作记录 | — | 已真实操作通过 | — |
| /admin/audit-logs | 管理员 | 操作者 ID 输入框 | input | — | — | 可见 | — | 只读/无副作用已验证 | — |
| /admin/audit-logs | 管理员 | 操作类型输入框 | input | 输入 USER_STATUS_CHANGED | 筛选结果 | 返回 3 页 USER_STATUS_CHANGED 记录 | — | 已真实操作通过 | — |
| /admin/audit-logs | 管理员 | 操作类型下拉框 | select | 选择“登录成功”后点击查询 | 返回登录成功记录 | 触发 `GET /api/v1/admin/audit-logs?action=LOGIN_SUCCESS&page=1&pageSize=20`，表格显示多条“登录成功”记录 | 网络请求 200，响应 `total=2849` | 已真实操作通过 | BUG-20260605-003 |
| /admin/audit-logs | 管理员 | 对象类型输入框 | input | — | — | 可见 | — | 只读/无副作用已验证 | — |
| /admin/audit-logs | 管理员 | 查询按钮 | button | 点击查询 | 返回筛选结果 | 返回结果 | — | 已真实操作通过 | — |
| /admin/audit-logs | 管理员 | 详情按钮 | button | 点击“查看日志详情 登录成功 8007807c” | 显示中文元数据详情 | 底部显示“日志元数据”和说明“当前行的原始审计上下文，用于排查请求链路和业务对象。” | 前 5 行详情按钮均具备“查看日志详情 <操作> <短 ID>”可访问名称 | 已真实操作通过 | — |
| /admin/audit-logs | 管理员 | Request ID 复制按钮 | button | 点击“复制请求 ID 8007807c” | 复制到剪贴板并给出明确反馈 | 页面显示“Request ID 已复制” | 前 5 行复制按钮均具备“复制请求 ID <短 ID>”可访问名称 | 已真实操作通过 | — |
| /admin/audit-logs | 管理员 | 复制 JSON 按钮 | button | 点击复制 | 复制 JSON 到剪贴板并给出明确反馈 | 页面显示“JSON 已复制” | `navigator.clipboard.writeText` 接收当前行元数据 JSON | 已真实操作通过 | — |
| /admin/audit-logs | 管理员 | 分页控件 | pagination | — | — | 显示"第 1 页 / 共 292 页" | — | 只读/无副作用已验证 | — |

### 5.9 管理员 - 权限解释

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /admin/auth-explain | 管理员 | 页面加载 | — | 打开页面 | 显示权限查询界面 | 页面加载成功，显示权限诊断、创建授权组、添加成员三个区域 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 用户 ID 输入框 | input | 输入 4 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 权限编码输入框 | input | 输入 OFFERING_READ / USER_READ / bad | 输入成功 | 输入成功，非法编码触发受控错误态 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 作用域类型下拉 | select | 选择 OFFERING | 选中成功 | 选中成功，默认 PLATFORM，含 6 个选项 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 立即分析按钮（允许） | button | userId=4，permission=OFFERING_READ，scopeType=OFFERING，scopeRefId=1 后点击分析 | 返回允许结果 | 页面显示"允许 (ALLOWED)"，reasonCode 为 `ALLOW_BY_SCOPE_ROLE` | `GET /api/v1/admin/auth/explain?...permission=OFFERING_READ...` 返回 200 | 已真实操作通过 | BUG-20260605-004 |
| /admin/auth-explain | 管理员 | 立即分析按钮（拒绝） | button | permission=USER_READ 后点击分析 | 返回拒绝结果 | 页面显示"拒绝 (DENIED)"，reasonCode 为 `DENY_NO_ROLE_BINDING` | `GET /api/v1/admin/auth/explain?...permission=USER_READ...` 返回 200 | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 立即分析按钮（非法编码） | button | permission=bad 后点击分析 | 显示可读错误态且页面不崩溃 | 页面显示"数据加载失败"和 `Failed to convert 'permission' with value: 'bad'` | `GET /api/v1/admin/auth/explain?...permission=bad...` 返回 400 | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | templateCode 输入框 | input | 输入 audit-readonly | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | displayName 输入框 | input | 输入"MCP 审计只读组 0606-0350" | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 创建授权组按钮（有效模板） | button | templateCode=audit-readonly，scopeType=SCHOOL，scopeRefId=1 后点击创建 | 授权组创建成功 | 返回新授权组，页面自动填充 groupId=1 | `POST /api/v1/admin/auth/groups` 返回 201，响应含 `templateCode=audit-readonly`、`scopeType=SCHOOL`、`status=ACTIVE` | 已真实操作通过 | BUG-20260605-005 |
| /admin/auth-explain | 管理员 | 创建授权组按钮（无效模板） | button | templateCode=missing-template-mcp-0606 后点击创建 | 显示模板不存在错误 | 返回 `AUTHZ_TEMPLATE_NOT_FOUND` / "授权组模板不存在" | `POST /api/v1/admin/auth/groups` 返回 404，无新增授权组 | 预期错误已验证 | — |
| /admin/auth-explain | 管理员 | groupId 输入框 | input | 创建有效授权组后查看 | 自动填入新组 ID | 自动填入 `1` | 来自创建授权组 201 响应 | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | userId 输入框 | input | 输入 4 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /admin/auth-explain | 管理员 | 添加成员按钮 | button | groupId=1，userId=4 后点击添加成员 | 成员添加成功 | 返回成员绑定记录 | `POST /api/v1/admin/auth/groups/1/members` 返回 201，响应含 `groupId=1`、`userId=4`、`sourceType=MANUAL` | 已真实操作通过 | — |

### 5.10 教师 - 公告管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/announcements | 教师 | 发布公告 | h2(可点击) | 点击打开表单 | 弹出标题/正文表单 | 弹出表单 | — | 已真实操作通过 | — |
| /teacher/courses/1/announcements | 教师 | 公告标题输入框 | input | 输入 E2E-FULLRUN-ML2 测试公告 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /teacher/courses/1/announcements | 教师 | 公告正文文本框 | textarea | 输入测试内容 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /teacher/courses/1/announcements | 教师 | 发布按钮 | button | 点击发布 | 公告创建成功 | 列表显示新公告 | 刷新后仍可见 | 已真实操作通过 | — |
| /teacher/courses/1/announcements | 教师 | 发布公告空提交 | button | 点击发布公告→标题和正文留空→点击发布 | 显示字段级错误且不发送创建请求 | 显示“请输入公告标题 / 请输入公告正文”，两个字段 `aria-invalid=true`，未发送 `POST /announcements` | 无新增公告；临时编辑种子清理后残留数 0 | 已真实操作通过 | — |
| /teacher/courses/1/announcements | 教师 | 编辑公告空提交 | button | 点击编辑公告→清空标题和正文→点击保存 | 显示字段级错误且不发送更新请求 | 显示“请输入公告标题 / 请输入公告正文”，两个字段 `aria-invalid=true`，未发送 `PUT /announcements`，无 Dialog 描述警告 | 临时公告种子通过 API 删除，`E2E-ANN-NEG-*` 残留数 0 | 已真实操作通过 | — |

### 5.11 教师 - 讨论管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/discussions | 教师 | 创建讨论按钮 | button/h2 | 点击打开表单 | 弹出标题/正文表单 | 弹出表单 | — | 已真实操作通过 | — |
| /teacher/courses/1/discussions | 教师 | 标题输入框 | input | 输入 E2E-FULLRUN-ML2 测试讨论 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /teacher/courses/1/discussions | 教师 | 正文文本框 | textarea | 输入测试内容 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /teacher/courses/1/discussions | 教师 | 提交按钮 | button | 点击提交 | 讨论创建成功 | 列表显示新讨论 | 刷新后仍可见 | 已真实操作通过 | — |
| /teacher/courses/1/discussions | 教师 | 创建讨论空提交 | button | 点击创建讨论→标题和正文留空→点击创建 | 显示字段级错误且不发送创建请求 | 显示“请输入讨论标题 / 请输入讨论正文”，两个字段 `aria-invalid=true`，未发送 `POST /discussions` | 无新增讨论 | 已真实操作通过 | — |
| /teacher/courses/1/discussions | 教师 | 锁定 / 解锁讨论按钮 | button | 读取讨论列表行操作名称 | 每个按钮都能区分对应讨论 | 20 个锁定 / 解锁按钮均可通过“锁定讨论 <标题> / 解锁讨论 <标题>”定位 | — | 已真实操作通过 | P2-L15 |

### 5.12 教师 - 资源管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/resources | 教师 | 页面加载 | — | 打开页面 | 显示资源列表 | 4 个资源文件，含文件名/大小/时间 | — | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 下载按钮 | button | 点击下载 | 文件下载成功 | 文件 e2e-fullrun-ml2-resource.txt 下载（41B） | 文件内容正确 | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 重命名按钮 | button | 点击→修改标题→保存 | 标题更新 | 弹出"编辑资源标题"对话框→修改为"E2E-FULLRUN 重命名测试资源"→保存成功 | 刷新后标题仍为新值 | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 编辑资源标题空提交 | button/input | 点击编辑→清空资源标题→保存 | 显示字段级错误且不发送更新请求 | 显示“请输入资源标题”，资源标题字段 `aria-invalid=true`，未发送 `PUT /teacher/course-resources/*` | 无标题变更 | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 编辑 / 删除资源行操作 | button | 读取资源列表行操作名称 | 每个按钮都能区分对应资源 | 4 个编辑按钮均可通过“编辑资源 <标题>”定位；抽查资源的“删除资源 <标题>”按钮可定位 | — | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 上传 / 编辑资源弹窗描述 | dialog | 分别打开上传和编辑弹窗 | 弹窗有清晰说明且无可访问性警告 | 上传弹窗显示“上传后学生可在课程资源区下载该文件。标题为空时将使用文件名。”；编辑弹窗显示“资源标题会显示在教师和学生端资源列表中。”；无 Radix Dialog 描述警告 | — | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 删除按钮 | button | 点击删除→确认 | 资源删除 | 弹出确认弹窗→确认后 Toast"资源已删除" | 刷新后资源不在列表 | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 资源标题输入框 | input | 输入"E2E-FULLRUN 上传测试资源" | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 选择文件区域 | upload | 选择 e2e-upload-test.txt | 文件选择成功 | 显示文件名和大小 | — | 已真实操作通过 | — |
| /teacher/courses/1/resources | 教师 | 开始上传按钮 | button | 点击上传 | 上传成功 | Toast"资源已上传"，新资源出现在列表 | 刷新后仍可见 | 已真实操作通过 | — |

### 5.12A 教师 - 成员管理补充

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/members | 教师 | 停用 / 恢复成员按钮 | button | 读取成员列表行操作名称 | 每个按钮都能区分对应成员 | 20 个状态按钮均可通过“停用成员 <姓名> / 恢复成员 <姓名>”定位 | — | 已真实操作通过 | P2-L14 |
| /teacher/courses/1/members | 教师 | 转班成员按钮 | button | 读取成员列表行操作名称 | 每个按钮都能区分对应成员 | 20 个转班按钮均可通过“转班成员 <姓名>”定位 | — | 已真实操作通过 | P2-L14 |
| /teacher/courses/1/members | 教师 | 添加成员空 userId | button/input | 点击添加成员→不填写 userId→点击添加 | 显示字段级错误且不发送添加请求 | 显示“请输入有效的 userId”，用户 ID 字段 `aria-invalid=true` | 未发送 `POST /teacher/course-offerings/1/members/batch` | 已真实操作通过 | — |
| /teacher/courses/1/members | 教师 | 添加成员缺教学班 | button/select | 填写 userId，角色保持学生，教学班留空→点击添加 | 显示字段级错误且不发送添加请求 | 显示“当前角色必须选择教学班”，教学班字段 `aria-invalid=true` | 未发送 `POST /teacher/course-offerings/1/members/batch` | 已真实操作通过 | — |
| /teacher/courses/1/members | 教师 | 添加成员成功反馈 | button/dialog | 填写用户 ID 621，角色选择整课助教→点击添加 | 添加成功后保留明确结果反馈 | 弹窗保持打开并显示“添加成功 1 人，失败 0 人。” | `POST /api/v1/teacher/course-offerings/1/members/batch` 返回 200 | 已真实操作通过 | — |
| /teacher/courses/1/members | 教师 | 添加 / 导入 / 转班弹窗描述 | dialog | 分别打开三个弹窗 | 弹窗有清晰说明且无可访问性警告 | 三个弹窗均显示说明文本，未出现 Radix Dialog 描述警告 | — | 已真实操作通过 | — |

### 5.13 教师 - 题库

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/question-bank | 教师 | 页面加载 | — | 打开页面 | 显示题库列表 | 5 个题目（SHORT_ANSWER, MULTIPLE_CHOICE, SINGLE_CHOICE, PROGRAMMING） | — | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 类型筛选下拉框 | select | 选择 PROGRAMMING | 筛选结果 | 只显示 1 个 PROGRAMMING 题目 | — | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 查询按钮 | button | 点击查询 | 返回筛选结果 | 返回结果 | — | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 分类管理入口 | button | 检查是否存在假入口 | 不保留无契约支撑的空功能按钮 | 后端稳定 API 仅提供分类/标签字典读取，分类通过题目创建/编辑时的 `categoryName` 自动维护；当前页面不再保留“分类管理”假按钮 | API 契约核对：`stable-api.md` 仅列出题目 CRUD 与分类列表读取 | 非缺陷，入口已清理 | BUG-20260605-008 |
| /teacher/courses/1/question-bank | 教师 | 新增题目按钮 | button | 填写标题/题干/分值/分类/标签→点击创建 | 题目创建成功并刷新题库列表、分类、标签 | 创建 `MCP-QUESTION-0606-0402` 后页面无需手动查询即显示新题，标签筛选新增 `autorefresh` | `POST /api/v1/teacher/course-offerings/1/question-bank/questions` 返回 201，随后自动触发 questions/categories/tags GET 200；刷新后 `MCP-QUESTION-0606-0356` 仍可见 | 已真实操作通过 | BUG-20260606-003 |
| /teacher/courses/1/question-bank | 教师 | 编辑题目按钮 | button | 点击编辑 | 弹出编辑对话框 | 点击“编辑题目 E2E-FULLRUN 新增测试题目”后打开“编辑题目”Dialog，并带入原题目标题和分值 | Playwright MCP DOM 读取 Dialog 标题、描述、`#question-title` 与 `#question-score` | 已真实操作通过 | BUG-20260605-006 |
| /teacher/courses/1/question-bank | 教师 | 编辑 / 归档行操作名称 | button | 读取题目列表行操作名称 | 每个按钮都能区分对应题目 | 前 3 行按钮均具备“编辑题目 <标题> / 归档题目 <标题>”的 `aria-label` 与 `title` | Playwright MCP DOM 读取 `main table button` 的 `aria-label` / `title`；单元测试覆盖“二叉树遍历”行 | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 归档按钮 | button | 点击归档 | 题目归档 | Toast"题目已归档" | — | 已真实操作通过 | — |

### 5.14 教师 - 判题环境

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/judge-environments | 教师 | 页面加载 | — | 打开页面 | 显示判题环境列表 | 页面加载成功 | — | 只读/无副作用已验证 | — |
| /teacher/courses/1/judge-environments | 教师 | 编程语言筛选 / 查询 | select/button | 选择 Go 1.22 后点击查询 | 只查询 Go 环境 | 触发 `GET /teacher/course-offerings/1/judge-environment-profiles?programmingLanguage=GO122&includeArchived=false`，列表过滤到 Go 1.22 | 网络请求 200 | 已真实操作通过 | — |
| /teacher/courses/1/judge-environments | 教师 | 新增配置空提交 | button/form | 打开新增配置后直接点击创建 | 显示字段级错误且不发送创建请求 | 显示“请输入配置编码 / 请输入配置名称”，两个字段 `aria-invalid=true` | 空提交期间未新增 `POST` 创建请求 | 已真实操作通过 | — |
| /teacher/courses/1/judge-environments | 教师 | 新增配置正常路径 | button/form | 填写 Go 1.22 配置后点击创建 | 创建成功并出现在列表 | Toast“判题环境已保存”，新配置显示在 Go 1.22 列表 | `POST /teacher/course-offerings/1/judge-environment-profiles` 返回 201 | 已真实操作通过 | — |
| /teacher/courses/1/judge-environments | 教师 | 编辑配置按钮 | button/dialog | 点击新配置行的编辑按钮 | 打开编辑弹窗并带入已有值 | “编辑配置”弹窗带入配置编码、名称、语言 Go 1.22、语言版本和运行命令；保存后 Toast“判题环境已更新” | `PUT /teacher/judge-environment-profiles/{id}` 返回 200 | 已真实操作通过 | — |
| /teacher/courses/1/judge-environments | 教师 | 归档配置按钮 | button/dialog | 点击归档并确认 | 归档成功，默认列表隐藏，包含归档后显示已归档状态 | 确认文案包含配置名；Toast“判题环境已归档”；默认筛选下记录隐藏，勾选包含归档后状态为“已归档”，行内不再显示归档按钮 | `POST /teacher/judge-environment-profiles/{id}/archive` 返回 200；包含归档查询返回 200 | 已真实操作通过 | — |

### 5.15 教师 - 通知公告

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/notifications | 教师 | 页面加载 | — | 打开页面 | 显示通知列表 | 28 条通知，分 2 页 | — | 已真实操作通过 | — |
| /teacher/notifications | 教师 | 标记已读按钮 | button | 点击标记已读 | 通知状态更新 | 未读数从 28 变为 27 | — | 已真实操作通过 | — |
| /teacher/notifications | 教师 | 全部已读按钮 | button | 点击全部已读 | 所有通知标记已读 | 未读数徽章消失 | — | 已真实操作通过 | — |
| /teacher/notifications | 教师 | 分页控件 | pagination | — | — | 显示"共 28 条，第 1/2 页" | — | 只读/无副作用已验证 | — |

### 5.16 学生 - 课程学习

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /student/courses/1 | 学生 | 页面加载 | — | 打开页面 | 显示公告、资源、讨论 | 3 个公告、4 个资源、11 个讨论 | — | 已真实操作通过 | — |
| /student/courses/1 | 学生 | 资源下载按钮 | button | 点击下载 | 文件下载成功 | 文件 e2e-fullrun-ml2-resource.txt 下载（41B） | 文件内容正确 | 已真实操作通过 | — |
| /student/courses/1 | 学生 | 讨论标题输入框 | input | 输入"E2E-FULLRUN 学生测试讨论" | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /student/courses/1 | 学生 | 讨论内容输入框 | textarea | 输入测试内容 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /student/courses/1 | 学生 | 创建讨论按钮 | button | 点击创建 | 讨论创建成功 | 新讨论出现在列表，链接到 /student/courses/1/discussions/18 | 刷新后仍可见 | 已真实操作通过 | — |
| /student/courses/{非所属教学班} | 学生 | 跨班级课程内容 | page/API | 学生打开未加入的教学班课程页 | 公告、资源、讨论均显示清晰无权访问状态，不暴露可提交讨论入口 | 页面显示“无权访问课程公告/课程资源/课程讨论，请确认已加入此课程”，讨论标题输入框与“创建讨论”按钮隐藏 | `GET /api/v1/me/course-classes/{classId}/announcements`、`resources`、`discussions` 均返回 403 | 辅助回归通过，待 MCP 复核 | BUG-20260606-016 |

### 5.17 学生 - 讨论详情

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /student/courses/1/discussions/18 | 学生 | 页面加载 | — | 打开页面 | 显示讨论内容和回复表单 | 显示讨论标题、时间、"可回复"状态 | — | 已真实操作通过 | — |
| /student/courses/1/discussions/18 | 学生 | 回复内容输入框 | textarea | 输入回复内容 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /student/courses/1/discussions/18 | 学生 | 发布回复按钮 | button | 点击发布 | 回复发布成功 | Toast"回复已发布"，新回复出现在列表 | 刷新后仍可见 | 已真实操作通过 | — |
| /student/courses/1/discussions/18 | 学生 | 返回课程链接 | link | — | — | 可见，指向 /student/courses/1 | — | 只读/无副作用已验证 | — |

### 5.18 学生 - 我的成绩

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /student/grades | 学生 | 页面加载 | — | 打开页面 | 显示成绩页面 | 显示课程选择下拉框和成绩表 | — | 已真实操作通过 | — |
| /student/grades | 学生 | 课程选择下拉框 | select | 选择"数据结构 2025 秋" | 选中成功 | 选中成功，表显示"暂无成绩数据" | — | 已真实操作通过 | — |
| /student/grades | 学生 | 导出成绩按钮 | button | 点击导出 | CSV 文件下载 | 文件 gradebook-me-offering-1.csv 下载 | 文件存在 | 已真实操作通过 | — |

### 5.19 学生 - 通知中心

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /student/notifications | 学生 | 页面加载 | — | 打开页面 | 显示通知列表 | 8 条通知 | — | 已真实操作通过 | — |
| /student/notifications | 学生 | 标记已读按钮 | button | 点击标记已读 | 通知状态更新 | 未读数从 8 变为 7 | — | 已真实操作通过 | — |
| /student/notifications | 学生 | 全部已读按钮 | button | 点击全部已读 | 所有通知标记已读 | 未读数徽章消失（从 8 变为 0） | — | 已真实操作通过 | — |
| /student/notifications | 学生 | 全部已读后列表刷新 | button/list | 发布临时实验生成 1 条未读通知，点击“全部已读” | 未读徽章消失，通知列表同步转为已读，不再显示“标记已读” | 修复前 `POST /read-all` 200 后列表仍保留“标记已读”；修复后未读徽章消失，列表刷新后隐藏行按钮 | 后端只读校验 `unreadCount=0`，目标通知 `read=true`，`firstUnreadId=null` | 已真实操作通过 | BUG-20260606-014 |

## 6. Playwright MCP 操作证据

（按操作顺序记录）

### 5.20 教师 - 题库管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/question-bank | 教师 | 页面加载 | — | 打开页面 | 显示题库列表 | 5 个题目（SHORT_ANSWER, MULTIPLE_CHOICE, SINGLE_CHOICE, PROGRAMMING） | — | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 类型筛选下拉框 | select | 选择 PROGRAMMING | 筛选结果 | 只显示 1 个 PROGRAMMING 题目 | — | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 查询按钮 | button | 点击查询 | 返回筛选结果 | 返回结果 | — | 已真实操作通过 | — |
| /teacher/courses/1/question-bank | 教师 | 编辑题目按钮 | button | 点击编辑 | 弹出编辑对话框 | 点击“编辑题目 E2E-FULLRUN 新增测试题目”后打开“编辑题目”Dialog，并带入原题目标题和分值 | Playwright MCP DOM 读取 Dialog 标题、描述、`#question-title` 与 `#question-score` | 已真实操作通过 | BUG-20260605-006 |
| /teacher/courses/1/question-bank | 教师 | 归档按钮 | button | 点击归档 | 题目归档 | Toast"题目已归档" | — | 已真实操作通过 | — |

### 5.21 教师 - 作业管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/assignments | 教师 | 选择课程下拉框 | select | 选择"数据结构 2025 秋" | 选中成功 | 选中成功，查询按钮启用 | — | 已真实操作通过 | — |
| /teacher/assignments | 教师 | 查询按钮 | button | 点击查询 | 返回作业列表 | 返回 20 页作业数据 | `GET /api/v1/teacher/course-offerings/1/assignments?page=1&pageSize=20` 返回 200 | 已真实操作通过 | — |
| /teacher/assignments | 教师 | 创建作业按钮 | link/button | 点击创建作业 | 打开创建表单并保留当前课程 | 跳转 `/teacher/assignments/create?offeringId=1` | — | 已真实操作通过 | — |
| /teacher/assignments/create?offeringId=1 | 教师 | 题库题目加入试卷 | select/button | 选择 `MCP-QUESTION-0606-0402 / 简答题 / 13 分` 后点击加入试卷 | 试卷显示 1 个分区 / 总分 13 | 页面显示 `1 个分区 / 总分 13`，包含题目 `MCP-QUESTION-0606-0402` | — | 已真实操作通过 | — |
| /teacher/assignments/create?offeringId=1 | 教师 | 创建作业按钮 | button | 填写标题、说明、教学班 A1、开放/截止时间、提交次数后提交 | 创建成功并返回列表 | 修复后 `POST /api/v1/teacher/course-offerings/1/assignments` 返回 201，列表出现 `MCP 作业回归 0606-0413` id=402 草稿 | 请求体中题库引用仅包含 `bankQuestionId=167` 和 `score=13`；201 响应 `paper.totalScore=13` | 已真实操作通过 | BUG-20260606-004 |
| /teacher/assignments | 教师 | 总分列 | table cell | 查看新建作业列表行 | 列表接口未返回试卷详情时不显示误导性 0 分 | 列表行总分显示 `暂无`；详情/创建/发布响应中的试卷总分仍为 13 | 列表响应 `paper=null`，前端使用未知态占位 | 已真实操作通过 | BUG-20260606-005 |
| /teacher/assignments/402/edit | 教师 | 保存作业按钮 | button | 将标题改为 `MCP 作业回归 0606-0413-编辑` 后保存 | 保存成功并返回列表 | `PUT /api/v1/teacher/assignments/402` 返回 200，列表标题更新 | PUT 请求体中题库引用仅包含 `bankQuestionId=167` 和 `score=13`；响应 `paper.totalScore=13` | 已真实操作通过 | BUG-20260606-004 |
| /teacher/assignments | 教师 | 发布作业按钮 | button | 点击发布→确认发布 | 作业状态变为已发布，发布按钮禁用，关闭按钮启用 | `POST /api/v1/teacher/assignments/402/publish` 返回 200；列表显示已发布 | DOM 校验 `publishDisabled=true`、`closeDisabled=false`，响应含 `publishedAt` | 已真实操作通过 | — |
| /teacher/assignments | 教师 | 关闭作业按钮 | button | 点击关闭 | 作业关闭 | Toast"作业已关闭" | — | 已真实操作通过 | — |

### 5.22 教师 - 提交管理

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/submissions | 教师 | 选择课程/作业下拉框 | select | 选择课程和作业 | 选项文本可读，选中成功 | 修复后课程下拉宽度约 280px，作业下拉宽度约 492px，长作业标题完整可读 | Playwright MCP DOM bbox 复核 | 已真实操作通过 | BUG-20260606-006 |
| /teacher/submissions | 教师 | 查询按钮 | button | 点击查询 | 返回提交列表 | 课程 `1` / 作业 `414` 返回提交 `139`，提交者 `807`，分数 `100` | 列表查询后 URL 保持 `offeringId=1&assignmentId=414` | 已真实操作通过 | — |
| /teacher/submissions | 教师 | 状态列 | table cell | 查看提交 `139` 状态 | 后端 `SUBMITTED` 显示为中文业务状态 | 状态列显示 `已提交`，不再裸露枚举值 | 单元契约覆盖 `SUBMITTED -> 已提交` | 已真实操作通过 | BUG-20260606-007 |
| /teacher/submissions | 教师 | 重新判题提交 139 | button | 点击重判→确认弹窗确认 | 先确认再创建手动重判任务 | `POST /api/v1/teacher/submissions/139/judge-jobs/requeue` 返回 201，响应 job id=133、`triggerType=MANUAL_REJUDGE` | 随后详情页判题任务列表出现新增任务 | 已真实操作通过 | — |
| /teacher/submissions/139 | 教师 | 提交级重判按钮 | button | 点击重判→确认弹窗确认 | 先确认再创建提交级手动重判任务 | 弹窗标题“提交级重判”；确认后 `POST /api/v1/teacher/submissions/139/judge-jobs/requeue` 返回 201，响应 job id=135、`status=PENDING` | 随后 `GET /api/v1/teacher/submissions/139/judge-jobs` 返回 200，页面显示 5 个判题任务 | 已真实操作通过 | BUG-20260606-008 |
| /teacher/submissions/139 | 教师 | 答案重判按钮 | button | 点击“重判答案 E2E-mq1e6zib-89oubn-webide-real-flow-programming”→确认 | 按钮可访问名称包含目标题目，先确认再创建答案级手动重判任务 | 弹窗说明包含题目名称；确认后 `POST /api/v1/teacher/submission-answers/490/judge-jobs/requeue` 返回 201，响应 job id=136、`status=PENDING` | 随后 `GET /api/v1/teacher/submissions/139/judge-jobs` 返回 200，页面显示 5 个判题任务 | 已真实操作通过 | BUG-20260606-008 |
| /teacher/submissions/67 | 教师 | 保存批改按钮 | button | 输入分数→点击保存 | 批改保存成功 | Toast"人工批改已保存" | — | 已真实操作通过 | — |
| /teacher/submissions/67 | 教师 | 下载报告按钮 | button | 点击下载 | 报告文件下载 | 文件 judge-job-60-report.json 下载 | 文件存在 | 已真实操作通过 | — |

### 5.23 教师 - 成绩册

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/grading/gradebook | 教师 | 选择课程下拉框 | select | 选择"数据结构 2025 秋" | 选中成功 | 选中成功 | — | 已真实操作通过 | — |
| /teacher/grading/gradebook | 教师 | 查询按钮 | button | 点击查询 | 返回成绩数据 | 返回 10 页学生成绩 | — | 已真实操作通过 | — |
| /teacher/grading/gradebook | 教师 | 导出 Excel 按钮 | button | 点击导出 | CSV 文件下载 | 文件 gradebook-offering-1.csv 下载 | 文件存在 | 已真实操作通过 | — |
| /teacher/grading/gradebook?offeringId=1&assignmentId=414 | 教师 | 选择课程/教学班/作业筛选 | select | 打开页面并观察筛选条 | 筛选项宽度稳定，长作业标题可读，移动端不横向溢出 | 修复后桌面课程约 284px、教学班约 224px、作业约 368px，390px 视口四个筛选控件均为 292px 且 `documentWidth=390` | Playwright MCP DOM bbox 复核 | 已真实操作通过 | BUG-20260606-009 |
| /teacher/grading/gradebook?offeringId=1&assignmentId=414 | 教师 | 批量调分按钮 | button | 提交 ID / 答案 ID / 分数留空后点击 | 显示字段级错误且不发送调分请求 | 显示“请输入有效的提交 ID / 答案 ID / 调整分数”，三个字段均 `aria-invalid=true` | 未出现 `POST /api/v1/teacher/assignments/414/grades/batch-adjust` | 已真实操作通过 | BUG-20260606-010 |
| /teacher/grading/gradebook?offeringId=1&assignmentId=414 | 教师 | 批量调分按钮 | button/dialog | 输入提交 139、答案 490、分数 98、反馈后点击并确认 | 先确认再提交调分，成功后刷新成绩册和报表 | 弹窗说明“将调整提交 139 的答案 490 分数为 98。确定要继续吗？”；确认后调分成功 | `POST /api/v1/teacher/assignments/414/grades/batch-adjust` 返回 200，answer 490 `manualScore/finalScore=98`；随后 gradebook/report GET 200 | 已真实操作通过 | BUG-20260606-010, BUG-20260606-011 |
| /teacher/grading/gradebook?offeringId=1&assignmentId=414 | 教师 | 下载导入模板按钮 | button | 点击下载 | 下载当前作业导入模板 | 下载 `assignment-grades-414-template.csv` | `GET /api/v1/teacher/assignments/414/grades/import-template` 返回 200，`content-disposition` 指向模板文件名 | 已真实操作通过 | — |
| /teacher/grading/gradebook?offeringId=1&assignmentId=414 | 教师 | 成绩导入上传区 | file upload | 上传 CSV：提交 139、答案 490、分数 99、反馈 `MCP gradebook import 0606` | 导入成功并刷新成绩册和报表 | 上传区显示 `aubb-grade-import-414.csv`；导入接口成功 | `POST /api/v1/teacher/assignments/414/grades/import` 返回 200，`successCount=1/failureCount=0`；随后 gradebook/report GET 200；提交详情 `GET /api/v1/teacher/submissions/139` 显示 answer 490 `manualScore/finalScore=99`、反馈为导入文本 | 已真实操作通过 | BUG-20260606-011 |
| /teacher/grading/gradebook?offeringId=1&assignmentId=414 | 教师 | 发布成绩按钮 | button/dialog | 点击发布成绩并确认 | 先确认发布，学生可见后刷新成绩册和报表 | 弹窗提示“发布后学生即可查看该作业的成绩”；确认后发布成功 | `POST /api/v1/teacher/assignments/414/grades/publish` 返回 200，`initialPublication=true`；刷新后 gradebook summary `publishedCount=41`，assignment 414 `gradePublished=true` | 已真实操作通过 | BUG-20260606-011 |

### 5.24 教师 - 实验中心

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/labs | 教师 | 选择课程/教学班下拉框 | select | 选择课程和教学班 | 选中成功 | 选中成功，实验列表加载 | — | 已真实操作通过 | — |
| /teacher/labs | 教师 | 创建实验空提交 | button/input | 选择课程 A1 后点击创建实验，实验标题留空后点击创建 | 显示字段级错误且不发送创建请求 | 显示“请输入实验标题”，标题字段 `aria-invalid=true` 且关联 `lab-title-error` | 仅有列表 `GET`，未出现 `POST /api/v1/teacher/course-offerings/1/labs` | 已真实操作通过 | BUG-20260606-012 |
| /teacher/labs | 教师 | 创建实验按钮 | button/dialog | 填写 `MCP 教师实验回归 0606-0646` 后点击创建 | 创建成功并刷新当前列表 | `POST /api/v1/teacher/course-offerings/1/labs` 返回 201，列表显示新实验 | 随后 `GET /api/v1/teacher/course-offerings/1/labs?teachingClassId=1&page=1&pageSize=50` 返回 200 | 已真实操作通过 | — |
| /teacher/labs | 教师 | 编辑实验按钮 | button/dialog | 点击“编辑实验 MCP 教师实验回归 0606-0646”，先清空标题保存，再填写编辑标题保存 | 空标题显示字段级错误；有效编辑成功刷新 | 空标题显示“请输入实验标题”且未出现 `PUT`；有效编辑 `PUT /api/v1/teacher/labs/74` 返回 200，列表显示 `MCP 教师实验回归 0606-0646-编辑` | 编辑成功后当前列表 GET 返回 200 | 已真实操作通过 | BUG-20260606-012 |
| /teacher/labs | 教师 | 发布实验按钮 | button/dialog | 点击“发布实验 MCP 教师实验回归 0606-0646-编辑”并确认 | 先确认再发布，状态与按钮可用性刷新 | 确认弹窗说明包含实验标题；确认前无发布请求，确认后 `POST /api/v1/teacher/labs/74/publish` 返回 200；列表显示已发布，发布按钮禁用、关闭按钮启用 | 随后当前列表 GET 返回 200 | 已真实操作通过 | — |
| /teacher/labs | 教师 | 报告按钮 / 空态 | button/section | 点击新实验报告按钮 | 报告区域可见，空态清晰 | `GET /api/v1/teacher/labs/74/reports?page=1&pageSize=20` 返回 200，页面显示“暂无实验报告” | — | 已真实操作通过 | — |
| /teacher/labs | 教师 | 报告详情 / 评阅 / 发布评阅 | button/dialog | 打开 `MCP 实验回归 mq1bfyvc` 报告，查看详情，填写评语并保存、发布 | 报告行操作可区分学生；详情、保存评阅、发布评阅闭环 | 报告行按钮名称包含 `MCP实验学生mq1bfyvc`；`GET /api/v1/teacher/labs/63/reports` 和 `GET /api/v1/teacher/lab-reports/30` 返回 200；正文与 `README.md` 附件可见；`PUT /review` 与 `POST /publish` 均返回 200，报告状态变为已发布 | 报告列表刷新 GET 返回 200 | 已真实操作通过 | BUG-20260606-012 |
| /teacher/labs | 教师 | 移动端 390px | viewport | 设置 390x844 后检查页面宽度和主要控件名称 | 无横向溢出，筛选控件有可访问名称 | `documentWidth=390`，课程下拉名称“选择课程”，教学班下拉名称“教学班”，创建实验按钮可见；控制台错误 0 | — | 已真实操作通过 | BUG-20260606-012 |
| /teacher/labs | 教师 | 关闭按钮 | button | 点击关闭 | 实验关闭 | Toast"实验已关闭" | — | 已真实操作通过 | — |

### 5.25 教师 - 讨论管理（锁定/解锁）

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /teacher/courses/1/discussions | 教师 | 锁定讨论按钮 | button | 点击锁定 | 讨论锁定 | Toast"讨论状态已更新"，显示"已锁定"标签，按钮变为"解锁讨论" | 刷新后仍为锁定状态 | 已真实操作通过 | — |
| /teacher/courses/1/discussions | 教师 | 解锁讨论按钮 | button | 点击解锁 | 讨论解锁 | Toast"讨论状态已更新"，按钮变回"锁定讨论" | 刷新后仍为解锁状态 | 已真实操作通过 | — |

### 5.26 学生 - 作业任务

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /student/assignments | 学生 | 页面加载 | — | 打开页面 | 显示作业列表 | 多个作业（已发布/已关闭），含截止时间和状态 | — | 已真实操作通过 | — |
| /student/assignments | 学生 | 开始做题链接 | link | 点击进入 | 跳转作业详情 | 跳转到 /student/assignments/9 | — | 已真实操作通过 | — |
| /student/assignments/9 | 学生 | 页面加载 | — | 打开页面 | 显示作业详情和题目 | 显示 4 个题目（单选/简答/文件上传/编程），作业已过期 | — | 已真实操作通过 | — |
| /student/assignments/9 | 学生 | 打开 IDE 链接 | link | 点击打开 | 跳转编程工作区 | 跳转到 /student/assignments/9/workspace/23 | — | 已真实操作通过 | — |
| /student/assignments/9 | 学生 | 提交答案按钮 | button | — | — | 可见（disabled，作业已截止） | — | 只读/无副作用已验证 | — |
| /student/assignments/9/workspace/23 | 学生 | 页面加载 | — | 打开页面 | 显示编程工作区 | 显示工作区，但"无权访问此编程工作区"（403） | — | 已真实操作通过 | — |
| /student/assignments/9/workspace/23 | 学生 | 保存按钮 | button | — | — | 可见（disabled） | — | 只读/无副作用已验证 | — |
| /student/assignments/9/workspace/23 | 学生 | 重置按钮 | button | — | — | 可见（作业已过期，工作区 403） | — | 受阻未测（作业过期） | — |
| /student/assignments/9/workspace/23 | 学生 | 历史按钮 | button | — | — | 可见（作业已过期） | — | 受阻未测（作业过期） | — |
| /student/assignments/9/workspace/23 | 学生 | 运行自测按钮 | button | — | — | 可见（disabled） | — | 只读/无副作用已验证 | — |
| /student/assignments/9/workspace/23 | 学生 | 提交按钮 | button | — | — | 可见（作业已过期，工作区 403） | — | 受阻未测（作业过期） | — |
| /student/assignments/439 | 学生 | 结构化答题表单 | radio/checkbox/input/textarea/file/link/button | 临时学生打开未过期作业，填写单选 A、多选 A/B、填空 `-1`、Markdown 简答，上传 `assignment-402-requests.txt`，打开 IDE 后返回并提交 | 单选/多选/填空/简答/文件/编程 6 类答案一起提交成功 | `POST /api/v1/me/assignments/439/submission-artifacts` 返回 201，详情页恢复草稿；提交后跳转 `/student/submissions/148`，显示 `SUBMITTED`、附件和 6 个答案 | `POST /api/v1/me/assignments/439/submissions` 返回 201，请求体包含 question 1515-1520 全部答案、artifact id 86 和 `main.py`；响应 submission id=148，单选/多选/填空自动判分 5/8/7 | 已真实操作通过 | — |
| /student/assignments/439/workspace/1520 | 学生 | 保存 / 运行自测 | button | 打开编程题 IDE，保存模板 `main.py`，点击运行自测 | 工作区可访问、可保存、样例运行通过 | 页面显示 `main.py`、`Language: PYTHON3`、可编辑；运行结果显示“已完成 / 通过 / ACCEPTED”，stdout 为 `3` | `GET /workspace` 200，`PUT /workspace` 200，`POST /sample-runs` 201，`GET /sample-runs` 200 | 已真实操作通过 | — |
| /student/assignments/439/workspace/1520 | 学生 | 历史恢复按钮 | button/dialog | 打开历史版本，点击目标历史版本的恢复按钮 | 多个恢复按钮能区分目标版本，恢复后有明确反馈 | 修复后恢复按钮名称包含目标版本和保存类型，如 `恢复历史版本 v2 手动保存`；点击后显示“历史版本已恢复” | 真实后端 Playwright 辅助回归覆盖历史列表、恢复点击、后续保存/运行/提交链路；Playwright MCP 当前 `Transport closed` | 辅助回归通过，待 MCP 复核 | BUG-20260606-015 |
| /student/assignments/439/workspace/1520 | 学生 | 重置为模板确认 | button/alertdialog | 点击重置，先取消，再再次点击并确认 | 危险操作先确认，取消不生效，确认后重置为模板且可继续编辑 | 点击“重置”显示“重置为模板”确认弹窗；取消后弹窗关闭；确认后显示“已重置模板”，重新填写代码后仍可保存、运行自测并提交 | 真实后端 Playwright 辅助回归覆盖取消/确认两条路径；Playwright MCP 当前 `Transport closed` | 辅助回归通过，待 MCP 复核 | BUG-20260606-015 |
| /student/assignments | 学生 | 移动端作业卡片 | viewport/link | 390x844 视口刷新作业列表 | 无横向溢出，卡片纵向排布，状态和目标明确的开始做题入口可见 | `documentWidth=390`，首个卡片宽度 326；状态在移动端可见；链接名称为 `开始做题 <作业标题>`，控制台错误 0 | — | 已真实操作通过 | BUG-20260606-013 |

### 5.26 学生 - 实验项目

| 页面 | 角色 | 控件名称 | 控件类型 | 用户动作 | 预期结果 | 实际结果 | 持久化校验 | 状态 | 缺陷编号 |
|------|------|----------|----------|----------|----------|----------|------------|------|----------|
| /student/labs | 学生 | 页面加载 | — | 打开页面 | 显示实验列表 | 默认选中"数据结构 2025 秋 / A1"，可见本轮已发布实验 `MCP 实验回归 mq1bfyvc` | — | 已真实操作通过 | — |
| /student/labs | 学生 | 教学班选择下拉框 | select | — | — | 默认选中"数据结构 2025 秋 / A1" | — | 只读/无副作用已验证 | — |
| /student/labs | 学生 | 实验项目按钮 | button | 点击选择实验 | 启用报告区域 | 报告区域启用（textarea、上传、保存、提交） | — | 已真实操作通过 | — |
| /student/labs | 学生 | 实验报告输入框 | textarea | 输入报告内容 | 输入成功 | 输入成功 | — | 已真实操作通过 | — |
| /student/labs | 学生 | 保存草稿按钮 | button | 点击保存 | 保存成功 | `PUT /api/v1/me/labs/63/report` 返回 200，页面状态为"草稿" | 请求体包含 `submit:false`，随后 `GET /report` 返回 `DRAFT` 报告 id=30 | 已真实操作通过 | BUG-20260605-007 |
| /student/labs | 学生 | 选择文件按钮 | button | 选择 `README.md` 上传 | 附件上传成功并显示数量 | `POST /api/v1/me/labs/63/attachments` 返回 201，页面显示"已上传附件数：1" | 附件 id=30，文件名 `README.md` | 已真实操作通过 | — |
| /student/labs | 学生 | 正式提交按钮 | button | 点击并确认提交 | 报告正式提交 | `PUT /api/v1/me/labs/63/report` 返回 200，页面状态为"已提交" | 请求体包含 `attachmentIds:[30]`、`submit:true`，响应 `SUBMITTED` | 已真实操作通过 | — |

## 7. 主链路测试结果

| # | 链路名称 | 步骤 | 状态 | 证据 |
|---|----------|------|------|------|
| ML-1 | 管理员初始化 | 平台配置✅ 组织架构✅ 用户✅ 用户批量导入✅ 学期✅ 课程模板✅ 开课✅ 用户详情✅ | 部分通过 | 见 5.1-5.7 |
| ML-2 | 教师教学准备 | 公告✅ 讨论✅ 资源下载✅ 资源重命名✅ 资源空标题校验✅ 通知已读✅ 题库筛选✅ 题库新增自动刷新✅ 关闭作业✅ 资源上传✅ 资源删除✅ 讨论锁定✅ 讨论解锁✅ | 部分通过 | 见 5.10-5.25 |
| ML-3 | 教师创建作业 | 创建作业✅ 编辑作业✅ 发布作业✅ 关闭作业✅ 查看提交✅ 提交级重判✅ 答案重判✅ 人工批改✅ 下载报告✅ 导出成绩册✅ 批量调分✅ 导入成绩✅ 发布成绩✅ 关闭实验✅ | 部分通过 | 见 5.20-5.24 |
| ML-4 | 学生答题 | 作业列表✅ 作业详情✅ 结构化答题提交✅ 编程工作区保存/运行✅ 正式提交含编程答案✅ 实验报告✅ | 部分通过 | 见 5.25-5.26 |
| ML-5 | 评测批改 | 状态中文展示✅ 提交级重判✅ 答案重判✅ 人工批改✅ 批量调分✅ 导入成绩✅ 发布成绩✅ 下载报告✅ | 通过 | 见 5.22-5.23 |
| ML-6 | 学生查看成绩 | 选择课程✅ 导出成绩✅ | 部分通过 | 见 5.18 |
| ML-7 | 实验流程 | 教师创建✅ 编辑✅ 发布✅ 报告详情✅ 评阅✅ 发布评阅✅；学生保存草稿✅ 上传附件✅ 正式提交✅ | 通过 | 见 5.24、5.26 |
| ML-8 | 通知流转 | 教师通知已读✅ 学生通知已读✅ 学生创建讨论✅ 学生回复讨论✅ | 部分通过 | 见 5.15-5.19 |
| ML-9 | 审计权限 | 审计日志筛选✅ 权限诊断✅ 创建授权组✅ 添加成员✅；非法权限编码 / 无效模板错误态✅ | 通过 | 见 5.8-5.9 |

## 8. 页面级测试结果

（待补充）

## 9. 负例与权限测试结果

| # | 测试项 | 场景 | 预期结果 | 实际结果 | 状态 |
|---|--------|------|----------|----------|------|
| 1 | 错误密码登录 | 输入错误密码 | 提示"用户名或密码错误" | 显示"用户名或密码错误" | 已真实操作通过 |
| 2 | 空输入登录 | 不输入直接点登录 | 提示必填 | 留在登录页 | 已真实操作通过 |
| 3 | 未登录访问/ | 无 token 访问根路径 | 跳转登录页 | 跳转到 /login | 已真实操作通过 |
| 4 | 学生访问/admin | 学生登录后访问 | 跳转 unauthorized | 跳转到 /unauthorized | 已真实操作通过 |
| 5 | 学生访问/teacher | 学生登录后访问 | 跳转 unauthorized | 跳转到 /unauthorized | 已真实操作通过 |
| 6 | 未登录访问 API | 无 token 请求 API | 返回 401 | 返回 401 | 已真实操作通过 |
| 7 | 退出登录 | 点击退出 | 跳转登录页 | 跳转到 /login | 已真实操作通过 |
| 8 | 学期创建空提交 | `/admin/academic-terms` 新增弹窗留空提交 | 显示必填错误且不创建数据 | 显示 6 个字段错误，字段均标记 `aria-invalid=true` | 已真实操作通过 |
| 9 | 课程模板创建空提交 | `/admin/course-catalogs` 新增弹窗留空提交 | 显示必填错误且不创建数据 | 显示 4 个字段错误，字段均标记 `aria-invalid=true`，所属学院候选排除学校节点 | 已真实操作通过 |
| 10 | 公告发布 / 编辑空提交 | `/teacher/courses/1/announcements` 发布和编辑弹窗留空提交 | 显示字段级错误且不发送创建 / 更新请求 | 发布和编辑均显示 2 个字段错误，字段均标记 `aria-invalid=true`，未发送 `POST` / `PUT` 公告请求 | 已真实操作通过 |
| 11 | 讨论创建空提交 | `/teacher/courses/1/discussions` 创建弹窗留空提交 | 显示字段级错误且不发送创建请求 | 显示 2 个字段错误，字段均标记 `aria-invalid=true`，未发送 `POST` 讨论请求 | 已真实操作通过 |
| 12 | 成员添加负例 | `/teacher/courses/1/members` 添加成员弹窗留空或缺教学班提交 | 显示字段级错误且不发送添加请求 | 用户 ID / 教学班错误均可见，对应字段均标记 `aria-invalid=true`，未发送 `POST /members/batch` | 已真实操作通过 |
| 13 | 成绩册批量调分空提交 | `/teacher/grading/gradebook?offeringId=1&assignmentId=414` 留空提交 ID / 答案 ID / 分数后点击批量调分 | 显示字段级错误且不发送调分请求 | 三个字段错误均可见，字段均标记 `aria-invalid=true`，未发送 `POST /grades/batch-adjust` | 已真实操作通过 |

## 10. 响应式与可访问性结果

| 角色 | 视口 | 页面 | 结果 |
|------|------|------|------|
| 管理员 | 390x844 | /admin/course-offerings | ✅ 汉堡菜单可用，表格可滚动，表单可见，验证消息正确显示 |
| 管理员 | 桌面 | /admin/academic-terms | ✅ 新增学期弹窗有描述文本，空提交错误与 `aria-invalid` 状态正确显示 |
| 管理员 | 桌面 | /admin/course-catalogs | ✅ 列表开课单位可见，新增模板弹窗有描述文本，所属学院过滤和空提交错误状态正确 |
| 教师 | 桌面 | /teacher/courses/1/announcements | ✅ 发布 / 编辑公告弹窗有描述文本、可见字段标签，空提交错误与 `aria-invalid` 状态正确显示 |
| 教师 | 桌面 | /teacher/courses/1/discussions | ✅ 创建讨论弹窗有描述文本、空提交错误与 `aria-invalid` 状态正确显示；锁定 / 解锁按钮可访问名称包含讨论标题 |
| 教师 | 桌面 | /teacher/courses/1/members | ✅ 添加 / 导入 / 转班弹窗有描述文本；添加成员负例错误与 `aria-invalid` 状态正确显示；停用 / 恢复 / 转班按钮可访问名称包含成员姓名 |
| 教师 | 桌面 | /teacher/grading/gradebook | ✅ 筛选下拉宽度稳定，批量调分空提交显示字段级错误，批量调分和发布均有确认弹窗 |
| 教师 | 390x844 | /teacher/grading/gradebook | ✅ 筛选条按单列排列，课程 / 教学班 / 学生 ID / 作业控件宽度均为 292px，`documentWidth=390`，无横向溢出 |
| 管理员 | 390x844 | 汉堡菜单 | ✅ 点击打开/关闭正常，所有导航链接可见 |
| 教师 | 390x844 | /teacher | ✅ 页面加载成功 |
| 学生 | 390x844 | /student | ✅ 页面加载成功 |

## 11. 缺陷清单

| 缺陷编号 | 严重级别 | 页面 | 问题摘要 | 状态 |
|----------|----------|------|----------|------|
| BUG-20260605-001 | P2 | /admin/org-units | UI 创建 COLLEGE 类型节点失败（缺 parentId） | 已修复 |
| BUG-20260605-002 | P1 | /admin/course-offerings | UI 创建开课失败（无网络请求，缺必填字段提示） | 已修复 |
| BUG-20260605-003 | P3 | /admin/audit-logs | 审计日志筛选中文操作类型无结果（列表显示中文但筛选需英文） | 已修复 |
| BUG-20260605-004 | P2 | /admin/auth-explain | 权限诊断返回 403（PLATFORM 级别资源范围匹配错误） | 已修复 |
| BUG-20260605-005 | P3 | /admin/auth-explain | 创建授权组返回 404（模板不存在，需先创建模板） | 非缺陷，预期行为；有效模板 `audit-readonly` 已回归通过 |
| BUG-20260605-006 | P2 | /teacher/courses/1/question-bank | 编辑题目按钮点击无反应（无对话框弹出） | 已修复 |
| BUG-20260605-007 | P1 | /student/labs | 学生实验报告保存草稿失败（保存请求缺少 `submit:false`，后端返回 400 `Failed to read request`） | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260605-008 | P2 | /teacher/courses/1/question-bank | 分类管理按钮点击无反应（无对话框弹出） | 非缺陷，入口已清理 |
| BUG-20260605-009 | P3 | /admin/org-units | 子节点创建成功后根节点表单类型残留 COLLEGE | 已修复 |
| BUG-20260606-001 | P1 | /admin/users/[userId] | 用户详情页学籍/教籍资料只读，“保存学籍资料”不可完成真实编辑 | 已修复 |
| BUG-20260606-002 | P2 | /teacher/courses/[offeringId]/members | 添加成员成功后结果提示随弹窗关闭，用户看不到批量结果 | 已修复 |
| BUG-20260606-003 | P2 | /teacher/courses/1/question-bank | 新增题目成功后题库列表、分类、标签筛选未自动刷新 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-004 | P1 | /teacher/assignments/create, /teacher/assignments/[assignmentId]/edit | 引用题库题目创建 / 编辑作业时提交了题干、题型、配置等多余字段，后端返回 400 `ASSIGNMENT_QUESTION_BANK_REFERENCE_INVALID` | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-005 | P3 | /teacher/assignments | 作业列表接口未返回 `paper` 时总分列误显示 0，容易被误认为作业 0 分 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-006 | P2 | /teacher/submissions | 提交管理筛选区作业下拉框宽度被压缩，长作业标题不可读 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-007 | P3 | /teacher/submissions | 提交列表直接显示后端枚举 `SUBMITTED`，未映射为中文业务状态 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-008 | P2 | /teacher/submissions/[submissionId] | 详情页提交级重判 / 答案重判直接触发，缺少确认；答案重判按钮缺少目标题目标识 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-009 | P2 | /teacher/grading/gradebook | 成绩册筛选区教学班 / 作业下拉框宽度被压缩，长标题不可读；移动端作业下拉框曾横向溢出 | 已修复，2026-06-06 Playwright MCP 桌面与 390px 回归通过 |
| BUG-20260606-010 | P2 | /teacher/grading/gradebook | 批量调分空输入静默无反馈，合法调分缺少确认弹窗 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-011 | P2 | /teacher/grading/gradebook | 批量调分 / 导入 / 发布后缓存失效 key 不匹配，当前成绩册和报表可能不刷新 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-012 | P2 | /teacher/labs | 实验中心行操作 / 报告行操作按钮目标不可区分，创建 / 编辑实验空标题静默无反馈，弹窗缺少描述 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-013 | P2 | /student/assignments | 移动端作业卡片仍左右排布导致标题被压缩，所有“开始做题”链接名称相同且无法区分目标作业 | 已修复，2026-06-06 Playwright MCP 回归通过 |
| BUG-20260606-014 | P2 | /student/notifications | “全部已读”接口成功且未读徽章清零后，分页通知列表未失效刷新，行内“标记已读”仍保留 | 已修复，2026-06-06 真实浏览器补充回归通过；Playwright MCP 当前 `Transport closed`，已记录工具降级 |
| BUG-20260606-015 | P3 | /student/assignments/[assignmentId]/workspace/[questionId] | 历史版本列表多个“恢复”按钮目标不可区分，重置确认路径缺少回归记录 | 已修复，2026-06-06 真实后端 Playwright 辅助回归通过；Playwright MCP 当前 `Transport closed` |
| BUG-20260606-016 | P2 | /student/courses/[classId] | 学生越权访问非所属教学班时虽显示 403 权限错误，但讨论创建表单仍可见 | 已修复，2026-06-06 真实后端 Playwright 辅助回归通过；Playwright MCP 当前 `Transport closed` |

## 12. 修复计划

- Playwright MCP 恢复后，优先复核近期因 `Transport closed` 降级为辅助证据的通知、WebIDE、用户导入、组织架构和课程越权批次。
- 继续按小批次补齐移动端视口覆盖，优先选择学生长链路和教师内容管理中尚未做 390px 回归的页面。
- 对报告中历史固定 ID 的学生课程 / 工作区记录做一次数据口径整理，避免旧测试数据与动态 fixture 混用造成误读。

## 13. 未覆盖项与风险

- 教师：题库"编辑题目"按钮已修复并通过真实浏览器复核
- 教师：提交管理列表级重判、详情级提交重判和答案重判已修复并通过真实浏览器复核
- 教师：成绩册"批量调整"、"导入"、"发布"已修复并通过真实浏览器复核
- 教师：实验"创建实验"、"编辑"、"发布"、"报告查看"、"评阅发布"已修复并通过真实浏览器复核
- 学生：作业任务（/student/assignments）结构化答题/提交已在 5.26 用 Playwright MCP 回归验证
- 学生：编程工作区保存/运行和正式提交编程答案已在 5.26 用 Playwright MCP 回归验证；重置/历史恢复已用真实后端 Playwright 辅助回归补测，MCP 待恢复后复核
- 学生：实验项目（/student/labs）上传附件/提交报告已在 5.26 用 Playwright MCP 回归验证；教师评阅发布已在 5.24 补测
- 学生：通知"全部已读"已补测并修复列表刷新问题
- 学生：跨角色权限负例（访问非所属教学班课程内容）已补测并修复讨论创建入口暴露问题；MCP 待恢复后复核
- 移动端视口仍仅局部覆盖；本轮补充 `/teacher/labs` 与 `/student/assignments` 390px 无横向溢出和控件名称检查

## 14. 命令与日志证据

| 命令 | 结果 |
|------|------|
| just healthcheck | 全部通过（backend 18080, frontend 3000, Docker 依赖） |
| just status | server/main clean；web/main 与 docs/main dirty（前端整改、测试和报告更新） |
| just healthcheck-strict | 通过；严格 E2E 环境变量、后端 18080、前端 3000、后端 readiness/OpenAPI、前端登录页均可用 |
| just verify | 2026-06-06 09:43 CST 通过；server 320 测试 0 失败 / 0 错误，web lint/typecheck 通过，docs build 通过（仅 VitePress chunk size warning） |
| just e2e-real | 2026-06-06 05:58 CST 复跑通过，38 个真实后端 Playwright E2E 全部通过，耗时 3.3 分钟 |
| cd web && npm run lint | 通过 |
| cd web && npm run typecheck | 通过 |
| cd web && npm test -- src/tests/unit/admin/audit-logs-page.test.tsx | 1 文件 / 2 测试通过 |
| cd docs && npm run docs:build | 通过；VitePress 输出 chunk size warning |
| Playwright MCP 审计日志行操作回归 | 管理员真实会话 `/admin/audit-logs`，`GET /api/v1/admin/audit-logs?page=1&pageSize=20` 返回 200；复制按钮具备“复制请求 ID <短 ID>”名称并显示“Request ID 已复制”；详情按钮具备“查看日志详情 <操作> <短 ID>”名称并显示“日志元数据”；复制 JSON 后显示“JSON 已复制” |
| cd web && npm test -- --run src/tests/unit/admin/user-detail-page.test.tsx | 1 文件 / 2 测试通过 |
| Playwright MCP 下载验证 | e2e-fullrun-ml2-resource.txt (41B), gradebook-me-offering-1.csv |
| Playwright MCP 用户详情回归 | 管理员真实会话 `/admin/users/621` 编辑学籍资料，`PUT /api/v1/admin/users/621/profile` 返回 200；强制下线确认后 `POST /api/v1/admin/users/621/sessions/revoke` 返回 204 |
| Playwright MCP 成员添加成功反馈回归 | 教师真实会话 `/teacher/courses/1/members` 添加用户 621 为整课助教，弹窗显示“添加成功 1 人，失败 0 人。”，`POST /api/v1/teacher/course-offerings/1/members/batch` 返回 200 |
| npm test -- src/tests/unit/course/teacher-announcements-page.test.tsx | 1 文件 / 2 测试通过 |
| npm test -- src/tests/unit/course/teacher-discussions-page.test.tsx | 1 文件 / 2 测试通过 |
| npm test -- 公告 / 讨论与已整改相关单测集合 | 9 文件 / 15 测试通过 |
| 本地 Playwright 公告负例脚本 | 发布 / 编辑空提交均显示 2 条错误，`POST` / `PUT` 公告请求数为 0，Dialog 警告数为 0，临时种子残留数为 0 |
| 本地 Playwright 讨论负例脚本 | 创建空提交显示 2 条错误，`POST` 讨论请求数为 0，Dialog 警告数为 0，20 个锁定 / 解锁按钮名称包含讨论标题 |
| Playwright MCP 判题环境逐按钮回归 | 教师真实会话完成 Go 1.22 筛选、空新增错误、创建、编辑、归档、包含归档复查；对应 `GET` / `POST` / `PUT` / archive 请求为 200/201 |
| Playwright MCP 审计日志中文筛选回归 | 管理员真实会话选择“登录成功”操作类型，下拉值提交 `LOGIN_SUCCESS`，`GET /api/v1/admin/audit-logs?action=LOGIN_SUCCESS&page=1&pageSize=20` 返回 200，表格显示“登录成功”记录 |
| Playwright MCP 权限解释回归 | 管理员真实会话完成权限允许 / 拒绝 / 非法编码错误态、有效模板创建授权组、添加成员、无效模板 404 预期错误；`/admin/auth/explain` 200/200/400，`/admin/auth/groups` 201/404，`/admin/auth/groups/1/members` 201 |
| Playwright MCP 题库新增自动刷新回归 | 教师真实会话创建 `MCP-QUESTION-0606-0402`，`POST /api/v1/teacher/course-offerings/1/question-bank/questions` 返回 201，随后自动拉取 questions/categories/tags，当前列表显示新题且标签筛选出现 `autorefresh` |
| npm test -- src/tests/unit/api/mappers.contract.test.ts src/tests/unit/assignment/assignment-form.test.ts | 2 文件 / 10 测试通过 |
| Playwright MCP 作业创建 / 编辑 / 发布回归 | 教师真实会话先复现题库引用作业创建 400 `ASSIGNMENT_QUESTION_BANK_REFERENCE_INVALID`；修复后创建 `MCP 作业回归 0606-0413` id=402 成功，`POST /api/v1/teacher/course-offerings/1/assignments` 返回 201；编辑标题后 `PUT /api/v1/teacher/assignments/402` 返回 200；确认发布后 `POST /api/v1/teacher/assignments/402/publish` 返回 200，列表显示已发布，发布按钮禁用、关闭按钮启用 |
| npm test -- src/tests/unit/api/mappers.contract.test.ts src/tests/unit/submission/teacher-submission-detail-page.test.tsx | 2 文件 / 9 测试通过 |
| Playwright MCP 提交管理列表回归 | 教师真实会话 `/teacher/submissions?offeringId=1&assignmentId=414`，课程下拉约 280px、作业下拉约 492px；提交 `139` 状态显示 `已提交`；点击“重新判题提交 139”并确认后 `POST /api/v1/teacher/submissions/139/judge-jobs/requeue` 返回 201 |
| Playwright MCP 提交详情重判回归 | 教师真实会话 `/teacher/submissions/139`，点击“提交级重判”先出现确认弹窗，确认后 `POST /api/v1/teacher/submissions/139/judge-jobs/requeue` 返回 201，job id=135；答案按钮可访问名称为“重判答案 E2E-mq1e6zib-89oubn-webide-real-flow-programming”，确认后 `POST /api/v1/teacher/submission-answers/490/judge-jobs/requeue` 返回 201，job id=136；随后 `GET /api/v1/teacher/submissions/139/judge-jobs` 返回 200，页面显示 5 个判题任务 |
| npm test -- src/tests/unit/grading/teacher-gradebook-page.test.tsx | 1 文件 / 2 测试通过 |
| Playwright MCP 成绩册调分/导入/发布回归 | 教师真实会话 `/teacher/grading/gradebook?offeringId=1&assignmentId=414`，筛选区桌面课程约 284px、教学班约 224px、作业约 368px；390px 视口四个筛选控件宽度均为 292px 且无横向溢出；空批量调分显示 3 个字段错误且未发送调分请求；确认批量调分前未发送请求，确认后 `POST /api/v1/teacher/assignments/414/grades/batch-adjust` 返回 200，随后 gradebook/report GET 200；历史补充验证：下载模板返回 `assignment-grades-414-template.csv`；CSV 导入返回 `successCount=1/failureCount=0` 并刷新；确认发布后 `POST /api/v1/teacher/assignments/414/grades/publish` 返回 200，`initialPublication=true`，刷新后 assignment 414 `gradePublished=true` |
| npm test -- src/tests/unit/lab/teacher-labs-page.test.tsx | 1 文件 / 3 测试通过 |
| Playwright MCP 教师实验中心回归 | 教师真实会话 `/teacher/labs` 选择课程 1 / A1；空创建和空编辑均显示“请输入实验标题”、标题字段 `aria-invalid=true` 且未发送创建 / 更新请求；创建 `MCP 教师实验回归 0606-0646` 返回 201，编辑 lab 74 返回 200；发布前先出现包含实验标题的确认弹窗，确认后 `POST /api/v1/teacher/labs/74/publish` 返回 200，列表显示已发布、发布按钮禁用、关闭按钮启用；报告空态 `GET /teacher/labs/74/reports` 返回 200 并显示“暂无实验报告”；既有报告 `MCP 实验回归 mq1bfyvc` 的详情、附件、保存评阅和发布评阅通过，`GET /teacher/labs/63/reports`、`GET /teacher/lab-reports/30`、`PUT /review`、`POST /publish` 均返回 200；390px 视口 `documentWidth=390`，控制台错误 0 |
| npm test -- src/tests/unit/assignment/student-assignments-page.test.tsx | 1 文件 / 1 测试通过 |
| Playwright MCP 学生作业移动端回归 | 学生真实会话 `/student/assignments`，390x844 视口 `documentWidth=390` / `bodyWidth=390`，`GET /api/v1/me/assignments` 返回 200，控制台错误 0；前三张作业卡片宽度 326px，类名包含 `flex-col` / `sm:flex-row`；“开始做题”链接名称分别包含对应作业标题并指向各自作业详情 |
| npm test -- src/tests/unit/api/query-keys.contract.test.ts | RED：新增通知 inbox 前缀契约时失败于 `["notification","inbox", undefined]`；修复后 1 文件 / 5 测试通过 |
| 真实浏览器学生通知全部已读补充回归 | Playwright MCP 当前返回 `Transport closed`，本轮降级使用 Codex in-app Browser 操作真实本地页面；学生真实会话 `/student/notifications` 中临时实验 `MCP 通知全部已读回归 mq1lx8tk` 生成 1 条未读通知，点击“全部已读”前行内“标记已读”按钮数量为 1，点击后为 0，顶部未读徽标消失；后端只读校验目标通知 `id=991`、`read=true`、`unreadCount=0`、`firstUnreadId=null`；浏览器控制台 error 数 0 |
| npm test -- src/tests/unit/submission/programming-workspace-page.test.tsx | RED：新增历史恢复按钮目标命名单测时失败，页面仅暴露重复的“恢复”按钮；修复后 1 文件 / 1 测试通过 |
| 真实后端 Playwright 学生 WebIDE 辅助回归 | Playwright MCP 当前返回 `Transport closed`；本轮降级使用本地 Playwright 真实后端用例补充验证。学生 WebIDE 完成编辑/保存、历史版本目标命名与恢复、重置取消与确认、重置后重新保存、运行自测、正式提交；`webide-real-flow.spec.ts` chromium 项目 1 个用例通过 |
| 真实后端 Playwright 管理员用户导入辅助回归 | Playwright MCP 当前返回 `Transport closed`；本轮降级使用本地 Playwright 真实后端用例补充验证。管理员真实会话 `/admin/users` 点击“批量导入”打开文件选择器，上传重复用户名 CSV 后 `POST /api/v1/admin/users/import` 返回 200，响应 `total=1/success=0/failed=1`，页面展示“导入 1 行，成功 0 行，失败 1 行。”和第 2 行错误；`admin-users-real-flow.spec.ts` chromium 项目 1 个用例通过 |
| 真实后端 Playwright 管理员组织架构辅助回归 | Playwright MCP 当前返回 `Transport closed`；本轮降级使用本地 Playwright 真实后端用例补充验证。管理员真实会话 `/admin/org-units` 从学校根节点点击“新增子节点”，Dialog 标题为“在 [学校名] 下新增子节点”，节点类型默认 `COLLEGE`，填写学院名称/编码后 `POST /api/v1/admin/org-units` 返回 201，树中显示新学院；`admin-org-units-real-flow.spec.ts` chromium 项目 1 个用例通过 |
| 真实后端 Playwright 学生课程越权辅助回归 | Playwright MCP 当前返回 `Transport closed`；本轮降级使用本地 Playwright 真实后端用例补充验证。动态学生访问非所属教学班课程页时，公告、资源、讨论 API 均返回 403，页面显示三处权限错误并隐藏讨论标题输入框和“创建讨论”按钮；`student-course-permission-real-flow.spec.ts` chromium 项目 RED 失败于按钮仍可见，修复后 1 个用例通过 |
