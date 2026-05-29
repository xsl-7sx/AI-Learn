import type { Question } from '@/types/quiz'

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']
const OPTION_PREFIX_RE = /^[A-Fa-f][.．、:：]\s*/

export function stripOptionPrefix(option: string): string {
  return option.replace(OPTION_PREFIX_RE, '').trim()
}

export function formatOptionLabel(index: number, option: string): string {
  const cleaned = stripOptionPrefix(option)
  return `${LETTERS[index]}. ${cleaned}`
}

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

function answerIndices(question: Question): number[] {
  return Array.isArray(question.answer) ? question.answer : [question.answer]
}

export function formatAnswerLetters(question: Question): string {
  return answerIndices(question).map((index) => LETTERS[index]).join('、')
}

export function formatAnswerSummary(question: Question): string {
  const indices = answerIndices(question)
  if (question.type === 'judge') {
    const options = getJudgeOptions(question)
    return indices.map((index) => `${LETTERS[index]} ${options[index]}`).join('、')
  }
  const options = question.options ?? []
  return indices.map((index) => formatOptionLabel(index, options[index])).join('；')
}
