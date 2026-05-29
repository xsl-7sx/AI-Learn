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

export function setQuizProgress(index: number, quizId?: string): void {
  uni.setStorageSync(PROGRESS_KEY, { index, quiz_id: quizId })
}

export function getQuizProgress(quizId?: string): number {
  const progress = uni.getStorageSync(PROGRESS_KEY) as { index?: number; quiz_id?: string } | null
  if (quizId && progress?.quiz_id && progress.quiz_id !== quizId) {
    return 0
  }
  return progress?.index ?? 0
}

/** 新开一局：写入题库并重置答题进度与作答记录 */
export function beginQuizSession(session: QuizSession): void {
  setCurrentQuiz(session)
  setQuizAnswers([])
  setQuizProgress(0, session.quiz_id)
}

export function clearQuizSession(): void {
  uni.removeStorageSync(QUIZ_KEY)
  uni.removeStorageSync(ANSWERS_KEY)
  uni.removeStorageSync(PROGRESS_KEY)
}
