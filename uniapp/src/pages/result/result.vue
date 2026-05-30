<template>

  <view class="page result-page">

    <view class="page-cloud page-cloud--a" aria-hidden="true" />
    <view class="page-cloud page-cloud--b" aria-hidden="true" />

    <view class="bt-notch-safe" />

    <view class="content">

      <view class="page-header">
        <text class="page-header__title">闯关完成 🎉</text>
        <view class="page-header__sub">
          <text>太棒了！你又</text>
          <view class="page-header__highlight-wrap">
            <text class="page-header__highlight">进步</text>
            <view class="page-header__underline" />
          </view>
          <text>啦～</text>
        </view>
      </view>

      <BentoEnergyPool

        :accuracy="correctRate"

        :score="score"

        :total="total"

        @knowledge-tap="onKnowledgeTap"

      />

      <view id="knowledge-section" class="knowledge-section">
        <BentoKnowledgePanel
          v-if="!loading && knowledgePoints.length"
          v-model:expanded="knowledgeExpanded"
          :points="knowledgePoints"
        />
      </view>

      <view id="report-section" class="report-section">
        <view v-if="loading" class="skeleton skeleton--teaser">
          <view class="skeleton__head">
            <view class="sk-icon" />
            <view class="sk-title-block">
              <view class="sk-line sk-line--title" />
              <view class="sk-line sk-line--sub" />
            </view>
          </view>
        </view>
        <BentoReportCards
          v-else-if="structuredReport"
          v-model:expanded="reportExpanded"
          :report="structuredReport"
        />
        <view v-else-if="fallbackMarkdown" class="report-fallback-box">
          <ReportView :markdown="fallbackMarkdown" />
        </view>
        <text v-else class="report-fallback">暂无复盘内容</text>
      </view>



      <view class="actions">

        <button class="bt-btn-primary" @tap="playAgain">再来一局</button>

        <button class="bt-btn-secondary is-disabled" disabled>分享（MVP 暂未开放）</button>

      </view>

    </view>

    <FloatTabbar />

  </view>

</template>



<script setup lang="ts">

import { computed, onMounted, ref } from 'vue'

import BentoEnergyPool from '@/components/BentoEnergyPool.vue'

import BentoKnowledgePanel from '@/components/BentoKnowledgePanel.vue'

import BentoReportCards from '@/components/BentoReportCards.vue'

import FloatTabbar from '@/components/FloatTabbar.vue'

import ReportView from '@/components/ReportView.vue'

import { generateReport, showApiError } from '@/services/api'

import type { QuizReportRequest, StructuredMiniReport } from '@/types/quiz'

import { sanitizeReportMarkdown, stripTrailingEmptyParens } from '@/utils/reportText'

import { formatCorrectRatePercent } from '@/utils/scoring'

import { parseStructuredReport } from '@/utils/structuredReport'

import {

  clearQuizSession,

  getCurrentQuiz,

  getQuizAnswers,

} from '@/utils/storage'



const loading = ref(true)

const structuredReport = ref<StructuredMiniReport | null>(null)

const fallbackMarkdown = ref('')

const score = ref(0)

const total = ref(10)

const reportExpanded = ref(false)

const knowledgeExpanded = ref(false)



const correctRate = computed(() => formatCorrectRatePercent(score.value, total.value))

const knowledgePoints = computed(() => structuredReport.value?.corePoints ?? [])



function calcLocalScore() {

  const answers = getQuizAnswers()

  total.value = getCurrentQuiz()?.questions.length ?? 10

  score.value = answers.filter((item) => item.correct).length

}



function buildKnowledgePoints(
  session: NonNullable<ReturnType<typeof getCurrentQuiz>>,
  answers: ReturnType<typeof getQuizAnswers>,
): string[] {
  const wrongIds = new Set(answers.filter((item) => !item.correct).map((item) => item.question_id))
  const ordered = [
    ...session.questions.filter((q) => wrongIds.has(q.id)),
    ...session.questions.filter((q) => !wrongIds.has(q.id)),
  ]
  const seen = new Set<string>()
  const points: string[] = []

  for (const question of ordered) {
    const text = stripTrailingEmptyParens(question.explanation?.trim() || question.stem)
    if (!text || seen.has(text)) continue
    seen.add(text)
    points.push(text)
    if (points.length >= 5) break
  }

  return points
}

function buildLocalStructuredReport(

  session: NonNullable<ReturnType<typeof getCurrentQuiz>>,

  answers: ReturnType<typeof getQuizAnswers>,

): StructuredMiniReport {

  const totalCount = session.questions.length

  const scoreCount = answers.filter((item) => item.correct).length

  const rate = formatCorrectRatePercent(scoreCount, totalCount)

  const wrong = answers.filter((item) => !item.correct)



  return {

    overview: `本次完成 ${totalCount} 题，答对 ${scoreCount} 题，正确率 ${rate}%。`,

    corePoints: buildKnowledgePoints(session, answers),

    wrongAnalysis: wrong.slice(0, 3).map((item) => {

      const question = session.questions.find((q) => q.id === item.question_id)

      return stripTrailingEmptyParens(question?.stem ?? item.question_id)

    }),

    reviewTips: [

      '回顾错题解析，用自己的话复述关键点',

      '明天再做一组同类题巩固',

    ],

  }

}



function applyReportPayload(raw: string) {
  const parsed = parseStructuredReport(raw)

  if (parsed) {
    const previous = structuredReport.value
    structuredReport.value = {
      ...parsed,
      corePoints: parsed.corePoints.length > 0 ? parsed.corePoints : (previous?.corePoints ?? []),
      wrongAnalysis:
        parsed.wrongAnalysis.length > 0 ? parsed.wrongAnalysis : (previous?.wrongAnalysis ?? []),
      reviewTips: parsed.reviewTips.length > 0 ? parsed.reviewTips : (previous?.reviewTips ?? []),
    }
    fallbackMarkdown.value = ''
    return
  }

  if (structuredReport.value) {
    fallbackMarkdown.value = ''
    return
  }

  structuredReport.value = null
  fallbackMarkdown.value = sanitizeReportMarkdown(raw)
}



async function fetchReport() {

  const session = getCurrentQuiz()

  const answers = getQuizAnswers()

  if (!session) {

    uni.reLaunch({ url: '/pages/index/index' })

    return

  }



  if (!session.questions.length || !answers.length) {

    uni.showToast({ title: '缺少答题记录', icon: 'none' })

    setTimeout(() => uni.reLaunch({ url: '/pages/index/index' }), 600)

    return

  }



  calcLocalScore()

  structuredReport.value = buildLocalStructuredReport(session, answers)

  fallbackMarkdown.value = ''

  loading.value = false



  const payload: QuizReportRequest = {

    quiz_id: session.quiz_id,

    topic: session.topic,

    questions: session.questions,

    answers,

  }



  try {

    const res = await generateReport(payload)

    score.value = res.score

    total.value = res.total

    if (res.report?.trim()) {

      applyReportPayload(res.report.trim())

    }

  } catch (error) {
    if (!structuredReport.value) {
      showApiError(error, 'AI 复盘失败，已显示本地摘要')
    }
  }

}



function playAgain() {

  clearQuizSession()

  uni.reLaunch({ url: '/pages/index/index' })

}



function onKnowledgeTap() {
  if (!knowledgePoints.value.length) {
    uni.showToast({ title: '暂无知识点数据', icon: 'none' })
    return
  }
  knowledgeExpanded.value = true
  setTimeout(() => {
    uni.pageScrollTo({
      selector: '#knowledge-section',
      duration: 300,
    })
  }, 280)
}



onMounted(() => {

  fetchReport()

})

</script>



<style scoped lang="scss">

.page {

  min-height: 100vh;

  padding-bottom: calc(140rpx + env(safe-area-inset-bottom));

}

.result-page {
  position: relative;
  background:
    radial-gradient(ellipse 90% 50% at 50% -10%, rgba(186, 230, 253, 0.7) 0%, transparent 70%),
    radial-gradient(ellipse 60% 40% at 10% 30%, rgba(219, 234, 254, 0.5) 0%, transparent 60%),
    radial-gradient(ellipse 50% 35% at 90% 60%, rgba(224, 242, 254, 0.45) 0%, transparent 55%),
    linear-gradient(180deg, #dbeafe 0%, #eff6ff 35%, #f8fbff 100%);
  overflow: hidden;
}

.page-cloud {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.55);
  pointer-events: none;
}

.page-cloud--a {
  width: 280rpx;
  height: 120rpx;
  top: 180rpx;
  right: -40rpx;
  border-radius: 50%;
}

.page-cloud--b {
  width: 200rpx;
  height: 90rpx;
  top: 320rpx;
  left: -30rpx;
  border-radius: 50%;
}



.content {

  padding: 0 36rpx 40rpx;

}



.page-header {
  padding-top: 20rpx;
  margin-bottom: 4rpx;
}

.page-header__title {
  display: block;
  font-size: 44rpx;
  font-weight: 800;
  color: #1f2937;
  letter-spacing: 1rpx;
  line-height: 1.3;
}

.page-header__sub {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-top: 12rpx;
  font-size: 28rpx;
  color: #4b5563;
  line-height: 1.5;
}

.page-header__highlight-wrap {
  position: relative;
  display: inline-flex;
  margin: 0 2rpx;
}

.page-header__highlight {
  font-weight: 700;
  color: #1f2937;
}

.page-header__underline {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 2rpx;
  height: 10rpx;
  background: #fde047;
  border-radius: 4rpx;
  z-index: -1;
}



.report-section {
  margin-bottom: 28rpx;
}

.knowledge-section {
  margin-bottom: 4rpx;
}

.skeleton {
  background: #fff;
  border-radius: 28rpx;
  padding: 28rpx;
  box-shadow: 0 8rpx 40rpx rgba(124, 58, 237, 0.08);
  border: 1rpx solid rgba(237, 233, 254, 0.9);
}

.skeleton__head {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.skeleton--teaser .skeleton__head {
  margin-bottom: 0;
}

.sk-icon {
  width: 72rpx;
  height: 72rpx;
  border-radius: 20rpx;
  background: linear-gradient(90deg, #f3f4f6, #e5e7eb, #f3f4f6);
}

.sk-title-block {
  flex: 1;
}

.sk-line {
  height: 24rpx;
  margin-top: 16rpx;
  border-radius: 12rpx;
  background: linear-gradient(90deg, #f3f4f6, #e5e7eb, #f3f4f6);

  &--title {
    width: 45%;
    margin-top: 0;
    height: 28rpx;
  }

  &--sub {
    width: 60%;
    margin-top: 12rpx;
    height: 20rpx;
  }
}

.sk-line.short {
  width: 70%;
}

.report-fallback-box {
  background: #fff;
  border-radius: 32rpx;
  padding: 28rpx;
  box-shadow: 0 8rpx 48rpx rgba(31, 41, 55, 0.07);
}

.report-fallback {

  display: block;

  font-size: 28rpx;

  color: #6b7280;

  line-height: 1.6;

}



.actions {

  display: flex;

  flex-direction: column;

  gap: 16rpx;

}



.is-disabled {

  opacity: 0.5;

}

</style>


