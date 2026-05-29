<template>
  <view v-if="session && question && !waitingNext" class="page bt-screen">
    <view class="bt-topbar">
      <view class="bt-progress-pill">第 {{ currentIndex + 1 }} / {{ totalQuestions }} 题</view>
      <view v-if="isGenerating" class="bt-generating-pill">
        <text>AI 生成中 {{ session.questions.length }}/{{ totalQuestions }}</text>
      </view>
    </view>

    <scroll-view class="stem-scroll" scroll-y :scroll-into-view="scrollIntoView" scroll-with-animation>
      <view class="bt-meta-row">
        <text>{{ session.topic }}</text>
        <text class="bt-pill">{{ typeLabel }}</text>
      </view>
      <view class="bt-progress-line">
        <view :style="{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }" />
      </view>
      <text class="bt-q-stem">{{ question.stem }}</text>

      <view v-if="question.type !== 'judge'" class="options-wrap">
        <view
          v-for="(option, index) in question.options"
          :key="index"
          :class="optionClass(index)"
          @tap="onSelect(index)"
        >
          <text class="bt-opt-letter">{{ letters[index] }}</text>
          <text class="option-text">{{ stripOptionPrefix(option) }}</text>
        </view>
        <button
          v-if="question.type === 'multiple'"
          class="bt-btn-primary submit-btn"
          :disabled="!canSubmitMultiple || locked"
          @tap="submitMultiple"
        >
          确认提交
        </button>
      </view>

      <view v-else class="bt-judge-row">
        <view
          v-for="(label, index) in judgeOptions"
          :key="label"
          :class="judgeClass(index)"
          @tap="onSelect(index)"
        >
          {{ label }}
        </view>
      </view>

      <view id="feedback-anchor" class="feedback-anchor" />
      <FeedbackPanel
        v-if="locked && question"
        :correct="lastCorrect"
        :explanation="question.explanation"
        :question="question"
      />
      <view class="scroll-bottom-space" />
    </scroll-view>

    <view class="footer">
      <button v-if="locked" class="bt-btn-primary" :disabled="waitingNext" @tap="goNext">
        {{ nextButtonText }}
      </button>
    </view>

    <FloatTabbar />
  </view>

  <view v-else-if="waitingNext && session" class="page bt-screen waiting-page">
    <view class="waiting-card">
      <view class="waiting-book">
        <AppIcon name="book-open" :size="72" color="#ea580c" />
      </view>
      <text class="waiting-title">下一题正在生成中…</text>
      <text class="waiting-sub">已就绪 {{ session.questions.length }}/{{ totalQuestions }} 题</text>
      <view class="waiting-progress-line">
        <view class="waiting-progress-fill" />
      </view>
    </view>
    <FloatTabbar />
  </view>
</template>

<script setup lang="ts">
import { computed, nextTick, onUnmounted, ref } from 'vue'
import { onHide, onShow } from '@dcloudio/uni-app'
import AppIcon from '@/components/AppIcon.vue'
import FloatTabbar from '@/components/FloatTabbar.vue'
import FeedbackPanel from '@/components/FeedbackPanel.vue'
import { getQuizJob } from '@/services/api'
import type { Question, QuizSession, UserAnswer } from '@/types/quiz'
import { checkAnswer, getJudgeOptions, getTypeLabel, stripOptionPrefix } from '@/utils/scoring'
import {
  getCurrentQuiz,
  getQuizAnswers,
  getQuizProgress,
  setCurrentQuiz,
  setQuizAnswers,
  setQuizProgress,
} from '@/utils/storage'

const letters = ['A', 'B', 'C', 'D', 'E', 'F']
const session = ref<QuizSession | null>(null)
const currentIndex = ref(0)
const selected = ref<number[]>([])
const locked = ref(false)
const lastCorrect = ref(false)
const waitingNext = ref(false)
const scrollIntoView = ref('')
let audio: UniApp.InnerAudioContext | null = null
let syncTimer: ReturnType<typeof setInterval> | null = null
let syncIntervalMs = 800

const totalQuestions = computed(() => session.value?.total_expected || session.value?.questions.length || 10)
const isGenerating = computed(() => Boolean(session.value?.generating))
const question = computed<Question | null>(() => session.value?.questions[currentIndex.value] ?? null)
const typeLabel = computed(() => (question.value ? getTypeLabel(question.value.type) : ''))
const judgeOptions = computed(() => (question.value ? getJudgeOptions(question.value) : []))
const isLast = computed(() => currentIndex.value >= totalQuestions.value - 1)
const canSubmitMultiple = computed(() => selected.value.length > 0)
const nextButtonText = computed(() => {
  if (waitingNext.value) return '下一题生成中…'
  return isLast.value ? '查看报告' : '下一题'
})

function restoreState() {
  session.value = getCurrentQuiz()
  if (!session.value) {
    uni.reLaunch({ url: '/pages/index/index' })
    return
  }
  const savedIndex = getQuizProgress(session.value.quiz_id)
  const maxIndex = Math.max(0, session.value.questions.length - 1)
  currentIndex.value = Math.min(Math.max(savedIndex, 0), maxIndex)
  selected.value = []
  locked.value = false
  waitingNext.value =
    currentIndex.value + 1 >= session.value.questions.length
    && session.value.questions.length < (session.value.total_expected || 10)
}

function tryAdvanceToNextQuestion() {
  if (!session.value) return

  const nextIndex = currentIndex.value + 1
  if (nextIndex < session.value.questions.length) {
    currentIndex.value = nextIndex
    setQuizProgress(currentIndex.value, session.value.quiz_id)
    selected.value = []
    locked.value = false
    waitingNext.value = false
    syncIntervalMs = 800
    restartBackgroundSync()
    return
  }

  const expected = session.value.total_expected || 10
  waitingNext.value =
    session.value.questions.length < expected
    && (Boolean(session.value.generating) || Boolean(session.value.job_id))
}

function mergeSession(status: Awaited<ReturnType<typeof getQuizJob>>) {
  if (!session.value) return

  const nextSession: QuizSession = {
    ...session.value,
    quiz_id: status.quiz_id || session.value.quiz_id,
    topic: status.topic || session.value.topic,
    questions: status.questions,
    generating: status.status !== 'completed',
    total_expected: status.total_expected,
    job_id: status.job_id,
  }

  if (status.status === 'completed' && status.result) {
    nextSession.questions = status.result.questions
    nextSession.generating = false
    nextSession.quiz_id = status.result.quiz_id
  }

  session.value = nextSession
  setCurrentQuiz(nextSession)
  tryAdvanceToNextQuestion()
}

function shouldSyncJob(): boolean {
  if (!session.value?.job_id) return false
  const expected = session.value.total_expected || 10
  if (session.value.generating) return true
  if (waitingNext.value) return true
  if (session.value.questions.length < expected) return true
  return false
}

async function syncQuizJob() {
  const jobId = session.value?.job_id
  if (!jobId || !shouldSyncJob()) {
    if (!waitingNext.value && session.value && !session.value.generating) {
      stopBackgroundSync()
    }
    return
  }

  try {
    const status = await getQuizJob(jobId)
    mergeSession(status)
    if (status.status === 'completed' || status.questions.length >= (status.total_expected || 10)) {
      syncIntervalMs = 800
    }
  } catch {
    // 后台同步失败时静默，下一轮继续
  }
}

function restartBackgroundSync() {
  stopBackgroundSync()
  startBackgroundSync()
}

function startBackgroundSync() {
  if (!shouldSyncJob()) return
  syncQuizJob()
  syncTimer = setInterval(syncQuizJob, syncIntervalMs)
}

function stopBackgroundSync() {
  if (syncTimer) {
    clearInterval(syncTimer)
    syncTimer = null
  }
}

function optionClass(index: number) {
  const classes = ['bt-opt']
  if (!locked.value) {
    if (question.value?.type === 'multiple' && selected.value.includes(index)) classes.push('is-selected')
    return classes
  }
  const answer = question.value?.answer
  const isAnswer = Array.isArray(answer) ? answer.includes(index) : answer === index
  const isChosen = question.value?.type === 'multiple'
    ? selected.value.includes(index)
    : selected.value[0] === index
  if (isAnswer) classes.push('is-correct')
  else if (isChosen) classes.push('is-wrong')
  return classes
}

function judgeClass(index: number) {
  const classes = ['bt-judge-btn', index === 0 ? 'bt-judge-btn--yes' : 'bt-judge-btn--no']
  if (!locked.value && selected.value[0] === index) classes.push('is-selected')
  if (locked.value) {
    const answer = question.value?.answer
    if (answer === index) classes.push('is-correct')
    else if (selected.value[0] === index) classes.push('is-wrong')
  }
  return classes
}

function playCorrectSound() {
  if (!audio) {
    audio = uni.createInnerAudioContext()
    audio.src = '/static/audio/correct.wav'
  }
  audio.stop()
  audio.play()
}

function vibrateWrong() {
  uni.vibrateShort({ type: 'medium' })
}

function recordAnswer(selectedValue: number | number[], correct: boolean) {
  if (!session.value || !question.value) return
  const answers = getQuizAnswers().filter((item) => item.question_id !== question.value!.id)
  const entry: UserAnswer = {
    question_id: question.value.id,
    selected: selectedValue,
    correct,
  }
  answers.push(entry)
  setQuizAnswers(answers)
}

function scrollToFeedback() {
  scrollIntoView.value = ''
  nextTick(() => {
    scrollIntoView.value = 'feedback-anchor'
  })
}

function finalize(selectedValue: number | number[]) {
  if (!question.value || locked.value) return
  const correct = checkAnswer(question.value, selectedValue)
  lastCorrect.value = correct
  locked.value = true
  recordAnswer(selectedValue, correct)
  if (correct) playCorrectSound()
  else vibrateWrong()
  scrollToFeedback()
}

function onSelect(index: number) {
  if (!question.value || locked.value) return
  if (question.value.type === 'multiple') {
    if (selected.value.includes(index)) {
      selected.value = selected.value.filter((item) => item !== index)
    } else {
      selected.value = [...selected.value, index]
    }
    return
  }
  selected.value = [index]
  finalize(index)
}

function submitMultiple() {
  if (!canSubmitMultiple.value || locked.value) return
  finalize([...selected.value].sort((a, b) => a - b))
}

function goNext() {
  if (!session.value || waitingNext.value) return

  if (isLast.value) {
    if (session.value.generating || session.value.questions.length < totalQuestions.value) {
      uni.showToast({ title: '题目还在生成，请稍候', icon: 'none' })
      return
    }
    uni.redirectTo({ url: '/pages/result/result' })
    return
  }

  const nextIndex = currentIndex.value + 1
  if (nextIndex >= session.value.questions.length) {
    waitingNext.value = true
    locked.value = false
    syncIntervalMs = 350
    restartBackgroundSync()
    syncQuizJob()
    return
  }

  currentIndex.value = nextIndex
  setQuizProgress(currentIndex.value, session.value.quiz_id)
  selected.value = []
  locked.value = false
}

onShow(() => {
  restoreState()
  if (waitingNext.value) {
    syncIntervalMs = 350
  }
  startBackgroundSync()
})

onHide(() => {
  stopBackgroundSync()
})

onUnmounted(() => {
  stopBackgroundSync()
})
</script>

<style scoped lang="scss">
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding-bottom: calc(180rpx + env(safe-area-inset-bottom));
}

.bt-topbar {
  padding: calc(88rpx + env(safe-area-inset-top)) 36rpx 20rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.bt-progress-pill,
.bt-generating-pill {
  display: inline-flex;
  padding: 12rpx 24rpx;
  border-radius: 999rpx;
  background: #fff;
  box-shadow: 0 4rpx 16rpx rgba(31, 41, 55, 0.06);
  font-size: 26rpx;
  font-weight: 600;
}

.bt-generating-pill {
  color: #ea580c;
  background: #fff7ed;
}

.stem-scroll {
  flex: 1;
  min-height: 0;
  padding: 0 36rpx;
  box-sizing: border-box;
}

.bt-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
  color: #6b7280;
  font-size: 26rpx;
}

.bt-pill {
  background: #fff7ed;
  color: #ea580c;
  padding: 6rpx 16rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
}

.bt-q-stem {
  display: block;
  margin: 28rpx 0;
  font-size: 34rpx;
  line-height: 1.7;
  color: #1f2937;
}

.option-text {
  flex: 1;
  line-height: 1.5;
}

.submit-btn {
  margin-top: 12rpx;
}

.footer {
  padding: 20rpx 36rpx 0;
}

.scroll-bottom-space {
  height: 120rpx;
}

.feedback-anchor {
  height: 1px;
}

.waiting-page {
  align-items: center;
  justify-content: center;
  padding: 40rpx;
}

.waiting-card {
  width: 100%;
  max-width: 560rpx;
  background: #fff;
  border-radius: 32rpx;
  padding: 56rpx 40rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20rpx;
  box-shadow: 0 8rpx 48rpx rgba(31, 41, 55, 0.07);
}

.waiting-book {
  animation: book-float 2.4s ease-in-out infinite;
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

.waiting-progress-line {
  width: 100%;
  height: 16rpx;
  border-radius: 999rpx;
  background: #f3f0ea;
  overflow: hidden;
}

.waiting-progress-fill {
  display: block;
  width: 72%;
  height: 100%;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #f06a2a 0%, #ffb07c 50%, #f06a2a 100%);
  background-size: 200% 100%;
  animation: waiting-shimmer 1.4s ease-in-out infinite;
}

@keyframes waiting-shimmer {
  0% {
    background-position: 100% 0;
  }

  100% {
    background-position: -100% 0;
  }
}

.waiting-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #1f2937;
}

.waiting-sub {
  font-size: 26rpx;
  color: #6b7280;
}
</style>
