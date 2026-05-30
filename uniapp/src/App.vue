<script setup lang="ts">
import { onLaunch } from '@dcloudio/uni-app'
import { initFeedbackAudio } from '@/utils/feedbackSound'
import { loadDisplayFont } from '@/utils/fonts'

onLaunch(() => {
  initFeedbackAudio()
  // 临时禁用装饰性手写字体加载，排查微信开发者工具中字体解码/加载导致的渲染空白问题
  // loadDisplayFont()
})
</script>

<style lang="scss">
@import '@/styles/bento.scss';
</style>
