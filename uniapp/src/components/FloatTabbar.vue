<template>
  <view class="bt-tabbar bt-tabbar-float">
    <view class="bt-tab is-active">
      <text class="bt-tab-icon">🚩</text>
      <text>闯关</text>
    </view>
    <view class="bt-tab is-disabled">
      <text class="bt-tab-icon">📚</text>
      <text>题库</text>
    </view>
    <view class="bt-tab is-disabled">
      <text class="bt-tab-icon">🏅</text>
      <text>勋章</text>
    </view>
  </view>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.bt-tabbar-float {
  position: fixed;
  left: 0;
  right: 0;
  width: 100%;
  max-width: 100vw;
  bottom: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 16rpx 32rpx calc(16rpx + env(safe-area-inset-bottom));
  background: #fff;
  box-shadow: 0 -4rpx 24rpx rgba(31, 41, 55, 0.06);
  border-top: 1rpx solid rgba(232, 226, 217, 0.6);
  box-sizing: border-box;
}

.bt-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
  min-width: 120rpx;
  padding: 12rpx 24rpx;
  border-radius: 999rpx;
  font-size: 22rpx;
  color: #9ca3af;
}

.bt-tab.is-active {
  background: #fff0e8;
  color: #ff7e3d;
  font-weight: 600;
}

.bt-tab.is-disabled {
  opacity: 0.55;
}

.bt-tab-icon {
  font-size: 28rpx;
  line-height: 1;
}
</style>
