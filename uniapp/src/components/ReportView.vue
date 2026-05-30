<template>

  <view class="report-view">

    <view v-for="(block, index) in blocks" :key="index" :class="block.className">

      {{ block.text }}

    </view>

  </view>

</template>



<script setup lang="ts">

import { computed } from 'vue'
import { stripTrailingEmptyParens } from '@/utils/reportText'



const props = defineProps<{

  markdown: string

}>()



type ReportBlock = { className: string; text: string }



function stripInlineMarkdown(text: string): string {
  return stripTrailingEmptyParens(text.replace(/\*\*/g, '').trim())
}



function parseListText(line: string): string | null {

  const bullet = line.match(/^[-*]\s+(.+)$/)

  if (bullet) return stripInlineMarkdown(bullet[1])

  const ordered = line.match(/^\d+\.\s+(.+)$/)

  if (ordered) return stripInlineMarkdown(ordered[1])

  return null

}



function parseMarkdownBlocks(markdown: string): ReportBlock[] {

  const blocks: ReportBlock[] = []



  for (const rawLine of markdown.split(/\r?\n/)) {

    const trimmed = rawLine.trim()

    if (!trimmed) continue



    if (trimmed.startsWith('### ')) {

      blocks.push({ className: 'report-h3', text: stripInlineMarkdown(trimmed.slice(4)) })

      continue

    }

    if (trimmed.startsWith('## ')) {

      blocks.push({ className: 'report-h2', text: stripInlineMarkdown(trimmed.slice(3)) })

      continue

    }

    if (trimmed.startsWith('# ')) {

      blocks.push({ className: 'report-h2', text: stripInlineMarkdown(trimmed.slice(2)) })

      continue

    }



    const listText = parseListText(trimmed)

    if (listText) {

      blocks.push({ className: 'report-li', text: `• ${listText}` })

      continue

    }



    blocks.push({ className: 'report-p', text: stripInlineMarkdown(trimmed) })

  }



  return blocks

}



const blocks = computed(() => parseMarkdownBlocks(props.markdown))

</script>



<style scoped lang="scss">

.report-h2 {

  display: block;

  font-size: 32rpx;

  font-weight: 700;

  margin: 28rpx 0 12rpx;

  color: #1f2937;



  &:first-child {

    margin-top: 0;

  }

}



.report-h3 {

  display: block;

  font-size: 30rpx;

  font-weight: 700;

  margin: 16rpx 0 8rpx;

  color: #1f2937;

}



.report-p {

  display: block;

  font-size: 28rpx;

  line-height: 1.7;

  color: #374151;

  margin-bottom: 12rpx;

}



.report-li {

  display: block;

  font-size: 28rpx;

  line-height: 1.7;

  color: #374151;

  margin-bottom: 10rpx;

  padding-left: 8rpx;

}

</style>


