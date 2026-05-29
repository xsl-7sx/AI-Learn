# 知练（KnowPractice）— MVP 前端实现指引

> **文档性质：** uni-app 小程序开发规格（Sprint 2–4 执行依据）。  
> **上级文档：** [MVP开发实施指南.md](./MVP开发实施指南.md)

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-29 | 初版：页面、组件、storage、UI 映射、交互检查表 |
| v1.1.0 | 2026-05-29 | 首页参考稿 UI 落地；layout 多机型顶栏适配；文档同步仓库结构 |

---

## 一、技术栈与初始化

| 项 | 决策 |
| -- | ---- |
| 框架 | uni-app + Vue 3 + TypeScript + Vite CLI |
| IDE | Cursor / VS Code + 微信开发者工具（不用 HBuilderX） |
| 状态 | Composition API + `ref/reactive`，**不引入 Pinia** |
| Markdown | towxml（Sprint 4）；备选 B：`\n\n` 分段 `<view>` |

**初始化命令：**

```bash
npx degit dcloudio/uni-preset-vue#vite-ts uniapp
cd uniapp && npm install
npm run dev:mp-weixin
```

微信开发者工具导入：`uniapp/dist/dev/mp-weixin`（以终端编译日志为准）。

---

## 二、页面路由（`pages.json`）

| 页面 | 路径 | 原型 | 职责 |
| ---- | ---- | ---- | ---- |
| 首页 | `pages/index/index` | [01 屏①](../prototypes/01_mvp_core.html) | 输入 topic + 开始生成 |
| 生成中 | `pages/loading/loading` | 01 屏② | 心理学进度条 + 调 API |
| 答题 | `pages/quiz/quiz` | 01 屏③–⑦ | 单题闯关 1/10 |
| 结算 | `pages/result/result` | 01 屏⑧–⑨ | 正确率 + AI 复盘 |

**跳转关系：**

```
index → loading → quiz → result → index（再来一局）
```

**禁止：** 通过 URL query 传递题目 JSON；统一使用 `uni.storage`。

---

## 三、目录结构

```
uniapp/src/
├── pages/
│   ├── index/index.vue
│   ├── loading/loading.vue
│   ├── quiz/quiz.vue
│   └── result/result.vue
├── components/
│   ├── QuestionCard.vue      # 题干展示
│   ├── OptionList.vue        # 选项 / 判断按钮
│   ├── FeedbackPanel.vue     # 对错反馈 + 解析
│   └── ReportView.vue        # Markdown 渲染（towxml 或备选 B）
├── services/
│   └── api.ts                # generateQuiz / generateReport
├── utils/
│   ├── scoring.ts            # 本地判分
│   ├── storage.ts            # 三 key 读写封装
│   ├── topics.ts             # 热门主题批次
│   └── layout.ts             # 顶栏/胶囊安全区适配
├── types/
│   └── quiz.ts               # snake_case 类型
├── styles/
│   └── bento.scss            # 从原型提取的 --bt-* Token
└── mock/
    └── quiz.json             # Sprint 2 Mock 数据
```

---

## 四、Storage 三 Key

| Key | 内容 | 写入时机 | 清除时机 |
| --- | ---- | -------- | -------- |
| `currentQuiz` | `{ quiz_id, topic, questions }` | loading 收到 generate 响应 | 再来一局 |
| `quizAnswers` | `UserAnswer[]` | 每答一题追加 | 再来一局 |
| `quizProgress` | `{ index: number }` | 每题推进 | 再来一局 |

```typescript
// utils/storage.ts — 再来一局（禁止 clearStorage）
export function clearQuizSession(): void {
  uni.removeStorageSync('currentQuiz')
  uni.removeStorageSync('quizAnswers')
  uni.removeStorageSync('quizProgress')
}
```

> **quiz 页 `onShow`：** 必须从 storage 恢复 `quizProgress` 与 `quizAnswers`，防止误触返回丢进度。

---

## 五、本地判分（`utils/scoring.ts`）

```typescript
function isMultipleChoiceCorrect(selected: number[], answer: number[]): boolean {
  if (selected.length !== answer.length) return false
  const sorted = [...selected].sort((a, b) => a - b)
  const ans = [...answer].sort((a, b) => a - b)
  return sorted.every((v, i) => v === ans[i])
}

export function checkAnswer(question: Question, selected: number | number[]): boolean {
  if (question.type === 'multiple') {
    return isMultipleChoiceCorrect(selected as number[], question.answer as number[])
  }
  return selected === question.answer
}
```

---

## 六、题型 UI 策略

| 题型 | UI 行为 | 判分 |
| ---- | ------- | ---- |
| `single` | 4 选项，点选即锁定并判分 | `selected === answer` |
| `multiple` | 多选 toggle + **「确认提交」** 按钮 | 集合相等 |
| `judge` | 「正确」「错误」两按钮 | `selected === answer`（下标） |

**最后一题：** 底部按钮文案改为「查看报告」，跳转 result。

---

## 七、交互动效（需求强制）

| 场景 | 行为 |
| ---- | ---- |
| 答对 | 选项变绿 `#07c160` + **短音效**（`uni.createInnerAudioContext`） |
| 答错 | 选项变红 `#fa5151` + `uni.vibrateShort({ type: 'medium' })` |
| 解析 | 答题后立即展示 `explanation`（得意黑风格 `.bt-teacher-note`） |
| 进度条 | `.bt-progress-line` 暖橙 8px 渐变 |

---

## 八、各页面实现要点

### 8.1 首页 `index`

**已实现（对齐 [`prototypes/ui.html`](../prototypes/ui.html) 参考首页）：**

- 顶栏：问候语 + 副标题；微信环境为胶囊预留右侧安全区（`utils/layout.ts`）
- 主标题 + 橙色下划线
- 输入卡片：多行输入、快捷主题 pill、「换一换」、双行主按钮
- 热门主题：横滑 5 张卡片（一屏约 3 张），点击填入 topic
- 未完成关卡卡片 + 「继续」；底栏 `FloatTabbar`（闯关 / 题库 / 勋章，后两者 MVP 置灰）

**MVP 必做（逻辑不变）：**

- topic 非空校验 → `loading` → API / Mock
- `TOPIC_BATCHES` + `shuffleTopics` 换批；`pickTopic` 写输入框

**不做：** 模式选择、URL 解析、底栏真实切换

### 8.2 生成页 `loading`

**心理学进度条：**

- 0–5s：快速增至 ~40%
- 之后慢速递增，最高 ~90%（不等 API 才到 100%）
- 文案每 3s 轮播（参考 `loading-steps.js` 四步）

**API 调用：**

```typescript
// onLoad: 从上一页 storage 或 eventChannel 取 topic
const res = await generateQuiz(topic)
uni.setStorageSync('currentQuiz', res)
uni.redirectTo({ url: '/pages/quiz/quiz' })
```

**取消策略：** `onUnload` 设 `cancelled = true`；响应返回时若已 cancelled 则丢弃、不跳转。

**失败：** Toast「生成失败，请重试」+ `navigateBack` 或 `reLaunch` 回首页。

### 8.3 答题页 `quiz`

**布局：**

```
┌─────────────────────────┐
│ 顶栏：题号 pill          │
├─────────────────────────┤
│ scroll-view（题干）      │
├─────────────────────────┤
│ 选项区（固定）           │
├─────────────────────────┤
│ FeedbackPanel（解析）    │
├─────────────────────────┤
│ 下一题 / 查看报告 按钮   │
└─────────────────────────┘
```

- 题干区、解析区使用 `scroll-view`，选项区与底部按钮固定
- Mock 数据须含**超长题干/解析**，小屏真机验证

**不做：** 顶栏倒计时、灵韵惩罚（`.bt-spirit` 原型仅探索）

### 8.4 结算页 `result`

**两阶段 UX（方案 §6.9）：**

1. **立即：** 从 `quizAnswers` 计算并展示本地正确率、得分环
2. **异步：** 报告区 skeleton +「AI 正在生成复盘报告…」
3. **完成：** 渲染 Markdown 报告

```typescript
const payload = {
  quiz_id: session.quiz_id,
  topic: session.topic,
  questions: session.questions,
  answers: getQuizAnswers(),
}
const report = await generateReport(payload)
```

**再来一局：** 调用 `clearQuizSession()` → `reLaunch` 到 index

**分享按钮：** 置灰，不可点击（MVP 不做）

---

## 九、API 封装（`services/api.ts`）

```typescript
const BASE_URL = 'http://127.0.0.1:8000'  // 真机改局域网 IP

export function generateQuiz(topic: string): Promise<GenerateQuizResponse> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}/api/v1/quiz/generate`,
      method: 'POST',
      data: { topic },
      timeout: 60000,
      success: (res) => {
        if (res.statusCode !== 200) reject(new Error('生成失败'))
        else resolve(res.data as GenerateQuizResponse)
      },
      fail: reject,
    })
  })
}
```

`generateReport` 同理，`timeout: 30000`。

---

## 十、UI：Bento Token 映射

从 [`prototypes/bento-theme.css`](../prototypes/bento-theme.css) 提取至 `styles/bento.scss`：

| CSS 变量 | 值 | 用途 |
| -------- | -- | ---- |
| `--bt-primary` | `#F06A2A` | 主色、按钮、进度条 |
| `--bt-bg-screen` | `#FFFDF8` | 页面背景 |
| `--bt-surface` | `#FFFFFF` | 卡片 |
| `--bt-text` | `#1F2937` | 主文字 |
| `--bt-success` | `#22C55E` | 答对（实现用 `#07c160`） |
| `--bt-error` | `#EF4444` | 答错（实现用 `#fa5151`） |
| `--bt-radius-md` | `16px` | 卡片圆角 |
| `--bt-font` | 文楷 | 全局 |
| `--bt-font-note` | 得意黑 | 仅解析区 |

**组件类映射：**

| 原型类 | uni-app 实现 |
| ------ | ------------ |
| `.ref-input-card` / `.ref-btn-generate` | 首页 `home-input-card` / `home-btn-generate` |
| `ui-ref-home` 顶栏与主题卡 | `pages/index/index.vue` + `FloatTabbar.vue` |
| `.bt-book-flip` | loading 翻书动画 |
| `.bt-opt` | OptionList 选项 |
| `.bt-judge-btn` | 判断题按钮 |
| `.bt-teacher-note` | FeedbackPanel 解析 |
| `.bt-progress-line` | 题间进度 |
| `.bt-score-ring` | result 得分环 |
| `.bt-report-top` | result 顶栏 |

---

## 十一、Mock 数据要求（Sprint 2）

`mock/quiz.json` 须包含：

- 恰好 10 题
- 至少各 1 道 `single`、`multiple`、`judge`
- 1 道含超长 `stem`（>200 字）
- 1 道含超长 `explanation`（>300 字）
- 判断题示例：`stem` 为易错题， `answer` 为选项下标

首页增加开发开关（仅 dev）：`USE_MOCK=true` 时跳过 API，直接写入 storage 并跳转 quiz。

---

## 十二、towxml 集成（Sprint 4）

1. `npm install towxml`
2. 将 towxml 组件复制到 `uniapp/src/wxcomponents/towxml/`（按官方 uni-app 指引）
3. `pages.json` 中 result 页 `usingComponents` 注册
4. `ReportView.vue` 传入 Markdown 字符串

**备选 B（超时启用）：** 按 `\n\n` 分段，`<view class="report-p">` 渲染；`##` 行渲染为 `<view class="report-h2">`。

---

## 十三、MVP 屏与方案对照检查表

| 检查项 | 屏 | 通过标准 |
| ------ | -- | -------- |
| 仅单一输入 | 1 | 无模式/URL 入口 |
| 心理学进度 | 2 | 文案轮播 + 可取消 |
| 三题型 | 3–5 | UI 可分 |
| 多选确认提交 | 4 | 无自动跳题 |
| 判断题语义 | 5 | answer 为下标 |
| 绿/红+震动+音效 | 6–7 | 方案 §6.3 |
| 即时解析 | 6–7 | explanation 展示 |
| 无计时 | 3–7 | 顶栏无倒计时 |
| 无生命值 | 3–7 | 不做 hearts/灵韵 |
| result 二次等待 | 9 | skeleton 态 |
| 再来一局清 3 key | 8 | 不 clearStorage |
| 分享 MVP 不做 | 8 | 置灰 |

---

## 十四、G0 / G2 验收清单

**G0：**

- [ ] 四页面在 `pages.json` 注册
- [ ] index → loading → quiz → result 空页可跳转

**G2：**

- [ ] Mock 10 题走完
- [ ] 三题型 UI 与判分正确
- [ ] 答对音效 + 答错震动
- [ ] 返回再进 quiz 进度恢复
- [ ] result 展示静态报告文本

---

## 修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-29 | 初版前端实现指引 |
| v1.1.0 | 2026-05-29 | 首页参考稿 UI、layout 适配、目录与 UI 映射更新 |
