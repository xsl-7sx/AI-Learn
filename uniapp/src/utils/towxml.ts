import type { TowxmlNodes } from '@/types/towxml'

let parseMarkdown: ((markdown: string) => TowxmlNodes) | null = null

// #ifdef MP-WEIXIN
// eslint-disable-next-line @typescript-eslint/no-require-imports
const towxml = require('../wxcomponents/towxml/index.js') as (
  content: string,
  type: 'markdown' | 'html',
  option?: Record<string, unknown>,
) => TowxmlNodes

parseMarkdown = (markdown: string) => towxml(markdown, 'markdown', { theme: 'light' })
// #endif

export function markdownToNodes(markdown: string): TowxmlNodes | null {
  if (!parseMarkdown || !markdown.trim()) return null
  try {
    return parseMarkdown(markdown)
  } catch {
    return null
  }
}
