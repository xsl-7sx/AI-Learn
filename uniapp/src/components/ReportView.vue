<template>
  <view class="report-view">
    <!-- #ifdef MP-WEIXIN -->
    <towxml v-if="nodes" :nodes="nodes" />
    <!-- #endif -->
    <template v-if="!nodes">
      <view v-for="(block, index) in blocks" :key="index" :class="block.className">
        {{ block.text }}
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { markdownToNodes } from '@/utils/towxml'

const props = defineProps<{
  markdown: string
}>()

const nodes = computed(() => markdownToNodes(props.markdown))

const blocks = computed(() => {
  return props.markdown
    .split(/\n{2,}/)
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      if (part.startsWith('## ')) {
        return { className: 'report-h2', text: part.replace(/^##\s+/, '') }
      }
      if (part.startsWith('# ')) {
        return { className: 'report-h2', text: part.replace(/^#\s+/, '') }
      }
      if (part.startsWith('- ')) {
        return { className: 'report-li', text: part.replace(/^-\s+/, '• ') }
      }
      return { className: 'report-p', text: part.replace(/\*\*/g, '') }
    })
})
</script>

<style scoped lang="scss">
.report-h2 {
  display: block;
  font-size: 32rpx;
  font-weight: 700;
  margin: 20rpx 0 12rpx;
  color: #1f2937;
}

.report-p,
.report-li {
  display: block;
  font-size: 28rpx;
  line-height: 1.7;
  color: #374151;
  margin-bottom: 12rpx;
  white-space: pre-wrap;
}
</style>
