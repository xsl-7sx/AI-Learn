/** 常见机型状态栏高度（px），API 异常时兜底 */
const STATUS_BAR_FALLBACK: Array<{ test: (model: string, brand: string) => boolean; height: number }> = [
  { test: (m) => /iPhone1[567]/i.test(m), height: 59 },
  { test: (m) => /iPhone1[234]/i.test(m) || /iPhone X/i.test(m), height: 44 },
  { test: (m) => /iPhone/i.test(m), height: 20 },
  { test: (m, b) => /huawei|honor/i.test(b) || /mate|p\d|nova/i.test(m), height: 32 },
  { test: (m, b) => /xiaomi|redmi/i.test(b), height: 28 },
  { test: (m, b) => /oppo|realme|oneplus/i.test(b), height: 30 },
  { test: (m, b) => /vivo/i.test(b), height: 30 },
  { test: (m, b) => /samsung|sm-/i.test(b) || /galaxy/i.test(m), height: 28 },
]

export interface LayoutMetrics {
  statusBarHeight: number
  safeAreaTop: number
  navBarHeight: number
  headerPaddingTop: number
  headerPaddingRight: number
  headerMinHeight: number
  scrollPaddingTop: number
  topicCardWidth: string
  windowWidth: number
  isMpWeixin: boolean
}

function rpxToPx(rpx: number, windowWidth: number): number {
  return (rpx * windowWidth) / 750
}

function resolveStatusBarFallback(model: string, brand: string, platform: string): number {
  for (const item of STATUS_BAR_FALLBACK) {
    if (item.test(model, brand)) return item.height
  }
  return platform === 'ios' ? 44 : 28
}

function readMenuButton() {
  const empty = { top: 0, bottom: 0, height: 0, width: 0, left: 0, right: 0 }
  // #ifdef MP-WEIXIN
  try {
    const rect = uni.getMenuButtonBoundingClientRect()
    if (rect && rect.height > 0) return rect
  } catch {
    /* ignore */
  }
  // #endif
  return empty
}

/** 根据系统信息与微信胶囊位置计算顶部安全间距 */
export function getLayoutMetrics(): LayoutMetrics {
  const info = uni.getSystemInfoSync()
  const windowWidth = info.windowWidth || info.screenWidth || 375
  const platform = (info.platform || '').toLowerCase()
  const model = info.model || ''
  const brand = (info as UniApp.GetSystemInfoResult & { brand?: string }).brand || ''

  let statusBarHeight = info.statusBarHeight ?? 0
  if (statusBarHeight <= 0) {
    statusBarHeight = resolveStatusBarFallback(model, brand, platform)
  }

  const safeInsets = info.safeAreaInsets
  let safeAreaTop = safeInsets?.top ?? info.safeArea?.top ?? 0
  if (safeAreaTop <= 0 && statusBarHeight > 24) {
    safeAreaTop = statusBarHeight
  }

  const menu = readMenuButton()
  const navBarHeight =
    menu.height > 0
      ? menu.height + Math.max(menu.top - statusBarHeight, 0) * 2
      : platform === 'ios'
        ? 44
        : 48

  const isMpWeixin = menu.width > 0

  // 顶栏顶部：不低于状态栏，并与胶囊顶对齐
  const headerPaddingTop =
    menu.top > 0
      ? Math.max(menu.top, statusBarHeight)
      : Math.max(safeAreaTop, statusBarHeight) + 6

  // 右侧为微信胶囊留白，避免与状态栏/胶囊重叠
  const headerPaddingRight =
    menu.left > 0
      ? windowWidth - menu.left + 10
      : rpxToPx(32, windowWidth)

  const headerMinHeight =
    menu.bottom > 0 ? menu.bottom + 12 : statusBarHeight + navBarHeight + 12

  // 顶栏与主标题之间的间距（px）
  const scrollPaddingTop = 8

  const pagePaddingPx = rpxToPx(64, windowWidth)
  const topicGapPx = rpxToPx(40, windowWidth)
  const topicCardWidth = `calc((100vw - ${pagePaddingPx}px - ${topicGapPx}px) / 3)`

  return {
    statusBarHeight,
    safeAreaTop,
    navBarHeight,
    headerPaddingTop,
    headerPaddingRight,
    headerMinHeight,
    scrollPaddingTop,
    topicCardWidth,
    windowWidth,
    isMpWeixin,
  }
}

export function layoutMetricsToStyle(metrics: LayoutMetrics) {
  return {
    header: {
      paddingTop: `${metrics.headerPaddingTop}px`,
      paddingRight: `${metrics.headerPaddingRight}px`,
      minHeight: `${metrics.headerMinHeight}px`,
    },
    scroll: {
      paddingTop: `${metrics.scrollPaddingTop}px`,
    },
    topicCard: {
      width: metrics.topicCardWidth,
    },
  }
}
