import { BASE_URL } from '@/config'
import type {
  GenerateQuizJobResponse,
  GenerateQuizResponse,
  QuizJobStatusResponse,
  QuizReportRequest,
  ReportResponse,
} from '@/types/quiz'

export class ApiError extends Error {
  statusCode: number

  constructor(message: string, statusCode: number) {
    super(message)
    this.statusCode = statusCode
  }
}

function parseErrorMessage(data: unknown, statusCode: number): string {
  if (typeof data === 'object' && data !== null && 'detail' in data) {
    const detail = (data as { detail?: unknown }).detail
    if (typeof detail === 'string') return detail
  }
  if (statusCode === 502) return 'AI 生成失败，请重试'
  if (statusCode === 504) return '请求超时，请稍后重试'
  if (statusCode === 404) return '生成任务不存在，请重试'
  return '网络异常，请检查后端服务'
}

function request<T>(
  url: string,
  method: 'GET' | 'POST',
  data: unknown,
  timeout: number,
): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      header: method === 'POST' ? { 'Content-Type': 'application/json' } : undefined,
      data: method === 'POST' ? data : undefined,
      timeout,
      success: (res) => {
        if (res.statusCode !== 200 && res.statusCode !== 202) {
          reject(new ApiError(parseErrorMessage(res.data, res.statusCode), res.statusCode))
          return
        }
        resolve(res.data as T)
      },
      fail: (error) => {
        reject(new ApiError(error.errMsg || '网络连接失败', 0))
      },
    })
  })
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export function startQuizJob(topic: string): Promise<GenerateQuizJobResponse> {
  return request<GenerateQuizJobResponse>('/api/v1/quiz/generate', 'POST', { topic }, 15000)
}

export function getQuizJob(jobId: string): Promise<QuizJobStatusResponse> {
  return request<QuizJobStatusResponse>(`/api/v1/quiz/jobs/${jobId}`, 'GET', null, 15000)
}

const POLL_INTERVAL_MS = 2000
const POLL_MAX_ATTEMPTS = 90

export async function generateQuiz(topic: string): Promise<GenerateQuizResponse> {
  const { job_id: jobId } = await startQuizJob(topic)

  for (let attempt = 0; attempt < POLL_MAX_ATTEMPTS; attempt += 1) {
    const status = await getQuizJob(jobId)

    if (status.status === 'completed' && status.result) {
      return status.result
    }

    if (status.status === 'failed') {
      throw new ApiError(status.error || 'AI 生成失败，请重试', 502)
    }

    await sleep(POLL_INTERVAL_MS)
  }

  throw new ApiError('请求超时，请稍后重试', 504)
}

export function generateReport(payload: QuizReportRequest): Promise<ReportResponse> {
  return request<ReportResponse>('/api/v1/quiz/report', 'POST', payload, 30000)
}

export function showApiError(error: unknown, fallback = '请求失败，请重试'): void {
  const message = error instanceof ApiError ? error.message : fallback
  uni.showToast({ title: message, icon: 'none', duration: 2500 })
}
