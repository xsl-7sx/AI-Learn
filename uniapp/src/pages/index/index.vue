<template>
  <view class="page home bt-screen">
    <view class="home-topbar" :style="layoutStyle.header">
      <view class="home-user">
        <view class="home-avatar">👤</view>
        <view class="home-user-text">
          <text class="home-greet">你好，<text class="strong">小皮</text> 👋</text>
          <text class="home-sub">今天也要元气满满哦！</text>
        </view>
      </view>
      <view v-if="!layoutMetrics.isMpWeixin" class="home-topbar-actions">
        <view class="home-streak">🔥 <text class="strong">7</text></view>
        <view class="home-icon-btn">📅</view>
      </view>
      <view v-else class="home-streak home-streak--capsule">🔥 <text class="strong">7</text></view>
    </view>

    <scroll-view class="home-scroll" scroll-y :style="layoutStyle.scroll">
      <view class="home-hero">
        <text class="home-title">今天想闯哪一关？</text>
        <view class="home-title-line" />
      </view>

      <view class="home-input-card">
        <text class="home-input-label">输入你想学的内容</text>
        <view class="home-textarea-wrap">
          <textarea
            v-model="topic"
            class="home-textarea"
            placeholder="例如：我想搞懂 RAG：检索、增强、生成各解决什么问题"
            maxlength="500"
            :auto-height="true"
          />
          <text class="home-pencil">✏️</text>
        </view>

        <view class="home-suggest-row">
          <text class="home-suggest-label">试试这些</text>
          <view class="home-suggest-pills">
            <view
              v-for="item in quickTopics"
              :key="item.title"
              class="home-pill"
              @tap="pickTopic(item.title)"
            >
              {{ item.title }}
            </view>
          </view>
          <view class="home-shuffle" @tap="shuffleTopics">
            <text class="shuffle-icon">↻</text>
            <text>换一换</text>
          </view>
        </view>

        <button class="home-btn-generate" :disabled="!canSubmit" @tap="startQuiz">
          <text class="btn-main">开始生成题目 →</text>
          <text class="btn-sub">AI 为你生成专属题目</text>
        </button>
        <button v-if="USE_MOCK" class="home-mock-btn" @tap="startMock">Mock 跳过 API</button>
      </view>

      <view class="home-section-hd">
        <text>热门主题</text>
        <text class="link" @tap="shuffleTopics">换一批 ›</text>
      </view>
      <view class="home-topic-wrap">
        <scroll-view
          class="home-topic-row"
          scroll-x
          enable-flex
          :show-scrollbar="false"
          :enhanced="true"
        >
          <view class="home-topic-track">
            <view
              v-for="item in currentTopics"
              :key="item.title"
              class="home-topic"
              :style="layoutStyle.topicCard"
              @tap="pickTopic(item.title)"
            >
              <view :class="['home-topic-icon', `home-topic-icon--${item.tone}`]">
                {{ item.icon || '✦' }}
              </view>
              <text class="home-topic-title">{{ item.title }}</text>
              <text v-if="item.desc" class="home-topic-desc">{{ item.desc }}</text>
              <text class="home-topic-heat">🔥 热度 {{ item.heat }}</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <view class="home-section-hd home-section-hd--gap">
        <text>未完成关卡</text>
        <text class="link">查看全部 ›</text>
      </view>
      <view class="home-level-card" @tap="continueQuiz">
        <view class="home-level-main">
          <view class="home-level-cover">📖</view>
          <view class="home-level-body">
            <view class="home-level-title-row">
              <text class="home-level-title">RAG 基础概念入门</text>
              <text class="home-level-tag">第 3 关</text>
            </view>
            <text class="home-level-desc">检索增强生成入门：理解检索、增强、生成如何协同。</text>
            <view class="home-level-progress-row">
              <view class="home-progress-bar">
                <view class="home-progress-fill" style="width: 60%" />
              </view>
              <text class="home-level-progress-txt">进度 6/10</text>
            </view>
          </view>
        </view>
        <button class="home-level-continue" @tap.stop="continueQuiz">继续</button>
      </view>

      <view class="bottom-spacer" />
    </scroll-view>

    <FloatTabbar />
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import FloatTabbar from '@/components/FloatTabbar.vue'
import mockQuiz from '@/mock/quiz.json'
import { USE_MOCK } from '@/config'
import { TOPIC_BATCHES } from '@/utils/topics'
import { getLayoutMetrics, layoutMetricsToStyle } from '@/utils/layout'
import { getCurrentQuiz, getQuizProgress, setCurrentQuiz, setPendingTopic } from '@/utils/storage'
import type { GenerateQuizResponse } from '@/types/quiz'

const topic = ref('')
const batchIndex = ref(0)
const currentTopics = computed(() => TOPIC_BATCHES[batchIndex.value])
const quickTopics = computed(() => currentTopics.value.slice(0, 3))
const layoutMetrics = ref(getLayoutMetrics())
const layoutStyle = computed(() => layoutMetricsToStyle(layoutMetrics.value))

const canSubmit = computed(() => topic.value.trim().length >= 2)

function refreshLayout() {
  layoutMetrics.value = getLayoutMetrics()
}

onMounted(refreshLayout)

function shuffleTopics() {
  batchIndex.value = (batchIndex.value + 1) % TOPIC_BATCHES.length
}

function pickTopic(title: string) {
  topic.value = title
}

function goLoading() {
  setPendingTopic(topic.value.trim())
  uni.navigateTo({ url: '/pages/loading/loading' })
}

function startQuiz() {
  if (!canSubmit.value) {
    uni.showToast({ title: '再多写几个字哦', icon: 'none' })
    return
  }
  goLoading()
}

function startMock() {
  setCurrentQuiz(mockQuiz as GenerateQuizResponse)
  uni.redirectTo({ url: '/pages/quiz/quiz' })
}

function continueQuiz() {
  const session = getCurrentQuiz()
  if (!session) {
    uni.showToast({ title: '暂无未完成关卡', icon: 'none' })
    return
  }
  const index = getQuizProgress()
  if (index >= session.questions.length) {
    uni.navigateTo({ url: '/pages/result/result' })
    return
  }
  uni.navigateTo({ url: '/pages/quiz/quiz' })
}
</script>

<style scoped lang="scss">
.page {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100vw;
  min-height: 100vh;
  overflow-x: hidden;
  padding-bottom: calc(150rpx + env(safe-area-inset-bottom));
}

.home-topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
  padding-left: 32rpx;
  padding-bottom: 8rpx;
  box-sizing: border-box;
}

.home-user {
  display: flex;
  align-items: center;
  gap: 20rpx;
  flex: 1;
  min-width: 0;
}

.home-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  background: linear-gradient(145deg, #fde68a, #fbbf24);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  flex-shrink: 0;
  box-shadow: 0 6rpx 20rpx rgba(251, 191, 36, 0.35);
}

.home-user-text {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
  min-width: 0;
}

.home-greet {
  font-size: 34rpx;
  font-weight: 700;
  color: #1c1917;
  line-height: 1.3;
}

.home-sub {
  font-size: 24rpx;
  color: #9ca3af;
  line-height: 1.3;
}

.strong {
  font-weight: 700;
  color: #1c1917;
}

.home-topbar-actions {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex-shrink: 0;
}

.home-streak {
  background: #fff7ed;
  color: #ea580c;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  flex-shrink: 0;
}

.home-streak--capsule {
  align-self: center;
}

.home-icon-btn {
  width: 72rpx;
  height: 72rpx;
  border-radius: 24rpx;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.home-scroll {
  flex: 1;
  min-height: 0;
  width: 100%;
  padding: 0 32rpx;
  overflow-x: hidden;
  box-sizing: border-box;
}

.home-hero {
  margin-bottom: 28rpx;
}

.home-title {
  display: block;
  font-size: 52rpx;
  font-weight: 800;
  color: #1c1917;
  line-height: 1.25;
  letter-spacing: 1rpx;
}

.home-title-line {
  width: 120rpx;
  height: 10rpx;
  margin-top: 12rpx;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #ff7e3d, #ffb07c);
}

.home-input-card {
  width: 100%;
  background: #fff;
  border-radius: 32rpx;
  padding: 32rpx 28rpx;
  box-shadow: 0 12rpx 48rpx rgba(31, 41, 55, 0.08);
  margin-bottom: 40rpx;
  overflow: hidden;
}

.home-input-label {
  display: block;
  font-size: 28rpx;
  color: #6b7280;
  margin-bottom: 20rpx;
}

.home-textarea-wrap {
  position: relative;
  margin-bottom: 24rpx;
}

.home-textarea {
  width: 100%;
  min-height: 180rpx;
  padding: 24rpx 56rpx 24rpx 24rpx;
  background: #f5f4f2;
  border-radius: 24rpx;
  font-size: 28rpx;
  line-height: 1.65;
  color: #374151;
}

.home-pencil {
  position: absolute;
  right: 20rpx;
  bottom: 20rpx;
  font-size: 28rpx;
  opacity: 0.55;
}

.home-suggest-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 28rpx;
}

.home-suggest-label {
  font-size: 24rpx;
  color: #9ca3af;
  flex-shrink: 0;
}

.home-suggest-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  flex: 1;
  min-width: 0;
}

.home-pill {
  padding: 10rpx 20rpx;
  border-radius: 999rpx;
  background: #fff7ed;
  color: #c2410c;
  font-size: 24rpx;
  border: 1rpx solid #fed7aa;
}

.home-shuffle {
  display: flex;
  align-items: center;
  gap: 6rpx;
  flex-shrink: 0;
  font-size: 24rpx;
  color: #9ca3af;
}

.shuffle-icon {
  font-size: 28rpx;
}

.home-btn-generate {
  width: 100%;
  padding: 24rpx 0;
  border-radius: 999rpx;
  background: linear-gradient(135deg, #ff7e3d 0%, #ff9f5a 100%);
  color: #fff;
  box-shadow: 0 12rpx 32rpx rgba(255, 126, 61, 0.38);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
}

.home-btn-generate[disabled] {
  opacity: 0.5;
  box-shadow: none;
}

.btn-main {
  font-size: 32rpx;
  font-weight: 700;
  line-height: 1.3;
}

.btn-sub {
  font-size: 22rpx;
  opacity: 0.9;
  line-height: 1.3;
}

.home-mock-btn {
  margin-top: 16rpx;
  width: 100%;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 26rpx;
  line-height: 80rpx;
  border-radius: 999rpx;
}

.home-section-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  width: 100%;
  margin-bottom: 24rpx;
  font-size: 32rpx;
  font-weight: 700;
  color: #1c1917;
}

.home-section-hd--gap {
  margin-top: 40rpx;
}

.link {
  flex-shrink: 0;
  color: #9ca3af;
  font-size: 26rpx;
  font-weight: 500;
}

.home-topic-wrap {
  width: 100%;
  overflow: hidden;
  margin-bottom: 8rpx;
}

.home-topic-row {
  width: 100%;
  height: 300rpx;
  white-space: nowrap;
}

.home-topic-track {
  display: inline-flex;
  flex-direction: row;
  flex-wrap: nowrap;
  height: 100%;
  padding: 8rpx 0 20rpx;
  gap: 16rpx;
}

.home-topic {
  display: inline-flex;
  flex-direction: column;
  flex-shrink: 0;
  min-height: 280rpx;
  padding: 24rpx 20rpx;
  border-radius: 24rpx;
  background: #fff;
  box-shadow: 0 8rpx 28rpx rgba(31, 41, 55, 0.07);
  vertical-align: top;
}

.home-topic-icon {
  width: 64rpx;
  height: 64rpx;
  border-radius: 18rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  margin-bottom: 16rpx;
}

.home-topic-icon--orange { background: #ffedd5; }
.home-topic-icon--blue { background: #dbeafe; }
.home-topic-icon--mint { background: #d1fae5; }
.home-topic-icon--lavender { background: #ede9fe; }

.home-topic-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.35;
  margin-bottom: 8rpx;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.home-topic-desc {
  flex: 1;
  font-size: 22rpx;
  color: #9ca3af;
  line-height: 1.45;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.home-topic-heat {
  margin-top: 12rpx;
  font-size: 22rpx;
  color: #ea580c;
  font-weight: 600;
}

.home-level-card {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  width: 100%;
  padding: 28rpx 24rpx;
  border-radius: 28rpx;
  background: #fff;
  box-shadow: 0 8rpx 32rpx rgba(31, 41, 55, 0.07);
  overflow: hidden;
}

.home-level-main {
  display: flex;
  align-items: flex-start;
  gap: 20rpx;
  width: 100%;
  min-width: 0;
}

.home-level-cover {
  width: 96rpx;
  height: 96rpx;
  border-radius: 24rpx;
  background: linear-gradient(145deg, #fff7ed, #ffedd5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44rpx;
  flex-shrink: 0;
}

.home-level-body {
  flex: 1;
  min-width: 0;
}

.home-level-title-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8rpx 12rpx;
  margin-bottom: 16rpx;
}

.home-level-title {
  font-size: 28rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.3;
}

.home-level-tag {
  font-size: 20rpx;
  color: #ea580c;
  background: #fff7ed;
  padding: 4rpx 12rpx;
  border-radius: 999rpx;
}

.home-progress-bar {
  height: 12rpx;
  border-radius: 999rpx;
  background: #f3f0ea;
  overflow: hidden;
}

.home-progress-fill {
  height: 100%;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #ff7e3d, #ffb07c);
}

.home-level-desc {
  display: block;
  margin-bottom: 16rpx;
  font-size: 24rpx;
  color: #6b7280;
  line-height: 1.5;
}

.home-level-progress-row {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.home-level-progress-txt {
  font-size: 24rpx;
  color: #6b7280;
}

.home-level-continue {
  align-self: flex-end;
  margin: 0;
  padding: 0 32rpx;
  min-width: 120rpx;
  height: 64rpx;
  line-height: 64rpx;
  background: #fff0e8;
  color: #ff7e3d;
  font-size: 26rpx;
  font-weight: 600;
  border-radius: 999rpx;
}

.bottom-spacer {
  height: 48rpx;
}
</style>
