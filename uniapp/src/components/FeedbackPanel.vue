<template>
  <view class="feedback">
    <view :class="['bt-feedback-bar', correct ? 'is-correct' : 'is-wrong', 'is-reveal']">
      <view class="bt-feedback-bar__lead">
        <AppIcon
          :name="correct ? 'circle-check' : 'circle-x'"
          :size="36"
          :color="correct ? '#047857' : '#b91c1c'"
        />
        <text class="bt-feedback-bar__text">{{ headline }}</text>
      </view>
      <text v-if="!correct" class="bt-feedback-bar__meta">已记入错题本</text>
    </view>

    <view v-if="!correct && answerSummary" class="answer-hint is-reveal">
      <text class="answer-hint-label">正确答案</text>
      <text class="answer-hint-value">{{ answerSummary }}</text>
    </view>

    <view class="bt-teacher-note bt-teacher-note--reveal">
      <view class="note-head">
        <AppIcon name="lightbulb" :size="32" color="#ea580c" />
        <text class="note-title">{{ noteTitle }}</text>
      </view>
      <text class="note-body">{{ explanation }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/components/AppIcon.vue'
import type { Question } from '@/types/quiz'
import { formatAnswerSummary } from '@/utils/scoring'

const props = defineProps<{
  correct: boolean
  explanation: string
  question: Question
}>()

const headline = computed(() => (props.correct ? '答对啦！' : '啊哦，选错了'))
const noteTitle = computed(() => (props.correct ? '趁热记住' : '一句话搞懂'))
const answerSummary = computed(() => (props.correct ? '' : formatAnswerSummary(props.question)))
</script>

<style scoped lang="scss">
.feedback {
  margin-top: 28rpx;
}

.bt-feedback-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  border-radius: 24rpx;
  margin-bottom: 20rpx;
}

.bt-feedback-bar.is-correct {
  background: #ecfdf5;
  border: 2rpx solid #a7f3d0;
  box-shadow: 0 8rpx 24rpx rgba(34, 197, 94, 0.12);
}

.bt-feedback-bar.is-wrong {
  background: #fef2f2;
  border: 2rpx solid #fecaca;
  box-shadow: 0 8rpx 24rpx rgba(239, 68, 68, 0.1);
}

.bt-feedback-bar__lead {
  display: flex;
  align-items: center;
  gap: 12rpx;
  min-width: 0;
}

.bt-feedback-bar__text {
  font-size: 32rpx;
  font-weight: 700;
  color: #047857;
}

.bt-feedback-bar.is-wrong .bt-feedback-bar__text {
  color: #b91c1c;
}

.bt-feedback-bar__meta {
  flex-shrink: 0;
  font-size: 22rpx;
  font-weight: 500;
  color: #b91c1c;
  opacity: 0.85;
}

.answer-hint {
  margin-bottom: 20rpx;
  padding: 20rpx 24rpx;
  border-radius: 20rpx;
  background: #fff;
  border: 2rpx dashed #fecaca;
}

.answer-hint-label {
  display: block;
  margin-bottom: 8rpx;
  font-size: 24rpx;
  color: #9ca3af;
}

.answer-hint-value {
  display: block;
  font-size: 30rpx;
  font-weight: 600;
  color: #047857;
  line-height: 1.6;
}

.note-head {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 12rpx;
}

.note-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #ea580c;
}

.note-body {
  display: block;
  line-height: 1.75;
  font-size: 28rpx;
  color: #44403c;
}

.is-reveal {
  animation: feedback-in 0.42s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.bt-teacher-note--reveal {
  animation-delay: 0.12s;
}

@keyframes feedback-in {
  from {
    opacity: 0;
    transform: translateY(16rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
