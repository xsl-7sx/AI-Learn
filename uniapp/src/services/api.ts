import { BASE_URL } from '@/config'
import type { GenerateQuizResponse, QuizReportRequest, ReportResponse } from '@/types/quiz'

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
  return '网络异常，请检查后端服务'
}

function request<T>(url: string, data: unknown, timeout: number): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method: 'POST',
      header: { 'Content-Type': 'application/json' },
      data,
      timeout,
      success: (res) => {
        if (res.statusCode !== 200) {
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

export function generateQuiz(topic: string): Promise<GenerateQuizResponse> {
  return request<GenerateQuizResponse>('/api/v1/quiz/generate', { topic }, 180000)
}

export function generateReport(payload: QuizReportRequest): Promise<ReportResponse> {
  return request<ReportResponse>('/api/v1/quiz/report', payload, 30000)
}

export function showApiError(error: unknown, fallback = '请求失败，请重试'): void {
  const message = error instanceof ApiError ? error.message : fallback
  uni.showToast({ title: message, icon: 'none', duration: 2500 })
}
