import { readFileSync } from 'node:fs';

import type { DefaultTheme } from 'vitepress';

type SummaryNode = {
  text: string;
  link: string;
  items: SummaryNode[];
};

const summaryContent = readFileSync(new URL('../SUMMARY.md', import.meta.url), 'utf8');

const summaryNodes = parseSummary(summaryContent);

export function buildNav(): DefaultTheme.NavItem[] {
  return summaryNodes.slice(1).map((node) => ({
    text: node.text,
    link: node.link,
  }));
}

export function buildSidebar(): DefaultTheme.SidebarItem[] {
  return summaryNodes.slice(1).map(toSidebarItem);
}

function parseSummary(markdown: string): SummaryNode[] {
  const root: SummaryNode[] = [];
  const stack: SummaryNode[] = [];

  for (const line of markdown.split(/\r?\n/)) {
    const match = line.match(/^(\s*)\* \[(.*)\]\(([^)]+)\)\s*$/);

    if (!match) {
      continue;
    }

    const [, indent, text, filePath] = match;
    const depth = Math.floor(indent.length / 2);
    const node: SummaryNode = {
      text: text.trim(),
      link: normalizeLink(filePath.trim()),
      items: [],
    };

    if (depth === 0) {
      root.push(node);
    } else {
      const parent = stack[depth - 1];

      if (parent) {
        parent.items.push(node);
      }
    }

    stack[depth] = node;
    stack.length = depth + 1;
  }

  return root;
}

function normalizeLink(filePath: string): string {
  const normalized = filePath.replace(/\\/g, '/').replace(/^\.\//, '');

  if (normalized === 'index.md') {
    return '/';
  }

  if (normalized.endsWith('/index.md')) {
    return `/${normalized.slice(0, -'index.md'.length)}`;
  }

  return `/${normalized.replace(/\.md$/, '')}`;
}

function toSidebarItem(node: SummaryNode): DefaultTheme.SidebarItem {
  if (node.items.length === 0) {
    return {
      text: node.text,
      link: node.link,
    };
  }

  return {
    text: node.text,
    link: node.link,
    collapsed: false,
    items: node.items.map(toSidebarItem),
  };
}
