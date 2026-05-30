import { describe, expect, it } from 'vitest'
import type { Question } from '@/types/quiz'
import {
  checkAnswer,
  formatCorrectRatePercent,
  getJudgeOptions,
  getTypeLabel,
} from '@/utils/scoring'

const single: Question = {
  id: 'q1',
  type: 'single',
  stem: '单选',
  options: ['A', 'B', 'C', 'D'],
  answer: 2,
  explanation: '解析',
}

const multiple: Question = {
  id: 'q2',
  type: 'multiple',
  stem: '多选',
  options: ['A', 'B', 'C', 'D'],
  answer: [0, 2],
  explanation: '解析',
}

const judge: Question = {
  id: 'q3',
  type: 'judge',
  stem: '判断',
  options: ['正确', '错误'],
  answer: 1,
  explanation: '解析',
}

describe('MVP G2 本地判分', () => {
  it('单选：选中正确下标判对', () => {
    expect(checkAnswer(single, 2)).toBe(true)
    expect(checkAnswer(single, 1)).toBe(false)
  })

  it('多选：集合相等才判对（顺序无关）', () => {
    expect(checkAnswer(multiple, [2, 0])).toBe(true)
    expect(checkAnswer(multiple, [0, 1])).toBe(false)
    expect(checkAnswer(multiple, [0, 2, 3])).toBe(false)
  })

  it('判断题：answer 为下标 0=正确 1=错误', () => {
    expect(checkAnswer(judge, 1)).toBe(true)
    expect(checkAnswer(judge, 0)).toBe(false)
    expect(getJudgeOptions(judge)).toEqual(['正确', '错误'])
  })

  it('三题型标签可读', () => {
    expect(getTypeLabel('single')).toBe('单选')
    expect(getTypeLabel('multiple')).toBe('多选')
    expect(getTypeLabel('judge')).toBe('判断')
  })

  it('正确率百分比为 0–100 整数', () => {
    expect(formatCorrectRatePercent(2, 5)).toBe(40)
    expect(formatCorrectRatePercent(1, 3)).toBe(33)
    expect(formatCorrectRatePercent(0, 0)).toBe(0)
  })
})
