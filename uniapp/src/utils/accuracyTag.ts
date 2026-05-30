export type AccuracyTagTone = 'roast' | 'grind' | 'rise' | 'legend'

export interface AccuracyTag {
  text: string
  tone: AccuracyTagTone
}

const ROAST_TAGS = ['脑子看懂了', '门外汉'] as const
const GRIND_TAGS = ['略知一二', '绝地求生'] as const
const RISE_TAGS = ['渐入佳境', '知识富豪'] as const
const LEGEND_TAGS = ['满分天秀', '触及盲区(真)'] as const

export function getAccuracyTag(accuracy: number, seed = 0): AccuracyTag {
  const rate = Math.min(100, Math.max(0, Math.round(accuracy)))
  const pick = (options: readonly string[], tone: AccuracyTagTone): AccuracyTag => ({
    text: options[Math.abs(seed) % options.length],
    tone,
  })

  if (rate === 100) return pick(LEGEND_TAGS, 'legend')
  if (rate <= 39) return pick(ROAST_TAGS, 'roast')
  if (rate <= 69) return pick(GRIND_TAGS, 'grind')
  return pick(RISE_TAGS, 'rise')
}

export function getEncouragementMessage(accuracy: number): string {
  const rate = Math.min(100, Math.max(0, Math.round(accuracy)))
  if (rate === 100) return '满分通关，太厉害了！'
  if (rate >= 80) return '表现优秀，继续保持！'
  if (rate >= 60) return '表现不错，继续加油！'
  if (rate >= 40) return '有进步空间，再接再厉！'
  return '别灰心，下次一定更好！'
}
