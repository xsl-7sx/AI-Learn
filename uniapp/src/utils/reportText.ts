const TRAILING_EMPTY_PARENS_RE = /[（(]\s*[）)]\s*$/u

/** 去掉题尾无意义的空括号，如「（ ）」「()」 */
export function stripTrailingEmptyParens(text: string): string {
  return text.replace(TRAILING_EMPTY_PARENS_RE, '').trimEnd()
}

/** 复盘 Markdown 逐行清洗，兜底处理模型漏删的空括号 */
export function sanitizeReportMarkdown(markdown: string): string {
  return markdown
    .split(/\r?\n/)
    .map((line) => stripTrailingEmptyParens(line))
    .join('\n')
}
