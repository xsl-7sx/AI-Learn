<template>
  <view class="page bt-screen">
    <view class="loading-header" :style="headerStyle">
      <text class="bt-greeting">AI 正在出题…</text>
      <text class="bt-title-lg">{{ headline }}</text>
    </view>

    <view class="loading-body">
      <view class="loading-main">
        <view class="bt-card">
          <view class="bt-book-flip">
            <AppIcon name="book-open" :size="80" color="#ea580c" />
          </view>
          <view class="bt-progress-line">
            <view class="bt-progress-fill" :style="{ width: `${progress}%` }" />
          </view>
          <text class="bt-caption">{{ stepText }}</text>
          <text v-if="typingHint" class="typing-hint">{{ typingHint }}</text>
        </view>

        <view class="bt-stepper">
          <view
            v-for="(step, index) in steps"
            :key="step"
            :class="['bt-step', stepClass(index)]"
          >
            <view class="bt-step-num">
              <text class="bt-step-num-text">{{ index + 1 }}</text>
            </view>
            <text class="bt-step-label">{{ step }}</text>
          </view>
        </view>

        <text class="bt-subtitle">
          {{ readyCount > 0 ? `已就绪 ${readyCount}/${totalExpected} 题，首题可先开练` : 'AI 自动搭配单选、多选、判断三种题型' }}
        </text>
        <view class="loading-cancel" @tap="cancel">取消</view>
      </view>
    </view>

    <FloatTabbar />
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { onUnload } from '@dcloudio/uni-app'
import AppIcon from '@/components/AppIcon.vue'
import FloatTabbar from '@/components/FloatTabbar.vue'
import mockQuiz from '@/mock/quiz.json'
import { BASE_URL, USE_MOCK, isLocalhostApiUrl } from '@/config'
import { showApiError, waitForFirstQuestion } from '@/services/api'
import { getLayoutMetrics } from '@/utils/layout'
import { clearPendingTopic, beginQuizSession, getPendingTopic } from '@/utils/storage'
import type { GenerateQuizResponse } from '@/types/quiz'

const progress = ref(0)
const cancelled = ref(false)
const readyCount = ref(0)
const totalExpected = ref(10)
const hasStreamActivity = ref(false)
const steps = ['检索考点', '出题校验', '排版选项', '准备闯关']
const stepTexts = ['正在检索考点…', '正在出题校验…', '正在排版选项…', '准备进入闯关…']

let timer: ReturnType<typeof setInterval> | null = null

const layoutMetrics = ref(getLayoutMetrics())
const headerStyle = computed(() => ({
  paddingTop: `${layoutMetrics.value.headerPaddingTop + 12}px`,
}))

const headline = computed(() => {
  if (readyCount.value > 0) return '第一题好了，准备开练！'
  return '等等，我去翻翻笔记…'
})

const currentStepIndex = computed(() => {
  if (progress.value >= 100) return 3
  if (readyCount.value > 0) return 3
  if (progress.value >= 75) return 3
  if (progress.value >= 50) return 2
  if (progress.value >= 25) return 1
  return 0
})

const stepText = computed(() => {
  if (progress.value >= 100) return '生成完成，即将进入闯关…'
  if (readyCount.value > 0) return `第 ${readyCount.value} 题已生成，正在准备闯关…`
  if (progress.value >= 90) return '快好了，再等等…'
  if (hasStreamActivity.value) return 'AI 正在逐字出题…'
  return stepTexts[currentStepIndex.value]
})

const typingHint = computed(() => {
  if (readyCount.value > 0) return ''
  if (!hasStreamActivity.value) return ''
  if (progress.value < 50) return '正在构思题干和选项…'
  if (progress.value < 80) return '正在撰写解析…'
  return '马上就好…'
})

function stepClass(index: number) {
  if (progress.value >= 100) return index === 3 ? 'is-active' : 'is-done'
  if (readyCount.value > 0) {
    if (index < 3) return 'is-done'
    return index === 3 ? 'is-active' : 'is-pending'
  }
  if (index < currentStepIndex.value) return 'is-done'
  if (index === currentStepIndex.value) return 'is-active'
  return 'is-pending'
}

function startProgress() {
  timer = setInterval(() => {
    if (cancelled.value || progress.value >= 100) return
    if (progress.value < 40) {
      progress.value = Math.min(88, progress.value + 6 + Math.random() * 6)
    } else if (progress.value < 88) {
      progress.value = Math.min(88, progress.value + 2 + Math.random() * 3)
    } else if (progress.value < 96) {
      progress.value = Math.min(96, progress.value + 0.5 + Math.random() * 0.5)
    }
  }, 650)
}

function stopProgress() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function applyStreamStatus(status: { questions: { length: number }; total_expected: number; stream_preview?: string }) {
  hasStreamActivity.value = true
  readyCount.value = status.questions.length
  totalExpected.value = status.total_expected
  const streamTarget = 12 + (readyCount.value / Math.max(status.total_expected, 1)) * 78
  progress.value = Math.max(progress.value, Math.min(96, streamTarget))
  if (readyCount.value > 0) {
    progress.value = Math.max(progress.value, 92)
  }
}

async function loadQuiz() {
  const topic = getPendingTopic()
  if (!topic) {
    uni.showToast({ title: '缺少学习主题', icon: 'none' })
    uni.navigateBack()
    return
  }

  try {
    if (USE_MOCK) {
      const result = mockQuiz as GenerateQuizResponse
      beginQuizSession({ ...result, topic: result.topic || topic })
      clearPendingTopic()
      if (!cancelled.value) {
        uni.redirectTo({ url: '/pages/quiz/quiz' })
      }
      return
    }

    const session = await waitForFirstQuestion(topic, applyStreamStatus)
    if (cancelled.value) return

    progress.value = 100
    stopProgress()
    beginQuizSession({ ...session, topic: session.topic || topic })
    clearPendingTopic()
    setTimeout(() => {
      if (!cancelled.value) {
        uni.redirectTo({ url: '/pages/quiz/quiz' })
      }
    }, 300)
  } catch (error) {
    if (cancelled.value) return
    showApiError(error, '生成失败，请重试')
    setTimeout(() => uni.navigateBack(), 800)
  }
}

function cancel() {
  cancelled.value = true
  clearPendingTopic()
  uni.navigateBack()
}

onMounted(() => {
  layoutMetrics.value = getLayoutMetrics()
  if (!USE_MOCK && isLocalhostApiUrl()) {
    uni.showToast({
      title: 'API 为 127.0.0.1，真机无法出题，请 npm run dev:mp-weixin 或重新 build',
      icon: 'none',
      duration: 4000,
    })
  }
  startProgress()
  loadQuiz()
})

onUnmounted(() => {
  cancelled.value = true
  stopProgress()
})

onUnload(() => {
  cancelled.value = true
})
</script>

<style scoped lang="scss">
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.loading-header {
  flex-shrink: 0;
  padding: 0 40rpx 8rpx;
  text-align: center;
}

.loading-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 40rpx;
  padding-bottom: calc(130rpx + env(safe-area-inset-bottom));
  box-sizing: border-box;
}

.loading-main {
  width: 100%;
  max-width: 90%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.bt-greeting {
  color: #6b7280;
  font-size: 28rpx;
}

.bt-title-lg {
  display: block;
  margin-top: 12rpx;
  font-family: var(--font-display);
  font-size: 44rpx;
  font-weight: 700;
  color: #1c1917;
  line-height: 1.35;
}

.bt-card {
  width: 100%;
  background: #fff;
  border-radius: 32rpx;
  padding: 40rpx 36rpx;
  box-shadow: 0 8rpx 48rpx rgba(31, 41, 55, 0.07);
  box-sizing: border-box;
}

.bt-book-flip {
  display: flex;
  justify-content: center;
  margin-bottom: 32rpx;
  animation: book-float 2.4s ease-in-out infinite;
}

.bt-progress-line {
  position: relative;
  overflow: hidden;
}

.bt-progress-fill {
  display: block;
  height: 100%;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #f06a2a 0%, #ffb07c 50%, #f06a2a 100%);
  background-size: 200% 100%;
  animation: progress-shimmer 1.6s ease-in-out infinite;
  transition: width 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes progress-shimmer {
  0% {
    background-position: 100% 0;
  }

  100% {
    background-position: -100% 0;
  }
}

@keyframes book-float {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10rpx);
  }
}

.bt-caption {
  display: block;
  margin-top: 24rpx;
  font-size: 28rpx;
  color: #374151;
}

.typing-hint {
  display: block;
  margin-top: 16rpx;
  font-size: 24rpx;
  line-height: 1.6;
  color: #9ca3af;
  animation: hint-fade 2.4s ease-in-out infinite;
}

@keyframes hint-fade {
  0%,
  100% {
    opacity: 0.55;
  }

  50% {
    opacity: 1;
  }
}

.bt-stepper {
  display: flex;
  width: 88%;
  align-self: center;
  margin: 40rpx 0 28rpx;
}

.bt-step {
  width: 25%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  text-align: center;
}

.bt-step-num {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-sizing: border-box;
}

.bt-step-num-text {
  display: block;
  font-size: 24rpx;
  line-height: 1;
  color: #9ca3af;
  text-align: center;
  padding-top: 2rpx;
}

.bt-step.is-done .bt-step-num {
  background: #fff7ed;
}

.bt-step.is-done .bt-step-num-text {
  color: #fdba74;
  font-weight: 600;
}

.bt-step.is-active .bt-step-num {
  background: #ea580c;
  box-shadow: 0 4rpx 16rpx rgba(234, 88, 12, 0.28);
  animation: step-pulse 1.4s ease-in-out infinite;
}

@keyframes step-pulse {
  0%,
  100% {
    transform: scale(1);
    box-shadow: 0 4rpx 16rpx rgba(234, 88, 12, 0.28);
  }

  50% {
    transform: scale(1.08);
    box-shadow: 0 6rpx 20rpx rgba(234, 88, 12, 0.38);
  }
}

.bt-step.is-active .bt-step-num-text {
  color: #fff;
  font-weight: 700;
  padding-top: 1rpx;
}

.bt-step-label {
  width: 100%;
  font-size: 20rpx;
  color: #9ca3af;
  line-height: 1.3;
  text-align: center;
  white-space: nowrap;
}

.bt-step.is-done .bt-step-label {
  color: #9ca3af;
  font-weight: 400;
}

.bt-step.is-active .bt-step-label {
  color: #ea580c;
  font-weight: 700;
}

.bt-subtitle {
  font-size: 26rpx;
  color: #6b7280;
  margin-bottom: 40rpx;
  line-height: 1.5;
  text-align: center;
}

.loading-cancel {
  width: 100%;
  min-height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 40rpx;
  font-size: 30rpx;
  font-weight: 500;
  color: #4b5563;
  border: 2rpx solid #d1d5db;
  border-radius: 999rpx;
  background: #fff;
  box-sizing: border-box;
  box-shadow: 0 4rpx 16rpx rgba(31, 41, 55, 0.04);
}
</style>
