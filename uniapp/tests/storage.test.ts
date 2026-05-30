import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { QuizSession, UserAnswer } from '@/types/quiz'
import {
  beginQuizSession,
  clearQuizSession,
  getCurrentQuiz,
  getIncompleteQuizzes,
  getQuizAnswers,
  setQuizAnswers,
} from '@/utils/storage'

const memory = new Map<string, unknown>()

vi.stubGlobal('uni', {
  getStorageSync: (key: string) => memory.get(key),
  setStorageSync: (key: string, value: unknown) => {
    memory.set(key, value)
  },
  removeStorageSync: (key: string) => {
    memory.delete(key)
  },
})

function makeSession(id: string): QuizSession {
  return {
    quiz_id: id,
    topic: '测试主题',
    questions: Array.from({ length: 10 }, (_, index) => ({
      id: `q${index + 1}`,
      type: 'single',
      stem: `题干${index + 1}`,
      options: ['A', 'B', 'C', 'D'],
      answer: 0,
      explanation: `解析${index + 1}`,
    })),
    total_expected: 10,
  }
}

describe('MVP G2 多关卡存档', () => {
  beforeEach(() => {
    memory.clear()
  })

  it('新开一局写入 archive 并清空作答', () => {
    beginQuizSession(makeSession('quiz_a'))
    expect(getCurrentQuiz()?.quiz_id).toBe('quiz_a')
    expect(getQuizAnswers()).toEqual([])
  })

  it('未完成关卡出现在首页列表', () => {
    beginQuizSession(makeSession('quiz_b'))
    const answers: UserAnswer[] = [{ question_id: 'q1', selected: 0, correct: true }]
    setQuizAnswers(answers)
    const incomplete = getIncompleteQuizzes()
    expect(incomplete).toHaveLength(1)
    expect(incomplete[0].quizId).toBe('quiz_b')
    expect(incomplete[0].completedCount).toBe(1)
  })

  it('再来一局只清除指定关卡', () => {
    beginQuizSession(makeSession('quiz_c'))
    beginQuizSession(makeSession('quiz_d'))
    clearQuizSession('quiz_c')
    expect(getIncompleteQuizzes().some((item) => item.quizId === 'quiz_c')).toBe(false)
    expect(getCurrentQuiz()?.quiz_id).toBe('quiz_d')
  })
})
