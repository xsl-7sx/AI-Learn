import correctWav from '@/static/audio/correct.wav'
import wrongWav from '@/static/audio/wrong.wav'

interface SoundChannel {
  ctx: UniApp.InnerAudioContext | null
  ready: boolean
  pendingPlay: boolean
  src: string
}

function createChannel(src: string): SoundChannel {
  return { ctx: null, ready: false, pendingPlay: false, src }
}

const correctChannel = createChannel(correctWav)
const wrongChannel = createChannel(wrongWav)

function bindAudio(channel: SoundChannel, ctx: UniApp.InnerAudioContext) {
  ctx.volume = 0.9
  // @ts-expect-error 微信小程序专有字段
  ctx.obeyMuteSwitch = false
  ctx.autoplay = false

  ctx.onCanplay(() => {
    channel.ready = true
    if (channel.pendingPlay) {
      channel.pendingPlay = false
      ctx.seek(0)
      ctx.play()
    }
  })

  ctx.onError((error) => {
    channel.ready = false
    channel.pendingPlay = false
    console.warn('[feedbackSound] load failed', channel.src, error)
  })
}

function ensureChannel(channel: SoundChannel): UniApp.InnerAudioContext {
  if (!channel.ctx) {
    channel.ctx = uni.createInnerAudioContext()
    bindAudio(channel, channel.ctx)
    channel.ctx.src = channel.src
  }
  return channel.ctx
}

function playChannel(channel: SoundChannel) {
  const ctx = ensureChannel(channel)
  if (channel.ready) {
    ctx.seek(0)
    ctx.play()
    return
  }
  channel.pendingPlay = true
  ctx.src = channel.src
}

function destroyChannel(channel: SoundChannel) {
  if (!channel.ctx) return
  channel.ctx.destroy()
  channel.ctx = null
  channel.ready = false
  channel.pendingPlay = false
}

/** 微信全局：静音开关下仍播放音效 */
export function initFeedbackAudio(): void {
  // #ifdef MP-WEIXIN
  if (typeof wx !== 'undefined' && wx.setInnerAudioOption) {
    wx.setInnerAudioOption({ obeyMuteSwitch: false })
  }
  // #endif
  ensureChannel(correctChannel)
  ensureChannel(wrongChannel)
}

/** 进入答题页时预加载 */
export function preloadFeedbackSounds(): void {
  ensureChannel(correctChannel)
  ensureChannel(wrongChannel)
}

/** @deprecated 使用 preloadFeedbackSounds */
export function preloadCorrectSound(): void {
  preloadFeedbackSounds()
}

export function playCorrectSound(): void {
  playChannel(correctChannel)
}

export function playWrongSound(): void {
  playChannel(wrongChannel)
}

export function destroyFeedbackSounds(): void {
  destroyChannel(correctChannel)
  destroyChannel(wrongChannel)
}

/** @deprecated 使用 destroyFeedbackSounds */
export function destroyCorrectSound(): void {
  destroyFeedbackSounds()
}
