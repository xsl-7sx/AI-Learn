<template>
  <view v-if="session && question" class="page bt-screen">
    <view class="bt-topbar">
      <view class="bt-progress-pill">第 {{ currentIndex + 1 }} / {{ session.questions.length }} 题</view>
    </view>

    <scroll-view class="stem-scroll" scroll-y>
      <view class="bt-meta-row">
        <text>{{ session.topic }}</text>
        <text class="bt-pill">{{ typeLabel }}</text>
      </view>
      <view class="bt-progress-line">
        <view :style="{ width: `${((currentIndex + 1) / session.questions.length) * 100}%` }" />
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
          <text class="option-text">{{ option }}</text>
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

      <FeedbackPanel
        v-if="locked"
        :correct="lastCorrect"
        :explanation="question.explanation"
      />
      <view class="scroll-bottom-space" />
    </scroll-view>

    <view class="footer">
      <button v-if="locked" class="bt-btn-primary" @tap="goNext">
        {{ isLast ? '查看报告' : '下一题' }}
      </button>
    </view>

    <FloatTabbar />
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import FloatTabbar from '@/components/FloatTabbar.vue'
import FeedbackPanel from '@/components/FeedbackPanel.vue'
import type { Question, QuizSession, UserAnswer } from '@/types/quiz'
import { checkAnswer, getJudgeOptions, getTypeLabel } from '@/utils/scoring'
import {
  getCurrentQuiz,
  getQuizAnswers,
  getQuizProgress,
  setQuizAnswers,
  setQuizProgress,
} from '@/utils/storage'

const letters = ['A', 'B', 'C', 'D', 'E', 'F']
const session = ref<QuizSession | null>(null)
const currentIndex = ref(0)
const selected = ref<number[]>([])
const locked = ref(false)
const lastCorrect = ref(false)
let audio: UniApp.InnerAudioContext | null = null

const question = computed<Question | null>(() => session.value?.questions[currentIndex.value] ?? null)
const typeLabel = computed(() => (question.value ? getTypeLabel(question.value.type) : ''))
const judgeOptions = computed(() => (question.value ? getJudgeOptions(question.value) : []))
const isLast = computed(() => currentIndex.value === (session.value?.questions.length ?? 1) - 1)
const canSubmitMultiple = computed(() => selected.value.length > 0)

function restoreState() {
  session.value = getCurrentQuiz()
  if (!session.value) {
    uni.reLaunch({ url: '/pages/index/index' })
    return
  }
  currentIndex.value = getQuizProgress()
  selected.value = []
  locked.value = false
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

function finalize(selectedValue: number | number[]) {
  if (!question.value || locked.value) return
  const correct = checkAnswer(question.value, selectedValue)
  lastCorrect.value = correct
  locked.value = true
  recordAnswer(selectedValue, correct)
  if (correct) playCorrectSound()
  else vibrateWrong()
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
  if (!session.value) return
  if (isLast.value) {
    uni.redirectTo({ url: '/pages/result/result' })
    return
  }
  currentIndex.value += 1
  setQuizProgress(currentIndex.value)
  selected.value = []
  locked.value = false
}

onShow(() => {
  restoreState()
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
}

.bt-progress-pill {
  display: inline-flex;
  padding: 12rpx 24rpx;
  border-radius: 999rpx;
  background: #fff;
  box-shadow: 0 4rpx 16rpx rgba(31, 41, 55, 0.06);
  font-size: 26rpx;
  font-weight: 600;
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
  height: 40rpx;
}
</style>
