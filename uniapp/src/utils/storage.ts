import type { QuizSession, UserAnswer } from '@/types/quiz'

const QUIZ_KEY = 'currentQuiz'
const ANSWERS_KEY = 'quizAnswers'
const PROGRESS_KEY = 'quizProgress'
const TOPIC_KEY = 'pendingTopic'

export function setPendingTopic(topic: string): void {
  uni.setStorageSync(TOPIC_KEY, topic)
}

export function getPendingTopic(): string {
  return (uni.getStorageSync(TOPIC_KEY) as string) || ''
}

export function clearPendingTopic(): void {
  uni.removeStorageSync(TOPIC_KEY)
}

export function setCurrentQuiz(session: QuizSession): void {
  uni.setStorageSync(QUIZ_KEY, session)
}

export function getCurrentQuiz(): QuizSession | null {
  return (uni.getStorageSync(QUIZ_KEY) as QuizSession) || null
}

export function setQuizAnswers(answers: UserAnswer[]): void {
  uni.setStorageSync(ANSWERS_KEY, answers)
}

export function getQuizAnswers(): UserAnswer[] {
  return (uni.getStorageSync(ANSWERS_KEY) as UserAnswer[]) || []
}

export function setQuizProgress(index: number): void {
  uni.setStorageSync(PROGRESS_KEY, { index })
}

export function getQuizProgress(): number {
  const progress = uni.getStorageSync(PROGRESS_KEY) as { index?: number } | null
  return progress?.index ?? 0
}

export function clearQuizSession(): void {
  uni.removeStorageSync(QUIZ_KEY)
  uni.removeStorageSync(ANSWERS_KEY)
  uni.removeStorageSync(PROGRESS_KEY)
}
