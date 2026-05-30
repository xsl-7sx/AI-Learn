<template>
  <image
    class="app-icon"
    :src="src"
    :style="wrapStyle"
    mode="aspectFit"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getIconDataUrl, type IconName } from '@/utils/icons'

const props = withDefaults(
  defineProps<{
    name: IconName
    size?: number
    color?: string
    strokeWidth?: number
  }>(),
  {
    size: 40,
    color: '#374151',
    strokeWidth: 2,
  },
)

const src = computed(() => getIconDataUrl(props.name, props.color, props.strokeWidth))

const wrapStyle = computed(() => ({
  width: `${props.size}rpx`,
  height: `${props.size}rpx`,
  flexShrink: 0,
}))
</script>

<style scoped lang="scss">
.app-icon {
  display: block;
}
</style>
