import { stripTrailingEmptyParens } from '@/utils/reportText'

export interface StructuredMiniReport {
  overview: string
  corePoints: string[]
  wrongAnalysis: string[]
  reviewTips: string[]
}

function sanitizeLine(text: string): string {
  return stripTrailingEmptyParens(text.replace(/\*\*/g, '').trim())
}

function toStringList(value: unknown): string[] {
  if (!Array.isArray(value)) return []
  return value
    .map((item) => sanitizeLine(String(item ?? '')))
    .filter(Boolean)
}

function extractJsonText(raw: string): string {
  const trimmed = raw.trim()
  const fenced = trimmed.match(/```(?:json)?\s*([\s\S]*?)```/i)
  const candidate = (fenced?.[1] ?? trimmed).trim()

  try {
    JSON.parse(candidate)
    return candidate
  } catch {
    // fall through to brace-balanced extraction
  }

  const start = candidate.indexOf('{')
  if (start === -1) return candidate

  let depth = 0
  let inString = false
  let escaped = false
  for (let i = start; i < candidate.length; i += 1) {
    const ch = candidate[i]
    if (inString) {
      if (escaped) {
        escaped = false
      } else if (ch === '\\') {
        escaped = true
      } else if (ch === '"') {
        inString = false
      }
      continue
    }
    if (ch === '"') {
      inString = true
      continue
    }
    if (ch === '{') depth += 1
    else if (ch === '}') {
      depth -= 1
      if (depth === 0) return candidate.slice(start, i + 1)
    }
  }

  return candidate.slice(start)
}

export function parseStructuredReport(raw: string | unknown): StructuredMiniReport | null {
  try {
    const parsed = typeof raw === 'string' ? JSON.parse(extractJsonText(raw)) : raw
    if (!parsed || typeof parsed !== 'object') return null

    const root = (parsed as Record<string, unknown>)['学习复盘报告'] ?? parsed
    if (!root || typeof root !== 'object') return null

    const mini = root as Record<string, unknown>
    const overview = sanitizeLine(String(mini['整体表现'] ?? ''))
    const corePoints = toStringList(mini['核心知识点回顾'])
    const wrongAnalysis = toStringList(mini['易错题分析'])
    const reviewTips = toStringList(mini['复习建议'])

    if (!overview && !corePoints.length && !wrongAnalysis.length && !reviewTips.length) {
      return null
    }

    return { overview, corePoints, wrongAnalysis, reviewTips }
  } catch {
    return null
  }
}
