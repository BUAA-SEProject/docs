import { defineConfig } from 'vitepress';

import { buildNav, buildSidebar } from './navigation';

export default defineConfig({
  lang: 'zh-CN',
  title: '在线教学与实训平台文档中心',
  description: '在线教学与实训平台项目文档，使用 VitePress 构建并发布到 GitHub Pages。',
  base: '/',
  cleanUrls: true,
  lastUpdated: true,
  srcExclude: ['README.md', 'SUMMARY.md'],
  themeConfig: {
    nav: buildNav(),
    sidebar: buildSidebar(),
    search: {
      provider: 'local',
    },
    outline: {
      level: [2, 3],
      label: '本页导航',
    },
    docFooter: {
      prev: '上一页',
      next: '下一页',
    },
    editLink: {
      pattern: 'https://github.com/BUAA-SEProject/docs/edit/main/:path',
      text: '在 GitHub 上编辑此页',
    },
    lastUpdated: {
      text: '最后更新于',
    },
    socialLinks: [
      {
        icon: 'github',
        link: 'https://github.com/BUAA-SEProject/docs',
      },
    ],
  },
});
