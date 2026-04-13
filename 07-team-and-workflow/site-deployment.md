# 站点发布说明

## 站点技术方案

当前文档站使用 VitePress 构建，源码直接维护在本仓库的 Markdown 文件中。

关键约定：

- 仓库根目录的 Markdown 页面作为站点内容源
- `.vitepress/config.mts` 负责站点配置
- `SUMMARY.md` 作为导航目录来源，顶栏和侧边栏会基于它自动生成
- 推送到 `main` 分支后，GitHub Actions 会自动构建并发布到 GitHub Pages

## 本地开发

首次运行：

```bash
npm install
```

启动本地预览：

```bash
npm run docs:dev
```

构建生产版本：

```bash
npm run docs:build
```

构建产物输出到 `.vitepress/dist`。

## 发布流程

1. 在功能分支修改 Markdown 或站点配置
2. 同步更新 `SUMMARY.md`，确保导航包含新增页面
3. 在本地执行 `npm run docs:build`
4. 合并或推送到 `main`
5. GitHub Actions 自动构建并部署到 GitHub Pages

## GitHub Pages 工作流

仓库内已提供 `.github/workflows/deploy-pages.yml`，采用 GitHub 官方 Pages Action：

- `push` 到 `main` 时自动触发
- 使用 `npm ci` 安装依赖
- 执行 `npm run docs:build`
- 上传 `.vitepress/dist`
- 发布到 GitHub Pages

## 维护建议

- 修改目录结构后优先检查 `SUMMARY.md`
- 若仓库名发生变化，需要同步更新 `.vitepress/config.mts` 中的 `base`
- 若切换默认分支，需要同步更新 Pages 工作流中的触发分支
