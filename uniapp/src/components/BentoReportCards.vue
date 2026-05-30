<template>
  <view class="report-wrap">
    <view class="report-teaser" @tap="openReport">
      <view class="report-teaser__icon">
        <AppIcon name="bot" :size="44" color="#7c3aed" />
      </view>
      <view class="report-teaser__body">
        <text class="report-teaser__title">AI 复盘报告</text>
        <text class="report-teaser__desc">AI 分析答题情况，帮你查漏补缺</text>
      </view>
      <view class="report-teaser__btn">
        <text class="report-teaser__btn-text">{{ expanded ? '收起' : '查看报告' }}</text>
        <text class="report-teaser__btn-arrow" :class="{ 'is-expanded': expanded }">›</text>
      </view>
    </view>

    <view v-if="expanded" class="report-detail">
      <view v-if="report.overview" class="block block--overview">
        <view class="block__head">
          <AppIcon name="target" :size="28" color="#f06a2a" />
          <text class="block__title">整体表现</text>
        </view>
        <text class="block__text">{{ report.overview }}</text>
      </view>

      <view v-if="report.wrongAnalysis.length" class="block block--wrong">
        <view class="block__head">
          <AppIcon name="circle-x" :size="28" color="#dc2626" />
          <text class="block__title">易错题分析</text>
        </view>
        <view class="block__list">
          <view
            v-for="(item, index) in report.wrongAnalysis"
            :key="`wrong-${index}`"
            class="block__item block__item--wrong"
          >
            <text class="block__item-idx">{{ index + 1 }}</text>
            <text class="block__item-text">{{ item }}</text>
          </view>
        </view>
      </view>

      <view v-if="report.reviewTips.length" class="block block--tips">
        <view class="block__head">
          <AppIcon name="lightbulb" :size="28" color="#f06a2a" />
          <text class="block__title">复习建议</text>
        </view>
        <view class="tips-list">
          <view
            v-for="(item, index) in report.reviewTips"
            :key="`tip-${index}`"
            class="tips-list__row"
          >
            <text class="tips-list__mark">·</text>
            <text class="tips-list__text">{{ item }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import AppIcon from '@/components/AppIcon.vue'
import type { StructuredMiniReport } from '@/utils/structuredReport'

defineProps<{
  report: StructuredMiniReport
}>()

const expanded = defineModel<boolean>('expanded', { default: false })

function openReport() {
  expanded.value = !expanded.value
}
</script>

<style scoped lang="scss">
.report-wrap {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.report-teaser {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 28rpx 24rpx 28rpx 28rpx;
  border-radius: 28rpx;
  background: #fff;
  box-shadow: 0 8rpx 40rpx rgba(124, 58, 237, 0.08);
  border: 1rpx solid rgba(237, 233, 254, 0.9);
}

.report-teaser__icon {
  width: 88rpx;
  height: 88rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.report-teaser__body {
  flex: 1;
  min-width: 0;
}

.report-teaser__title {
  display: block;
  font-size: 30rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
}

.report-teaser__desc {
  display: block;
  margin-top: 6rpx;
  font-size: 22rpx;
  color: #6b7280;
  line-height: 1.4;
}

.report-teaser__btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 2rpx;
  padding: 14rpx 22rpx;
  border-radius: 999rpx;
  background: #f5f3ff;
  border: 1rpx solid #ddd6fe;
}

.report-teaser__btn-text {
  font-size: 24rpx;
  font-weight: 600;
  color: #7c3aed;
}

.report-teaser__btn-arrow {
  font-size: 28rpx;
  font-weight: 700;
  color: #7c3aed;
  line-height: 1;
  display: inline-block;
  transform: rotate(0deg);
  transition: transform 0.22s ease;

  &.is-expanded {
    transform: rotate(90deg);
  }
}

.report-detail {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  animation: report-in 0.28s ease-out;
}

@keyframes report-in {
  from {
    opacity: 0;
    transform: translateY(-10rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.block {
  padding: 24rpx 28rpx;
  border-radius: 24rpx;
  background: #fff;
  border: 1rpx solid rgba(232, 226, 217, 0.8);
  box-shadow: 0 4rpx 24rpx rgba(31, 41, 55, 0.04);
}

.block__head {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-bottom: 16rpx;
}

.block__title {
  font-size: 28rpx;
  font-weight: 700;
  color: #374151;
}

.block__text {
  display: block;
  font-size: 28rpx;
  line-height: 1.75;
  color: #44403c;
}

.block--overview {
  border-left: 6rpx solid #f06a2a;
}

.block--wrong {
  border-left: 6rpx solid #dc2626;
}

.block--tips {
  border-left: 6rpx solid #f59e0b;
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

.block__item--wrong {
  background: #fef2f2;
}

.block__item-idx {
  flex-shrink: 0;
  width: 36rpx;
  height: 36rpx;
  border-radius: 10rpx;
  background: #fee2e2;
  color: #b91c1c;
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

.tips-list {
  padding: 4rpx 0;
}

.tips-list__row {
  display: flex;
  align-items: flex-start;
  gap: 10rpx;

  & + & {
    margin-top: 12rpx;
  }
}

.tips-list__mark {
  flex-shrink: 0;
  font-size: 32rpx;
  font-weight: 700;
  color: #f06a2a;
  line-height: 1.4;
}

.tips-list__text {
  flex: 1;
  font-size: 28rpx;
  line-height: 1.65;
  color: #44403c;
}
</style>
