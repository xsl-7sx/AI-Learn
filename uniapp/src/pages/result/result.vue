<template>
  <view class="page bt-screen">
    <view class="bt-notch-safe" />
    <view class="content">
      <text class="bt-greeting">闯关完成</text>
      <view class="score-card">
        <view class="score-ring">
          <text class="score-num">{{ correctRate }}%</text>
          <text class="score-label">正确率</text>
        </view>
        <text class="score-desc">答对 {{ score }} / {{ total }} 题</text>
      </view>

      <view class="report-box">
        <text class="report-title">AI 复盘报告</text>
        <view v-if="loading" class="skeleton">
          <text>AI 正在生成复盘报告…</text>
          <view class="sk-line" />
          <view class="sk-line short" />
          <view class="sk-line" />
        </view>
        <ReportView v-else :markdown="reportText" />
      </view>

      <view class="actions">
        <button class="bt-btn-primary" @tap="playAgain">再来一局</button>
        <button class="bt-btn-secondary is-disabled" disabled>分享（MVP 暂未开放）</button>
      </view>
    </view>
    <FloatTabbar />
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import FloatTabbar from '@/components/FloatTabbar.vue'
import ReportView from '@/components/ReportView.vue'
import { generateReport, showApiError } from '@/services/api'
import {
  clearQuizSession,
  getCurrentQuiz,
  getQuizAnswers,
} from '@/utils/storage'

const loading = ref(true)
const reportText = ref('')
const score = ref(0)
const total = ref(10)

const correctRate = computed(() => {
  if (!total.value) return 0
  return Math.round((score.value / total.value) * 100)
})

function calcLocalScore() {
  const answers = getQuizAnswers()
  total.value = getCurrentQuiz()?.questions.length ?? 10
  score.value = answers.filter((item) => item.correct).length
}

async function fetchReport() {
  const session = getCurrentQuiz()
  const answers = getQuizAnswers()
  if (!session) {
    uni.reLaunch({ url: '/pages/index/index' })
    return
  }

  calcLocalScore()

  try {
    const res = await generateReport({
      quiz_id: session.quiz_id,
      topic: session.topic,
      questions: session.questions,
      answers,
    })
    score.value = res.score
    total.value = res.total
    reportText.value = res.report
  } catch (error) {
    showApiError(error, '复盘生成失败')
    reportText.value = '## 复盘暂不可用\n\n请稍后重试，或检查后端服务是否已启动。'
  } finally {
    loading.value = false
  }
}

function playAgain() {
  clearQuizSession()
  uni.reLaunch({ url: '/pages/index/index' })
}

onMounted(() => {
  fetchReport()
})
</script>

<style scoped lang="scss">
.page {
  min-height: 100vh;
  padding-bottom: calc(140rpx + env(safe-area-inset-bottom));
}

.content {
  padding: 0 36rpx 40rpx;
}

.bt-greeting {
  display: block;
  padding-top: 24rpx;
  font-size: 28rpx;
  color: #6b7280;
}

.score-card {
  margin: 24rpx 0 32rpx;
  background: #fff;
  border-radius: 32rpx;
  padding: 32rpx;
  text-align: center;
  box-shadow: 0 8rpx 48rpx rgba(31, 41, 55, 0.07);
}

.score-ring {
  width: 220rpx;
  height: 220rpx;
  margin: 0 auto 16rpx;
  border-radius: 50%;
  border: 10rpx solid #f06a2a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-num {
  font-size: 52rpx;
  font-weight: 700;
  color: #f06a2a;
}

.score-label {
  font-size: 24rpx;
  color: #6b7280;
}

.score-desc {
  font-size: 28rpx;
  color: #374151;
}

.report-box {
  background: #fff;
  border-radius: 32rpx;
  padding: 28rpx;
  margin-bottom: 28rpx;
  box-shadow: 0 8rpx 48rpx rgba(31, 41, 55, 0.07);
}

.report-title {
  display: block;
  font-size: 32rpx;
  font-weight: 700;
  margin-bottom: 20rpx;
}

.skeleton {
  color: #6b7280;
  font-size: 28rpx;
}

.sk-line {
  height: 24rpx;
  margin-top: 16rpx;
  border-radius: 12rpx;
  background: linear-gradient(90deg, #f3f4f6, #e5e7eb, #f3f4f6);
}

.sk-line.short {
  width: 70%;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.is-disabled {
  opacity: 0.5;
}
</style>
