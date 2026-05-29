<template>
  <view class="feedback">
    <view :class="['feedback-bar', correct ? 'is-correct' : 'is-wrong']">
      <text>{{ correct ? '答对了！' : '答错了' }}</text>
    </view>
    <view class="bt-teacher-note">
      <text class="note-title">老师笔记</text>
      <text class="note-body">{{ explanation }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  correct: boolean
  explanation: string
}>()
</script>

<style scoped lang="scss">
.feedback {
  margin-top: 24rpx;
}

.feedback-bar {
  margin-bottom: 16rpx;
  padding: 16rpx 20rpx;
  border-radius: 20rpx;
  font-size: 30rpx;
  font-weight: 700;
}

.feedback-bar.is-correct {
  background: #ecfdf5;
  color: #047857;
}

.feedback-bar.is-wrong {
  background: #fef2f2;
  color: #b91c1c;
}

.note-title {
  display: block;
  font-size: 26rpx;
  font-weight: 700;
  margin-bottom: 8rpx;
}

.note-body {
  display: block;
  line-height: 1.7;
  font-size: 28rpx;
}
</style>
