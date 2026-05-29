const DISPLAY_FONT = 'LXGW WenKai Screen'
const DISPLAY_FONT_URL =
  'https://cdn.jsdelivr.net/npm/lxgw-wenkai-screen-web@0.4.0/LXGWWenKaiScreen-Regular.woff2'

let displayFontLoaded = false

/** 仅为主标题加载装饰性手写字体，正文一律使用系统无衬线体 */
export function loadDisplayFont(): void {
  if (displayFontLoaded) return

  uni.loadFontFace({
    family: DISPLAY_FONT,
    source: `url("${DISPLAY_FONT_URL}")`,
    global: false,
    success: () => {
      displayFontLoaded = true
    },
    fail: () => {
      /* 加载失败时回退到 PingFang SC */
    },
  })
}

export const FONT_BODY = "'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif"
export const FONT_DISPLAY = `'${DISPLAY_FONT}', 'PingFang SC', 'Microsoft YaHei', sans-serif`
