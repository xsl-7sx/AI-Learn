import type { Question } from '@/types/quiz'

function isMultipleChoiceCorrect(selected: number[], answer: number[]): boolean {
  if (selected.length !== answer.length) return false
  const sorted = [...selected].sort((a, b) => a - b)
  const expected = [...answer].sort((a, b) => a - b)
  return sorted.every((value, index) => value === expected[index])
}

export function checkAnswer(question: Question, selected: number | number[]): boolean {
  if (question.type === 'multiple') {
    return isMultipleChoiceCorrect(selected as number[], question.answer as number[])
  }
  return selected === question.answer
}

export function getJudgeOptions(question: Question): string[] {
  if (question.options?.length === 2) return question.options
  return ['正确', '错误']
}

export function getTypeLabel(type: Question['type']): string {
  if (type === 'single') return '单选'
  if (type === 'multiple') return '多选'
  return '判断'
}
