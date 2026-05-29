<template>
  <view class="page bt-screen">
    <view class="bt-notch-safe" />
    <view class="center-wrap">
      <text class="bt-greeting">AI 正在出题…</text>
      <text class="bt-title-lg">等等，我去翻翻笔记…</text>

      <view class="bt-card">
        <view class="bt-book-flip">
          <AppIcon name="book-open" :size="80" color="#ea580c" />
        </view>
        <view class="bt-progress-line">
          <view :style="{ width: `${progress}%` }" />
        </view>
        <text class="bt-caption">{{ stepText }}</text>
      </view>

      <view class="bt-stepper">
        <view
          v-for="(step, index) in steps"
          :key="step"
          :class="['bt-step', stepClass(index)]"
        >
          <view class="bt-step-num">{{ index + 1 }}</view>
          <text class="bt-step-label">{{ step }}</text>
        </view>
      </view>

      <text class="bt-subtitle">AI 自动搭配单选、多选、判断三种题型</text>
      <button class="bt-btn-secondary" @tap="cancel">取消</button>
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
import { USE_MOCK } from '@/config'
import { generateQuiz, showApiError } from '@/services/api'
import { clearPendingTopic, getPendingTopic, setCurrentQuiz } from '@/utils/storage'
import type { GenerateQuizResponse } from '@/types/quiz'

const progress = ref(0)
const cancelled = ref(false)
const steps = ['检索考点', '出题校验', '排版选项', '准备闯关']
const stepTexts = [
  '① 正在检索考点…',
  '② 正在出题校验…',
  '③ 正在排版选项…',
  '④ 准备进入闯关…',
]

let timer: ReturnType<typeof setInterval> | null = null

const stepText = computed(() => {
  if (progress.value >= 100) return '生成完成，即将进入闯关…'
  const idx = progress.value >= 75 ? 3 : progress.value >= 50 ? 2 : progress.value >= 25 ? 1 : 0
  return stepTexts[idx]
})

function stepClass(index: number) {
  const idx = progress.value >= 75 ? 3 : progress.value >= 50 ? 2 : progress.value >= 25 ? 1 : 0
  if (progress.value >= 100) return 'is-done'
  if (index < idx) return 'is-done'
  if (index === idx) return 'is-active'
  return 'is-pending'
}

function startProgress() {
  timer = setInterval(() => {
    if (progress.value < 40) {
      progress.value = Math.min(90, progress.value + 8 + Math.random() * 6)
    } else {
      progress.value = Math.min(90, progress.value + 2 + Math.random() * 3)
    }
  }, 700)
}

async function loadQuiz() {
  const topic = getPendingTopic()
  if (!topic) {
    uni.showToast({ title: '缺少学习主题', icon: 'none' })
    uni.navigateBack()
    return
  }

  try {
    const result = USE_MOCK
      ? (mockQuiz as GenerateQuizResponse)
      : await generateQuiz(topic)

    if (cancelled.value) return

    progress.value = 100
    setCurrentQuiz({ ...result, topic: result.topic || topic })
    clearPendingTopic()
    setTimeout(() => {
      if (!cancelled.value) {
        uni.redirectTo({ url: '/pages/quiz/quiz' })
      }
    }, 400)
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
  startProgress()
  loadQuiz()
})

onUnmounted(() => {
  cancelled.value = true
  if (timer) clearInterval(timer)
})

onUnload(() => {
  cancelled.value = true
})
</script>

<style scoped lang="scss">
.page {
  min-height: 100vh;
  padding-bottom: calc(140rpx + env(safe-area-inset-bottom));
}

.center-wrap {
  min-height: calc(100vh - 200rpx);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 40rpx;
  text-align: center;
}

.bt-greeting {
  color: #6b7280;
  font-size: 28rpx;
}

.bt-title-lg {
  display: block;
  margin: 16rpx 0 32rpx;
  font-size: 44rpx;
  font-weight: 700;
}

.bt-card {
  width: 100%;
  background: #fff;
  border-radius: 32rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 48rpx rgba(31, 41, 55, 0.07);
}

.bt-book-flip {
  font-size: 80rpx;
  margin-bottom: 24rpx;
}

.bt-caption {
  display: block;
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #1f2937;
}

.bt-stepper {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin: 36rpx 0 20rpx;
}

.bt-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  opacity: 0.45;
}

.bt-step.is-active,
.bt-step.is-done {
  opacity: 1;
}

.bt-step-num {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
}

.bt-step.is-active .bt-step-num,
.bt-step.is-done .bt-step-num {
  background: #fff0e8;
  color: #ea580c;
}

.bt-step-label {
  font-size: 22rpx;
  color: #6b7280;
}

.bt-subtitle {
  font-size: 26rpx;
  color: #9ca3af;
  margin-bottom: 24rpx;
}
</style>
