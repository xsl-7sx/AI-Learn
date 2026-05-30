/** 从 .env.development 读取；真机联调必须填电脑局域网 IP，不能用 127.0.0.1 */
function resolveBaseUrl(): string {
  const fromEnv = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim()
  if (fromEnv) return fromEnv.replace(/\/$/, '')
  return 'http://127.0.0.1:8000'
}

export const BASE_URL = resolveBaseUrl()

/** localtunnel 域名需附加此头，否则微信 request 会拿到拦截页 */
export function buildApiHeaders(method: 'GET' | 'POST'): Record<string, string> {
  const headers: Record<string, string> = {}
  if (method === 'POST') headers['Content-Type'] = 'application/json'
  if (/loca\.lt/i.test(BASE_URL)) headers['Bypass-Tunnel-Reminder'] = 'true'
  return headers
}

/** 是否为 HTTPS 隧道地址（真机可不依赖同一 WiFi） */
export function isTunnelApiUrl(url = BASE_URL): boolean {
  return /^https:\/\//i.test(url) && !/^https:\/\/192\.168\./i.test(url)
}

/** 开发调试：跳过 AI 请求，直接使用 mock 题库 */
export const USE_MOCK = false

/** 是否为仅本机可访问的 API 地址（真机通常会连不上） */
export function isLocalhostApiUrl(url = BASE_URL): boolean {
  return /^(https?:\/\/)?(127\.0\.0\.1|localhost)(:\d+)?/i.test(url)
}
