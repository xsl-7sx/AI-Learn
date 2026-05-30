<template>
  <view class="score-card">
    <view class="score-card__main">
      <view class="ring-area">
        <view class="ring">
          <view class="ring__track">
            <view class="ring__arc" :style="{ background: arcGradient }" />
          </view>
          <view class="ring__center">
            <text class="ring__pct">{{ displayAccuracy }}%</text>
            <text class="ring__label">正确率</text>
          </view>
        </view>
        <image class="mascot" :src="mascotImg" mode="aspectFit" aria-hidden="true" />
      </view>

      <view class="detail">
        <view class="bubble-row">
          <view class="bubble">
            <text class="bubble__text">{{ encouragement }}</text>
          </view>
          <text class="bubble-star" aria-hidden="true">⭐</text>
        </view>

        <view class="tag-badge" :class="`tag-badge--${tag.tone}`">
          <AppIcon name="medal" :size="26" :color="tagIconColor" />
          <text class="tag-badge__text">{{ tag.text }}</text>
        </view>

        <view class="score-line">
          <text class="score-line__label">答对</text>
          <text class="score-line__num">{{ score }}</text>
          <text class="score-line__slash">/</text>
          <text class="score-line__total">{{ total }}</text>
          <text class="score-line__label">题</text>
        </view>
      </view>
    </view>

    <view class="score-card__divider" />

    <view class="knowledge-row" @tap="emit('knowledge-tap')">
      <view class="knowledge-row__icon">
        <AppIcon name="lightbulb" :size="32" color="#2563eb" />
      </view>
      <view class="knowledge-row__text">
        <text class="knowledge-row__title">知识点掌握情况</text>
        <text class="knowledge-row__sub">知识若水，学无止境</text>
      </view>
      <AppIcon name="chevron-right" :size="32" color="#9ca3af" />
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import AppIcon from '@/components/AppIcon.vue'
import mascotImg from '@/static/result-mascot.png'
import { getAccuracyTag, getEncouragementMessage } from '@/utils/accuracyTag'

const props = defineProps<{
  accuracy: number
  score: number
  total: number
}>()

const emit = defineEmits<{
  'knowledge-tap': []
}>()

const displayAccuracy = ref(0)

const tag = computed(() => getAccuracyTag(props.accuracy, props.score))
const encouragement = computed(() => getEncouragementMessage(props.accuracy))

const tagIconColors: Record<string, string> = {
  roast: '#ef4444',
  grind: '#f06a2a',
  rise: '#16a34a',
  legend: '#9333ea',
}

const tagIconColor = computed(() => tagIconColors[tag.value.tone] ?? tagIconColors.grind)

const arcGradient = computed(() => {
  const pct = Math.min(100, Math.max(0, displayAccuracy.value))
  return `conic-gradient(#f06a2a 0deg, #f06a2a ${pct * 3.6}deg, #fff0e6 ${pct * 3.6}deg, #fff0e6 360deg)`
})

function animateRing(target: number) {
  displayAccuracy.value = 0
  setTimeout(() => {
    displayAccuracy.value = Math.min(100, Math.max(0, target))
  }, 100)
}

onMounted(() => {
  animateRing(props.accuracy)
})

watch(
  () => props.accuracy,
  (value) => {
    animateRing(value)
  },
)
</script>

<style scoped lang="scss">
.score-card {
  margin: 24rpx 0 20rpx;
  border-radius: 32rpx;
  background: #fff;
  box-shadow: 0 8rpx 40rpx rgba(59, 130, 246, 0.1);
  border: 1rpx solid rgba(255, 255, 255, 0.9);
  overflow: hidden;
}

.score-card__main {
  display: flex;
  align-items: flex-start;
  padding: 36rpx 32rpx 28rpx;
  gap: 20rpx;
}

.ring-area {
  position: relative;
  flex-shrink: 0;
  width: 210rpx;
  padding-bottom: 16rpx;
}

.ring {
  position: relative;
  width: 196rpx;
  height: 196rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ring__track {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  padding: 12rpx;
  background: #fff5ee;
}

.ring__arc {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  transition: background 1s cubic-bezier(0.22, 1, 0.36, 1);
}

.ring__center {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 140rpx;
  height: 140rpx;
  border-radius: 50%;
  background: #fff;
}

.ring__pct {
  font-family: var(--font-display, 'PingFang SC', sans-serif);
  font-size: 52rpx;
  font-weight: 800;
  color: #f06a2a;
  line-height: 1.1;
}

.ring__label {
  margin-top: 4rpx;
  font-size: 22rpx;
  color: #9ca3af;
  font-weight: 500;
}

.mascot {
  position: absolute;
  left: -12rpx;
  bottom: -4rpx;
  width: 88rpx;
  height: 88rpx;
  z-index: 2;
}

.detail {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 18rpx;
  padding-top: 8rpx;
}

.bubble-row {
  display: flex;
  align-items: flex-start;
  gap: 6rpx;
}

.bubble {
  position: relative;
  flex: 1;
  min-width: 0;
  padding: 14rpx 18rpx;
  border-radius: 20rpx 20rpx 20rpx 6rpx;
  background: linear-gradient(135deg, #fef08a 0%, #fde047 100%);
  box-shadow: 0 2rpx 8rpx rgba(234, 179, 8, 0.2);

  &::after {
    content: '';
    position: absolute;
    left: 12rpx;
    bottom: -10rpx;
    width: 0;
    height: 0;
    border-left: 10rpx solid transparent;
    border-right: 10rpx solid transparent;
    border-top: 12rpx solid #fde047;
  }
}

.bubble__text {
  font-size: 26rpx;
  font-weight: 700;
  color: #713f12;
  line-height: 1.45;
}

.bubble-star {
  flex-shrink: 0;
  font-size: 36rpx;
  line-height: 1;
  margin-top: -4rpx;
}

.tag-badge {
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 18rpx 8rpx 14rpx;
  border-radius: 999rpx;
}

.tag-badge__text {
  font-size: 24rpx;
  font-weight: 700;
}

.tag-badge--roast {
  background: #fef2f2;
  border: 1rpx solid #fecaca;

  .tag-badge__text {
    color: #b91c1c;
  }
}

.tag-badge--grind {
  background: #fff7ed;
  border: 1rpx solid #fed7aa;

  .tag-badge__text {
    color: #c2410c;
  }
}

.tag-badge--rise {
  background: #f0fdf4;
  border: 1rpx solid #bbf7d0;

  .tag-badge__text {
    color: #15803d;
  }
}

.tag-badge--legend {
  background: #faf5ff;
  border: 1rpx solid #e9d5ff;

  .tag-badge__text {
    color: #7e22ce;
  }
}

.score-line {
  display: flex;
  align-items: baseline;
  gap: 4rpx;
}

.score-line__label {
  font-size: 26rpx;
  color: #6b7280;
}

.score-line__num {
  font-size: 36rpx;
  font-weight: 800;
  color: #f06a2a;
  line-height: 1;
}

.score-line__slash {
  font-size: 28rpx;
  color: #d1d5db;
}

.score-line__total {
  font-size: 30rpx;
  font-weight: 600;
  color: #9ca3af;
  line-height: 1;
}

.score-card__divider {
  margin: 0 32rpx;
  height: 0;
  border-top: 2rpx dashed #e5e7eb;
}

.knowledge-row {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 24rpx 32rpx 28rpx;
}

.knowledge-row__icon {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.knowledge-row__text {
  flex: 1;
  min-width: 0;
}

.knowledge-row__title {
  display: block;
  font-size: 28rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
}

.knowledge-row__sub {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: #9ca3af;
  line-height: 1.4;
}
</style>
