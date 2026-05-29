<template>
  <view class="page home bt-screen">
    <view class="home-topbar" :style="layoutStyle.header">
      <view class="home-topbar-inner" :style="layoutStyle.topbarInner">
        <view class="home-user">
          <view :class="['home-avatar', { 'home-avatar--mp': layoutMetrics.isMpWeixin }]">
            <AppIcon name="user" :size="layoutMetrics.isMpWeixin ? 32 : 40" color="#b45309" />
          </view>
          <view class="home-user-text">
            <text class="home-brand">知练</text>
            <text class="home-greet">你好，<text class="strong">小皮</text> 👋</text>
          </view>
        </view>
        <view v-if="!layoutMetrics.isMpWeixin" class="home-topbar-actions">
          <view class="home-streak">
            <AppIcon name="flame" :size="28" color="#ea580c" />
            <text class="strong">7</text>
          </view>
          <view class="home-icon-btn">
            <AppIcon name="calendar" :size="36" color="#78716c" />
          </view>
        </view>
        <view v-else class="home-streak home-streak--capsule" :style="layoutStyle.streak">
          <AppIcon name="flame" :size="28" color="#ea580c" />
          <text class="strong">7</text>
        </view>
      </view>
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
            placeholder-class="home-textarea-ph"
            placeholder="例如：我想搞懂 RAG：检索、增强、生成各解决什么问题"
            maxlength="500"
            :auto-height="true"
          />
          <AppIcon class="home-pencil" name="pencil" :size="32" color="#f06a2a" />
        </view>

        <view class="home-suggest-row">
          <view class="home-suggest-label">
            <text>试试这些</text>
            <AppIcon name="play" :size="16" color="#9ca3af" />
          </view>
          <view class="home-suggest-pills-wrap">
            <scroll-view
              class="home-suggest-pills-scroll"
              scroll-x
              :show-scrollbar="false"
              :enhanced="true"
            >
              <view class="home-suggest-pills-track">
                <view
                  v-for="item in quickTopics"
                  :key="item.title"
                  class="home-pill"
                  @tap="pickTopic(item.title)"
                >
                  {{ item.title }}
                </view>
              </view>
            </scroll-view>
            <view class="home-suggest-fade" />
          </view>
          <view class="home-shuffle" @tap="shuffleTopics">
            <AppIcon name="refresh-cw" :size="24" color="#9ca3af" />
            <text>换一换</text>
          </view>
        </view>

        <view
          class="home-btn-generate"
          :class="{ 'is-disabled': !canSubmit }"
          @tap="startQuiz"
        >
          <view class="btn-main-row">
            <text class="btn-main">开始生成题目</text>
            <AppIcon name="arrow-right" :size="30" color="#ffffff" />
          </view>
          <text class="btn-sub">AI 为你生成专属题目</text>
        </view>
        <button v-if="USE_MOCK" class="home-mock-btn" @tap="startMock">Mock 跳过 API</button>
      </view>

      <view class="home-section-hd">
        <text>热门主题</text>
        <view class="link" @tap="shuffleTopics">
          <text>换一批</text>
          <AppIcon name="refresh-cw" :size="24" color="#9ca3af" />
        </view>
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
                <AppIcon
                  :name="item.icon || 'layers'"
                  :size="32"
                  :color="topicIconColor(item.tone)"
                />
              </view>
              <text class="home-topic-title">{{ item.title }}</text>
              <text v-if="item.desc" class="home-topic-desc">{{ item.desc }}</text>
              <view class="home-topic-heat">
                <AppIcon name="flame" :size="22" color="#ea580c" />
                <text>热度 {{ item.heat }}</text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>

      <view class="home-section-hd home-section-hd--gap">
        <text>未完成关卡</text>
        <view class="link">
          <text>查看全部</text>
          <AppIcon name="chevron-right" :size="24" color="#9ca3af" />
        </view>
      </view>
      <view class="home-level-card" @tap="continueQuiz">
        <view class="home-level-main">
          <view class="home-level-cover">
            <AppIcon name="book-open" :size="48" color="#ea580c" />
          </view>
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
        <view class="home-level-continue" @tap.stop="continueQuiz">继续</view>
      </view>

      <view class="bottom-spacer" />
    </scroll-view>

    <FloatTabbar />
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import AppIcon from '@/components/AppIcon.vue'
import FloatTabbar from '@/components/FloatTabbar.vue'
import mockQuiz from '@/mock/quiz.json'
import { USE_MOCK } from '@/config'
import { TOPIC_BATCHES } from '@/utils/topics'
import { TONE_ICON_COLORS } from '@/utils/icons'
import { getLayoutMetrics, layoutMetricsToStyle } from '@/utils/layout'
import { beginQuizSession, getCurrentQuiz, getQuizProgress, setPendingTopic } from '@/utils/storage'
import type { GenerateQuizResponse } from '@/types/quiz'

const topic = ref('')
const batchIndex = ref(0)
const currentTopics = computed(() => TOPIC_BATCHES[batchIndex.value])
const quickTopics = computed(() => currentTopics.value.slice(0, 2))
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

function topicIconColor(tone: string) {
  return TONE_ICON_COLORS[tone] || '#374151'
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
  beginQuizSession(mockQuiz as GenerateQuizResponse)
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
  width: 100%;
  padding-left: 32rpx;
  box-sizing: border-box;
}

.home-topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 16rpx;
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
  flex-shrink: 0;
  box-shadow: 0 6rpx 20rpx rgba(251, 191, 36, 0.35);
}

.home-avatar--mp {
  width: 64rpx;
  height: 64rpx;
  font-size: 28rpx;
}

.home-user-text {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
  min-width: 0;
}

.home-brand {
  font-family: var(--font-body);
  font-size: 22rpx;
  font-weight: 600;
  color: #ea580c;
  letter-spacing: 2rpx;
  line-height: 1.3;
}

.home-greet {
  font-family: var(--font-display);
  font-size: 30rpx;
  font-weight: 700;
  color: #1c1917;
  line-height: 1.35;
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6rpx;
  background: #fff7ed;
  color: #ea580c;
  padding: 0 18rpx;
  border-radius: 999rpx;
  font-size: 24rpx;
  flex-shrink: 0;
  box-sizing: border-box;
}

.home-streak--capsule {
  padding: 0 16rpx;
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
  margin-top: 0;
  margin-bottom: 36rpx;
}

.home-title {
  display: block;
  font-family: var(--font-display);
  font-size: 52rpx;
  font-weight: 800;
  color: #1c1917;
  line-height: 1.3;
  letter-spacing: 1rpx;
}

.home-title-line {
  width: 80rpx;
  height: 12rpx;
  margin-top: 10rpx;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #ff7e3d, #ffb07c);
}

.home-input-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 32rpx;
  padding: 32rpx 28rpx;
  box-shadow: 0 12rpx 40rpx rgba(68, 45, 32, 0.1);
  margin-bottom: 40rpx;
  overflow: hidden;
  border: 1rpx solid rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
}

.home-input-label {
  display: block;
  font-family: var(--font-body);
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
  padding: 36rpx 80rpx 36rpx 36rpx;
  background: linear-gradient(135deg, #fffbf7 0%, #fff7ed 100%);
  border-radius: 24rpx;
  border: 1rpx solid rgba(251, 146, 60, 0.18);
  font-family: var(--font-display);
  font-size: 28rpx;
  font-weight: 400;
  line-height: 1.65;
  color: #374151;
  box-sizing: border-box;
}

.home-pencil {
  position: absolute;
  right: 24rpx;
  bottom: 24rpx;
}

.home-suggest-label {
  display: inline-flex;
  align-items: center;
  gap: 4rpx;
  height: 48rpx;
  font-family: var(--font-body);
  font-size: 24rpx;
  color: #9ca3af;
  flex-shrink: 0;
}

.home-pill {
  display: inline-flex;
  align-items: center;
  padding: 8rpx 12rpx;
  border-radius: 999rpx;
  background: #fff7ed;
  color: #c2410c;
  font-family: var(--font-body);
  font-size: 20rpx;
  font-weight: 500;
  border: 1rpx solid #fed7aa;
  flex-shrink: 0;
  white-space: nowrap;
}

.home-shuffle {
  display: flex;
  align-items: center;
  gap: 6rpx;
  flex-shrink: 0;
  margin-left: 24rpx;
  padding-left: 4rpx;
  font-family: var(--font-body);
  font-size: 24rpx;
  color: #9ca3af;
}

.home-suggest-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 32rpx;
}

.home-suggest-pills-wrap {
  position: relative;
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.home-suggest-pills-scroll {
  width: 100%;
  white-space: nowrap;
}

.home-suggest-pills-track {
  display: inline-flex;
  align-items: center;
  gap: 12rpx;
  padding-right: 16rpx;
}

.home-suggest-fade {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 40rpx;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.96) 100%);
  pointer-events: none;
}

.btn-main-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
}

.home-btn-generate {
  width: 100%;
  padding: 26rpx 0;
  border-radius: 999rpx;
  background: linear-gradient(180deg, #ff9f5a 0%, #f06a2a 52%, #e85a1a 100%);
  box-shadow: 0 12rpx 32rpx rgba(232, 90, 26, 0.38);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
}

.home-btn-generate.is-disabled {
  opacity: 0.5;
  box-shadow: none;
}

.btn-main {
  font-family: var(--font-body);
  font-size: 32rpx;
  font-weight: 700;
  line-height: 1.3;
  color: #ffffff;
}

.btn-sub {
  font-family: var(--font-body);
  font-size: 22rpx;
  line-height: 1.3;
  color: rgba(255, 255, 255, 0.92);
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
  margin-bottom: 20rpx;
  font-family: var(--font-display);
  font-size: 32rpx;
  font-weight: 700;
  color: #1c1917;
}

.home-section-hd--gap {
  margin-top: 40rpx;
}

.link {
  display: inline-flex;
  align-items: center;
  gap: 4rpx;
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
  height: 320rpx;
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
  padding: 22rpx 16rpx;
  border-radius: 24rpx;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 8rpx 24rpx rgba(68, 45, 32, 0.08);
  border: 1rpx solid rgba(255, 255, 255, 0.8);
  vertical-align: top;
  box-sizing: border-box;
}

.home-topic-icon {
  width: 56rpx;
  height: 56rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-bottom: 14rpx;
}

.home-topic-icon--orange { background: #ffedd5; }
.home-topic-icon--blue { background: #dbeafe; }
.home-topic-icon--mint { background: #d1fae5; }
.home-topic-icon--lavender { background: #ede9fe; }

.home-topic-title {
  font-family: var(--font-display);
  font-size: 24rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.45;
  margin-bottom: 8rpx;
  min-height: 70rpx;
  overflow: hidden;
  word-break: break-word;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.home-topic-desc {
  flex: 1;
  font-family: var(--font-display);
  font-size: 20rpx;
  font-weight: 400;
  color: #9ca3af;
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.home-topic-heat {
  display: flex;
  align-items: center;
  gap: 6rpx;
  margin-top: 12rpx;
  font-family: var(--font-body);
  font-size: 22rpx;
  color: #ea580c;
  font-weight: 600;
}

.home-level-card {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  width: 100%;
  max-width: 100%;
  padding: 28rpx 24rpx;
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 8rpx 28rpx rgba(68, 45, 32, 0.08);
  overflow: hidden;
  box-sizing: border-box;
  border: 1rpx solid rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
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
  font-family: var(--font-display);
  font-size: 28rpx;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.35;
}

.home-level-tag {
  font-family: var(--font-body);
  font-size: 20rpx;
  color: #ea580c;
  background: #fff7ed;
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
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
  font-family: var(--font-display);
  font-size: 24rpx;
  font-weight: 400;
  color: #6b7280;
  line-height: 1.5;
}

.home-level-progress-row {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.home-level-progress-txt {
  font-family: var(--font-body);
  font-size: 24rpx;
  color: #6b7280;
}

.home-level-continue {
  align-self: flex-end;
  padding: 10rpx 28rpx;
  border-radius: 999rpx;
  background: #fff0e8;
  color: #ff7e3d;
  font-family: var(--font-body);
  font-size: 26rpx;
  font-weight: 600;
}

.bottom-spacer {
  height: calc(200rpx + env(safe-area-inset-bottom));
}
</style>

<style lang="scss">
.home-textarea-ph {
  font-family: 'LXGW WenKai Screen', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 28rpx;
  font-weight: 400;
  color: #9ca3af;
  line-height: 1.65;
}
</style>
