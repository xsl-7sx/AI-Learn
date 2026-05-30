<template>
  <view class="bt-tabbar bt-tabbar-float">
    <view class="bt-tab is-active">
      <AppIcon name="flag" :size="32" color="#ff7e3d" />
      <text>闯关</text>
    </view>
    <view class="bt-tab is-disabled">
      <AppIcon name="library" :size="32" color="#9ca3af" />
      <text>题库</text>
    </view>
    <view class="bt-tab is-disabled">
      <AppIcon name="medal" :size="32" color="#9ca3af" />
      <text>勋章</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import AppIcon from '@/components/AppIcon.vue'

defineOptions({
  virtualHost: true,
})
</script>

<style scoped lang="scss">
.bt-tabbar-float {
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 100%;
  padding: 12rpx 20rpx;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 8rpx 32rpx rgba(31, 41, 55, 0.1);
  border: 1rpx solid rgba(232, 226, 217, 0.55);
  border-radius: 999rpx;
  box-sizing: border-box;
}

.bt-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
  min-width: 100rpx;
  padding: 10rpx 20rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
  color: #9ca3af;
}

.bt-tab.is-active {
  background: linear-gradient(180deg, #fff7f0 0%, #ffede0 100%);
  color: #ff7e3d;
  font-weight: 600;
}

.bt-tab.is-disabled {
  opacity: 0.55;
}
</style>
