<script setup lang="ts">
import { onLaunch } from '@dcloudio/uni-app'
import { loadDisplayFont } from '@/utils/fonts'

onLaunch(() => {
  loadDisplayFont()
})
</script>

<style lang="scss">
@import '@/styles/bento.scss';
</style>
