import { readFileSync, existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

const uniappRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const srcRoot = path.join(uniappRoot, 'src')

describe('MVP G0/G2/G4 前端静态验收', () => {
  it('G0：pages.json 注册四页面且文件存在', () => {
    const pagesJson = JSON.parse(readFileSync(path.join(srcRoot, 'pages.json'), 'utf-8'))
    const routes: string[] = pagesJson.pages.map((page: { path: string }) => page.path)
    expect(routes).toEqual([
      'pages/index/index',
      'pages/loading/loading',
      'pages/quiz/quiz',
      'pages/result/result',
    ])
    for (const route of routes) {
      expect(existsSync(path.join(srcRoot, `${route}.vue`))).toBe(true)
    }
  })

  it('G2：答题页具备退出 Sheet 与反馈音效模块', () => {
    const quizSource = readFileSync(path.join(srcRoot, 'pages/quiz/quiz.vue'), 'utf-8')
    expect(quizSource).toContain('showExitSheet')
    expect(quizSource).toContain('playWrongSound')
    expect(quizSource).toContain('vibrateShort')
  })

  it('G4：结算页拆分知识点面板与 AI 复盘卡片', () => {
    const resultSource = readFileSync(path.join(srcRoot, 'pages/result/result.vue'), 'utf-8')
    expect(resultSource).toContain('BentoEnergyPool')
    expect(resultSource).toContain('BentoKnowledgePanel')
    expect(resultSource).toContain('BentoReportCards')
    expect(resultSource).toContain('parseStructuredReport')
    expect(existsSync(path.join(srcRoot, 'components/BentoKnowledgePanel.vue'))).toBe(true)
    expect(existsSync(path.join(srcRoot, 'components/BentoReportCards.vue'))).toBe(true)
  })

  it('G2：多关卡存档 API 存在', () => {
    const storageSource = readFileSync(path.join(srcRoot, 'utils/storage.ts'), 'utf-8')
    expect(storageSource).toContain('getIncompleteQuizzes')
    expect(storageSource).toContain('beginQuizSession')
    expect(storageSource).not.toContain('clearStorage')
  })

  it('G4：再来一局使用 clearQuizSession 而非 clearStorage', () => {
    const resultSource = readFileSync(path.join(srcRoot, 'pages/result/result.vue'), 'utf-8')
    expect(resultSource).toContain('clearQuizSession')
    expect(resultSource).not.toContain('clearStorage')
  })
})
