import { describe, expect, it } from 'vitest'
import { parseStructuredReport } from '@/utils/structuredReport'

const basePayload = {
  学习复盘报告: {
    整体表现: '本次练测共10题，仅答对2题，正确率20%。',
    核心知识点回顾: ['Few-shot 学习', 'Role-playing'],
    易错题分析: ['提示词应清晰具体'],
    复习建议: ['明天再练一组'],
  },
}

const baseJson = JSON.stringify(basePayload)

describe('MVP G4 结构化复盘解析', () => {
  it('解析纯 JSON', () => {
    const parsed = parseStructuredReport(baseJson)
    expect(parsed?.overview).toContain('10题')
    expect(parsed?.corePoints).toHaveLength(2)
    expect(parsed?.wrongAnalysis).toHaveLength(1)
    expect(parsed?.reviewTips).toHaveLength(1)
  })

  it('容忍尾部说明文字', () => {
    expect(parseStructuredReport(`${baseJson}\n希望对你有帮助`)).not.toBeNull()
  })

  it('容忍前缀说明文字', () => {
    expect(parseStructuredReport(`以下是复盘报告：\n${baseJson}`)).not.toBeNull()
  })

  it('容忍 markdown 代码块包裹', () => {
    expect(parseStructuredReport(`\`\`\`json\n${baseJson}\n\`\`\``)).not.toBeNull()
  })
})
