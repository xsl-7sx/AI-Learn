<template>
  <view class="knowledge-wrap">
    <view class="knowledge-teaser" @tap="toggle">
      <view class="knowledge-teaser__icon">
        <AppIcon name="book-open" :size="44" color="#2563eb" />
      </view>
      <view class="knowledge-teaser__body">
        <text class="knowledge-teaser__title">知识点掌握情况</text>
        <text class="knowledge-teaser__desc">基于本次答题，整理关键要点</text>
      </view>
      <view class="knowledge-teaser__btn">
        <text class="knowledge-teaser__btn-text">{{ expanded ? '收起' : '查看' }}</text>
        <text class="knowledge-teaser__btn-arrow" :class="{ 'is-expanded': expanded }">›</text>
      </view>
    </view>

    <view v-if="expanded" class="knowledge-detail">
      <view class="block__list">
        <view
          v-for="(item, index) in points"
          :key="`point-${index}`"
          class="block__item"
        >
          <text class="block__item-idx">{{ index + 1 }}</text>
          <text class="block__item-text">{{ item }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import AppIcon from '@/components/AppIcon.vue'

defineProps<{
  points: string[]
}>()

const expanded = defineModel<boolean>('expanded', { default: false })

function toggle() {
  expanded.value = !expanded.value
}
</script>

<style scoped lang="scss">
.knowledge-wrap {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 20rpx;
}

.knowledge-teaser {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 28rpx 24rpx 28rpx 28rpx;
  border-radius: 28rpx;
  background: #fff;
  box-shadow: 0 8rpx 40rpx rgba(37, 99, 235, 0.08);
  border: 1rpx solid rgba(219, 234, 254, 0.9);
}

.knowledge-teaser__icon {
  width: 88rpx;
  height: 88rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.knowledge-teaser__body {
  flex: 1;
  min-width: 0;
}

.knowledge-teaser__title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
}

.knowledge-teaser__desc {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: #6b7280;
  line-height: 1.4;
}

.knowledge-teaser__btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 2rpx;
  padding: 14rpx 22rpx;
  border-radius: 999rpx;
  background: #eff6ff;
  border: 1rpx solid #bfdbfe;
}

.knowledge-teaser__btn-text {
  font-size: 24rpx;
  font-weight: 600;
  color: #2563eb;
}

.knowledge-teaser__btn-arrow {
  font-size: 28rpx;
  font-weight: 700;
  color: #2563eb;
  line-height: 1;
  display: inline-block;
  transform: rotate(0deg);
  transition: transform 0.22s ease;

  &.is-expanded {
    transform: rotate(90deg);
  }
}

.knowledge-detail {
  padding: 24rpx 28rpx;
  border-radius: 24rpx;
  background: #fff;
  border: 1rpx solid rgba(219, 234, 254, 0.8);
  border-left: 6rpx solid #2563eb;
  box-shadow: 0 4rpx 24rpx rgba(31, 41, 55, 0.04);
  animation: knowledge-in 0.28s ease-out;
}

@keyframes knowledge-in {
  from {
    opacity: 0;
    transform: translateY(-10rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.block__list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.block__item {
  display: flex;
  align-items: flex-start;
  gap: 14rpx;
  padding: 16rpx 18rpx;
  border-radius: 16rpx;
  background: #f8fafc;
}

.block__item-idx {
  flex-shrink: 0;
  width: 36rpx;
  height: 36rpx;
  border-radius: 10rpx;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 22rpx;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.block__item-text {
  flex: 1;
  font-size: 28rpx;
  line-height: 1.65;
  color: #374151;
  padding-top: 2rpx;
}
</style>
