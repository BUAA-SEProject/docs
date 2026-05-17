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
- **Contextual Sidebar (宽度 240px)**: 针对当前所选模块的二级导航。
- **Content Area**: 位于顶部和侧边导航包裹中，最大宽度限制在 `1440px`。

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

### 2.6 响应式断点控制
- **Mobile (Base)**: < 768px。
- **Tablet (md)**: 768px - 1280px。
- **Desktop (xl)**: > 1280px。

## 3. 组件准则 (Component Guidelines)

### 3.1 按钮 (Buttons)
- 采用更硬朗的微圆角（6px），高度不低于 `44px`。
- 强化边框感，使用 `1px` 实线描边增强几何存在感。

### 3.2 卡片 (Cards)
- 采用 `rounded-lg` (8px) 配合极细边框 `1px border-slate-200`。
- 阴影应更加内敛，仅在悬浮时通过微小的位移产生立体感。

### 3.3 数据展示
- 图表配合活力蓝和活力绿。

### 3.4 完整交互状态机
- **聚焦 (Focus Visible)**: 使用 `ring-2 ring-primary ring-offset-2`。
- **禁用 (Disabled)**: 透明度 `opacity-40`。
- **加载 (Loading)**: 必须显示 `animate-pulse` 骨架屏。

## 4. 技术实现
- **Framework**: Next.js 16 (App Router).
- **Styling**: Tailwind CSS v4 (CSS variables in `@theme`).
- **Icons**: Lucide React (保持统一的 1.5px 描边宽度)。
- **Animations**: CSS transitions (150ms - 300ms, ease-in-out)。
