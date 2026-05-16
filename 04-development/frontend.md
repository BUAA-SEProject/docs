# 前端文档

## 1. 当前技术基线

- 框架：Next.js 16 (App Router)
- 语言：TypeScript
- UI：React 19、Tailwind CSS 4、shadcn/ui
- 状态管理：Zustand（全局状态）、TanStack Query（服务端状态）
- HTTP 客户端：Axios
- 在线编辑器：Monaco Editor
- 终端：xterm.js

## 2. 目录结构

```text
web/src/
  app/           # Next.js 页面与路由（App Router）
  features/      # 业务域逻辑（API, Hooks, Components, Models）
  shared/        # 共享基础能力（Client, UI, Utils, Config）
  tests/         # 测试用例（Unit, Integration, E2E）
```

## 3. 页面信息架构

| 角色 | 一级导航 | 核心页面 |
| --- | --- | --- |
| 学员 | 我的学习 | 我的课程、公告、资源、讨论、作业、提交、IDE、成绩、实验、通知 |
| 教师 | 我的教学 | 我的课程、班级、公告、资源、讨论、作业、提交、评测、成绩、实验、通知 |
| 助教 | 协助教学 | 我的课程、成员范围、提交查看、班级成绩册、通知 |
| 管理员 | 平台治理 | 平台配置、组织树、用户管理、审计日志、学期、课程目录、开课 |

## 4. 路由组织

- `app/(public)/*`：登录、无权限、系统维护页
- `app/(student)/*`：学员门户
- `app/(teacher)/*`：教师与助教门户
- `app/(admin)/*`：平台治理门户

## 5. 状态管理

### 5.1 Zustand Store

| Store | 字段 |
| --- | --- |
| `authStore` | accessToken、refreshToken、currentUser、initialized |
| `notificationStore` | 未读数、通知列表 |

### 5.2 TanStack Query

按业务域拆分 query key：

- `auth`：当前用户信息
- `platform`：平台配置
- `users`：用户列表与详情
- `courses`：课程列表与详情
- `courseContent`：公告、资源、讨论
- `assignments`：作业列表与详情
- `submissions`：提交列表与详情
- `workspace`：编程工作区快照
- `judge`：评测任务与报告
- `grading`：批改、成绩册
- `labs`：实验与实验报告
- `notifications`：通知列表与未读数

缓存策略：

- 列表页：以分页参数作为 query key
- 详情页：以实体 `id` 作为 query key
- 成功变更后优先失效相关列表，再局部回写详情

## 6. 前后端联调约定

- 所有请求通过统一 `apiClient`（Axios）发出。
- access token 统一走 `Authorization: Bearer <token>`。
- refresh token 由统一 auth client 管理，不暴露给业务模块。
- 任意业务接口返回 `401` 时，先尝试一次 refresh；refresh 失败则清空本地会话并跳回登录页。
- 统一拦截 `401`、`403`、`429` 和系统错误。
- 表格分页统一使用 `page`、`pageSize`、`total`。
- 时间字段统一以 ISO 8601 字符串返回，前端本地格式化展示。
- 运行结果与正式评测结果使用不同接口和不同状态枚举，不混用组件状态。

## 7. 认证模型

- 登录：`POST /api/v1/auth/login`
- 当前用户：`GET /api/v1/auth/me`（登录后初始化用户与路由权限的唯一事实来源）
- 刷新 access token：`POST /api/v1/auth/refresh`
- 登出当前会话：`POST /api/v1/auth/logout`
- 主动撤销 refresh token：`POST /api/v1/auth/revoke`

## 8. 关键页面设计

### 8.1 任务详情页

- 顶部：任务标题、截止时间、状态标签、剩余次数。
- 中部：Markdown 任务说明、附件下载、样例输入输出、支持语言说明。
- 底部：进入在线 IDE 按钮、历史提交列表、当前评测结果摘要。

### 8.2 在线 IDE 页

- 左侧：文件树、文件操作按钮、语言切换。
- 中部：Monaco 编辑器、多标签切换、未保存状态提示。
- 下方：运行控制台、输入面板、最近运行记录。
- 右侧：任务说明摘要、样例、正式提交按钮、提交规则提示。

### 8.3 提交详情页

- 左栏：代码快照、文件列表、提交元信息。
- 右栏：评测状态、测试点结果、错误摘要、人工评分区。

## 9. 交互规范

- 所有异步写操作必须显示进行中状态。
- 工作区编辑采用防抖自动保存，并在保存失败时展示显式警告。
- "运行代码"与"正式提交"按钮在颜色、文案和确认流程上必须明显区分。
- 对发布、撤回、重新评测等操作显示二次确认。
- 页面必须显式区分空态、加载态、异常态和无权限态。
- 学员侧错误提示应面向操作结果，教师侧可显示更细的业务上下文。

## 10. 验证命令

- Lint：`npm run lint`
- 类型检查：`npm run typecheck`
- 单元测试：`npm test`
- 构建：`npm run build`
- E2E 测试：`npm run test:e2e`
