---
title: "前端设计规范"
section: "04-development"
status: current
---
# 前端设计规范

## 1. 核心设计理念 (Core Philosophy)
AUBB 平台旨在提供一个**专业、严谨、高效**的在线教学环境。
- **专业 (Professional)**：减少装饰性元素，强调内容展示。
- **严谨 (Rigorous)**：采用硬朗的几何线条，收紧圆角，体现学术氛围。
- **高效 (Efficient)**：优化信息架构，确保核心操作路径最短。

## 2. 视觉系统 (Visual System)

### 2.1 色彩规范 (Color Tokens - Tailwind v4 OKLCH)
基于 **Academic Blue** 风格定义：
- **Primary (品牌蓝)**: `oklch(55% 0.22 260)` (#2563EB) - 用于主按钮、激活状态、顶部导航。
- **Success (活力绿)**: `oklch(75% 0.18 160)` (#34D399) - 用于完成状态、及格、提交成功。
- **Background (背景色)**: `oklch(98% 0.01 240)` (#F8FAFC) - 系统底色，柔和不刺眼。
- **Surface (容器色)**: `oklch(100% 0 0)` (#FFFFFF) - 卡片、面板、侧边栏容器。
- **Foreground (文字主色)**: `oklch(25% 0.05 260)` (#0F172A) - 核心正文。
- **Muted (辅助色)**: `oklch(60% 0.03 260)` (#64748B) - 辅助信息、面包屑。

### 2.2 布局结构 (Layout Architecture)
采用 **Hybrid Navigation (混合导航)**：
- **Global Topbar (高度 64px)**: 包含 Logo、全局搜索、个人中心、系统通知及一级模块切换。
- **Contextual Sidebar (展开宽度 240px，收起宽度 56px)**: 针对当前所选模块的二级导航，必须支持收起 / 展开，收起时保留图标与 tooltip。
- **Content Area**: 位于顶部和侧边导航包裹中，最大宽度限制在 `1440px`。
- **Page Toolbar**: 页面级主操作、筛选、导出、刷新、返回等操作优先放在内容区顶部工具栏；顶栏只承载全局搜索、通知、身份切换和当前页面必要的全局命令。
- **Multi-level Navigation**: 课程详情、成员、作业、题库、判题环境、成绩等上下文页面优先使用二级侧栏或页内 tabs；三级以下内容使用下拉菜单或分组列表收敛，不堆叠多层卡片。

### 2.3 间距与密度 (Spacing & Density)
遵循 **标准学术型 (Academic Professional)** 原则：
- **基础步进**: `8px` (1rem = 16px)。
- **页面内边距 (Container Padding)**: `32px` (p-8)。
- **组件内边距 (Component Padding)**: `24px` (p-6)。
- **卡片间距 (Gap)**: `24px` (gap-6)。
- **圆角 (Border Radius)**: `6px` (rounded-md) - 赋予界面稳重、严谨的学术感。关键容器如卡片使用 `8px` (rounded-lg)。

### 2.4 字体排印规范 (Typography Specifications)
- **字体族 (Font Family)**:
  - **英数**: `'Inter'`, `system-ui`, `sans-serif`。
  - **中**: `'PingFang SC'`, `'Hiragino Sans GB'`, `'Microsoft YaHei'`, `sans-serif`。
- **字号与行高阶梯 (Scale & Line Height)**:
  - **H1 (Page Title)**: `text-3xl` (30px) / `leading-tight` (1.2)。
  - **H2 (Section)**: `text-xl` (20px) / `leading-snug` (1.3)。
  - **Body (Primary)**: `text-base` (16px) / `leading-relaxed` (1.625)。
- **字重限制 (Font Weight)**:
  - **Regular (400)**: 用于所有正文。
  - **Semibold (600)**: 用于标题、按钮及强调。

### 2.5 暗黑模式色值映射
基于 Tailwind v4 原生 CSS 变量实现。

### 2.6 桌面端体验基准
- **主设计视口**：1440x900 及以上，优先保障教师、管理员在桌面端进行表格筛选、批量操作、详情查看和长链路录入的效率。
- **最低桌面验收视口**：1280x800；关键页面在该尺寸下应保持导航、筛选区、主操作、行操作和主要数据列可见且不互相遮挡。
- **非目标范围**：本阶段不要求移动端、平板端或 390px/375px 小屏专项适配；小屏问题不作为验收阻塞，除非同一布局问题同时影响桌面端核心流程。
- **桌面优先策略**：优先使用稳定的表格宽度、双栏或多栏信息布局、可扫描的筛选条和明确的行操作；不要为了小屏堆叠而牺牲桌面端信息密度。

### 2.7 体验参考与信息架构
- **工作台参考**：整体体验参考 VS Code / GitLab Web IDE 的 workbench、Ant Design Pro 的后台信息架构、Carbon / Atlassian 的数据密集型表格与详情页组织方式。
- **页面目标**：每个页面进入后必须直接呈现当前用户最可能执行的核心工作，不做营销式英雄区，不用大面积说明文字替代真实操作入口。
- **低嵌套原则**：页面 section 不能被层层卡片包裹；列表、表单、详情、抽屉、弹窗各自承担清晰职责。需要强调的信息使用标题、分隔、密度和状态色，而不是把卡片套进卡片。
- **上下文命令**：顶栏、页面工具栏、行操作和空态按钮的职责必须分离。全局命令放顶栏，页面批量操作放页面工具栏，单条数据命令放行操作。
- **多身份切换**：同一用户可能同时拥有学生、教师、助教、管理员身份。前端应提供工作区切换和记忆上次选择的机制，不应只按最高权限强制落到管理员首页。

### 2.8 Markdown 内容规范
- 作业题目描述、实验内容、课程公告、资源说明等说明性正文应支持 Markdown。
- Markdown 渲染必须具备清晰的标题层级、列表、引用、表格、代码块、行内代码、链接和附件引用样式。
- Markdown 正文应在教学内容区域以阅读密度展示，不放入窄卡片；宽度建议控制在 `72ch` 到 `88ch`，代码块和表格可横向滚动。

## 3. 组件准则 (Component Guidelines)

### 3.1 按钮 (Buttons)
- 采用更硬朗的微圆角（6px），常规桌面按钮高度建议为 `36px` - `40px`，主操作按钮可使用 `40px` 保持可点击性与页面密度平衡。
- 强化边框感，使用 `1px` 实线描边增强几何存在感。

### 3.2 卡片 (Cards)
- 采用 `rounded-lg` (8px) 配合极细边框 `1px border-slate-200`。
- 阴影应更加内敛，仅在悬浮时通过微小的位移产生立体感。

### 3.3 数据展示
- 图表配合活力蓝和活力绿。
- 表格默认支持列宽稳定、分页、排序、筛选、空态、加载态、错误态和行级权限裁剪。
- 详情页应优先使用摘要栏 + 分区内容 + 关联列表的结构，避免让用户在多层折叠面板中寻找主要信息。

### 3.4 完整交互状态机
- **聚焦 (Focus Visible)**: 使用 `ring-2 ring-primary ring-offset-2`。
- **禁用 (Disabled)**: 透明度 `opacity-40`。
- **加载 (Loading)**: 必须显示 `animate-pulse` 骨架屏。
- **权限不足 (Forbidden)**: 后端返回 403 时必须在页面或操作位置显示明确原因和下一步建议，不能只在控制台报错。
- **写操作失败 (Mutation Error)**: 表单、文件操作、IDE 保存和批量操作失败时必须回滚不一致的乐观状态，或明确标记本地状态未同步。

### 3.5 WebIDE 工作台
- WebIDE 采用 VS Code / GitLab Web IDE 风格：文件树、编辑器、多标签、运行结果、版本记录和状态栏稳定布局。
- WebIDE 不提供终端；学生只能通过运行按钮、标准输入框、样例选择和运行结果面板与程序交互。
- WebIDE 内“提交”语义等同于保存当前编程题并返回作业界面；整份结构化作业的正式提交只能在作业详情页完成。
- 禁用多文件时必须隐藏或禁用新建文件 / 目录入口；后端拒绝文件操作时前端必须回滚本地文件树并显示错误。

## 4. 技术实现
- **Framework**: Next.js 16 (App Router).
- **Styling**: Tailwind CSS v4 (CSS variables in `@theme`).
- **Icons**: Lucide React (保持统一的 1.5px 描边宽度)。
- **Animations**: CSS transitions (150ms - 300ms, ease-in-out)。
