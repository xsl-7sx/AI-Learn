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
  generating?: boolean
  job_id?: string
  total_expected?: number
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

export type QuizJobStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface GenerateQuizJobResponse {
  job_id: string
  status: 'pending'
}

export interface QuizJobStatusResponse {
  job_id: string
  status: QuizJobStatus
  quiz_id?: string
  topic?: string
  questions: Question[]
  total_expected: number
  ready: boolean
  stream_preview?: string
  result?: GenerateQuizResponse
  error?: string
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
