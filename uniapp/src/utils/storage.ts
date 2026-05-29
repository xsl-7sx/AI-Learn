import type { QuizSession, UserAnswer } from '@/types/quiz'

const LEGACY_QUIZ_KEY = 'currentQuiz'
const LEGACY_ANSWERS_KEY = 'quizAnswers'
const LEGACY_PROGRESS_KEY = 'quizProgress'
const TOPIC_KEY = 'pendingTopic'
const ARCHIVE_KEY = 'quizArchive'
const ACTIVE_QUIZ_ID_KEY = 'activeQuizId'

export interface SavedQuizRecord {
  session: QuizSession
  answers: UserAnswer[]
  progressIndex: number
  updatedAt: number
}

export interface IncompleteQuizSummary {
  topic: string
  quizId: string
  completedCount: number
  totalCount: number
  resumeIndex: number
  updatedAt: number
}

function readArchive(): SavedQuizRecord[] {
  migrateLegacyStorage()
  return (uni.getStorageSync(ARCHIVE_KEY) as SavedQuizRecord[]) || []
}

function writeArchive(records: SavedQuizRecord[]): void {
  uni.setStorageSync(ARCHIVE_KEY, records)
}

function getRecord(quizId: string): SavedQuizRecord | undefined {
  return readArchive().find((item) => item.session.quiz_id === quizId)
}

function upsertRecord(record: SavedQuizRecord): void {
  const records = readArchive().filter((item) => item.session.quiz_id !== record.session.quiz_id)
  records.push(record)
  records.sort((a, b) => b.updatedAt - a.updatedAt)
  writeArchive(records)
}

function removeRecord(quizId: string): void {
  writeArchive(readArchive().filter((item) => item.session.quiz_id !== quizId))
}

function migrateLegacyStorage(): void {
  const legacy = uni.getStorageSync(LEGACY_QUIZ_KEY) as QuizSession | null
  if (!legacy?.quiz_id) return

  const existing = (uni.getStorageSync(ARCHIVE_KEY) as SavedQuizRecord[]) || []
  if (existing.some((item) => item.session.quiz_id === legacy.quiz_id)) {
    uni.removeStorageSync(LEGACY_QUIZ_KEY)
    uni.removeStorageSync(LEGACY_ANSWERS_KEY)
    uni.removeStorageSync(LEGACY_PROGRESS_KEY)
    return
  }

  const legacyAnswers = (uni.getStorageSync(LEGACY_ANSWERS_KEY) as UserAnswer[]) || []
  const legacyProgress = uni.getStorageSync(LEGACY_PROGRESS_KEY) as { index?: number } | null

  writeArchive([
    {
      session: legacy,
      answers: legacyAnswers,
      progressIndex: legacyProgress?.index ?? 0,
      updatedAt: Date.now(),
    },
    ...existing,
  ])

  if (!uni.getStorageSync(ACTIVE_QUIZ_ID_KEY)) {
    uni.setStorageSync(ACTIVE_QUIZ_ID_KEY, legacy.quiz_id)
  }

  uni.removeStorageSync(LEGACY_QUIZ_KEY)
  uni.removeStorageSync(LEGACY_ANSWERS_KEY)
  uni.removeStorageSync(LEGACY_PROGRESS_KEY)
}

function resolveQuizId(quizId?: string): string | null {
  return quizId || (uni.getStorageSync(ACTIVE_QUIZ_ID_KEY) as string) || null
}

export function setPendingTopic(topic: string): void {
  uni.setStorageSync(TOPIC_KEY, topic)
}

export function getPendingTopic(): string {
  return (uni.getStorageSync(TOPIC_KEY) as string) || ''
}

export function clearPendingTopic(): void {
  uni.removeStorageSync(TOPIC_KEY)
}

export function getActiveQuizId(): string | null {
  migrateLegacyStorage()
  return (uni.getStorageSync(ACTIVE_QUIZ_ID_KEY) as string) || null
}

export function setActiveQuizId(quizId: string): void {
  uni.setStorageSync(ACTIVE_QUIZ_ID_KEY, quizId)
}

export function activateQuiz(quizId: string): boolean {
  const record = getRecord(quizId)
  if (!record) return false
  setActiveQuizId(quizId)
  return true
}

export function setCurrentQuiz(session: QuizSession): void {
  const existing = getRecord(session.quiz_id)
  upsertRecord({
    session,
    answers: existing?.answers ?? [],
    progressIndex: existing?.progressIndex ?? 0,
    updatedAt: Date.now(),
  })
  setActiveQuizId(session.quiz_id)
}

export function getCurrentQuiz(): QuizSession | null {
  const quizId = getActiveQuizId()
  if (!quizId) return null
  return getRecord(quizId)?.session ?? null
}

export function setQuizAnswers(answers: UserAnswer[], quizId?: string): void {
  const id = resolveQuizId(quizId)
  if (!id) return
  const record = getRecord(id)
  if (!record) return
  upsertRecord({
    ...record,
    answers,
    updatedAt: Date.now(),
  })
}

export function getQuizAnswers(quizId?: string): UserAnswer[] {
  const id = resolveQuizId(quizId)
  if (!id) return []
  return getRecord(id)?.answers ?? []
}

export function setQuizProgress(index: number, quizId?: string): void {
  const id = resolveQuizId(quizId)
  if (!id) return
  const record = getRecord(id)
  if (!record) return
  upsertRecord({
    ...record,
    progressIndex: index,
    updatedAt: Date.now(),
  })
}

export function getQuizProgress(quizId?: string): number {
  const id = resolveQuizId(quizId)
  if (!id) return 0
  return getRecord(id)?.progressIndex ?? 0
}

/** 新开一局：写入题库并重置该关卡的答题进度与作答记录 */
export function beginQuizSession(session: QuizSession): void {
  upsertRecord({
    session,
    answers: [],
    progressIndex: 0,
    updatedAt: Date.now(),
  })
  setActiveQuizId(session.quiz_id)
}

export function clearQuizSession(quizId?: string): void {
  const id = resolveQuizId(quizId)
  if (!id) return
  removeRecord(id)
  if (getActiveQuizId() === id) {
    uni.removeStorageSync(ACTIVE_QUIZ_ID_KEY)
  }
}

function toIncompleteSummary(record: SavedQuizRecord): IncompleteQuizSummary | null {
  const totalCount = record.session.total_expected || record.session.questions.length || 10
  if (record.answers.length >= totalCount) return null
  return {
    topic: record.session.topic,
    quizId: record.session.quiz_id,
    completedCount: record.answers.length,
    totalCount,
    resumeIndex: record.progressIndex,
    updatedAt: record.updatedAt,
  }
}

/** 首页「未完成关卡」列表，按最近更新时间倒序 */
export function getIncompleteQuizzes(): IncompleteQuizSummary[] {
  return readArchive()
    .map(toIncompleteSummary)
    .filter((item): item is IncompleteQuizSummary => item !== null)
    .sort((a, b) => b.updatedAt - a.updatedAt)
}

/** @deprecated 使用 getIncompleteQuizzes */
export function getIncompleteQuiz(): IncompleteQuizSummary | null {
  return getIncompleteQuizzes()[0] ?? null
}

export function getIncompleteProgressPercent(item: IncompleteQuizSummary): number {
  if (!item.totalCount) return 0
  return Math.min(100, Math.round((item.completedCount / item.totalCount) * 100))
}
