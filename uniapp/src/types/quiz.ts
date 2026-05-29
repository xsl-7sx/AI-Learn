export type QuestionType = 'single' | 'multiple' | 'judge'

export interface Question {
  id: string
  type: QuestionType
  stem: string
  options?: string[]
  answer: number | number[]
  explanation: string
}

export interface QuizSession {
  quiz_id: string
  topic: string
  questions: Question[]
}

export interface UserAnswer {
  question_id: string
  selected: number | number[]
  correct: boolean
}

export interface GenerateQuizResponse {
  quiz_id: string
  topic: string
  questions: Question[]
}

export interface QuizReportRequest {
  quiz_id: string
  topic: string
  questions: Question[]
  answers: UserAnswer[]
}

export interface ReportResponse {
  score: number
  total: number
  correct_rate: number
  report: string
}

export interface QuizProgress {
  index: number
}
