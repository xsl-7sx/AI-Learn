# 知练（KnowPractice）— MVP 前端实现指引

> **文档性质：** uni-app 小程序开发规格（Sprint 2–4 执行依据）。  
> **上级文档：** [MVP开发实施指南.md](./MVP开发实施指南.md)

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-29 | 初版：页面、组件、storage、UI 映射、交互检查表 |
| v1.1.0 | 2026-05-29 | 首页参考稿 UI 落地；layout 多机型顶栏适配；文档同步仓库结构 |
| v1.2.0 | 2026-05-29 | 首页 UI 精修：Lucide 图标、安全区底栏、间距与横滑优化 |
| v1.3.0 | 2026-05-29 | 生成页 UI 精修：垂直居中布局、四步指示器、取消按钮与底栏安全区 |
| v1.4.0 | 2026-05-29 | 答题退出 Sheet、多关卡存档、首页未完成列表、真机 `.env` 联调 |

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
│   ├── AppIcon.vue           # Lucide SVG data URI 图标
│   ├── FloatTabbar.vue       # 悬浮胶囊底栏（闯关 / 题库 / 勋章）
│   ├── QuestionCard.vue      # 题干展示
│   ├── OptionList.vue        # 选项 / 判断按钮
│   ├── FeedbackPanel.vue     # 对错反馈 + 解析
│   └── ReportView.vue        # Markdown 渲染（towxml 或备选 B）
├── services/
│   └── api.ts                # generateQuiz / generateReport
├── utils/
│   ├── scoring.ts            # 本地判分
│   ├── storage.ts            # 三 key 读写封装
│   ├── topics.ts             # 热门主题批次（含 IconName）
│   ├── icons.ts              # Lucide 图标注册表
│   ├── fonts.ts              # 装饰性手写字体按需加载
│   └── layout.ts             # 顶栏/胶囊安全区与主题卡宽度
├── types/
│   └── quiz.ts               # snake_case 类型
├── styles/
│   └── bento.scss            # 从原型提取的 --bt-* Token
└── mock/
    └── quiz.json             # Sprint 2 Mock 数据
```

---

## 四、Storage（多关卡存档）

| Key | 内容 | 写入时机 | 清除时机 |
| --- | ---- | -------- | -------- |
| `quizArchive` | `SavedQuizRecord[]`（session + answers + progressIndex + updatedAt） | 答题中增量更新；保存并退出 | 放弃本关 / 再来一局（仅删当前关） |
| `activeQuizId` | 当前正在答的 `quiz_id` | 进入答题 / 新开一局 / 点「继续」 | 放弃本关或清除当前关 |

旧版单 key（`currentQuiz` / `quizAnswers` / `quizProgress`）首次读取时自动迁移进 `quizArchive`。

```typescript
// 新开一局
export function beginQuizSession(session: QuizSession): void

// 首页未完成列表（按 updatedAt 倒序）
export function getIncompleteQuizzes(): IncompleteQuizSummary[]

// 点「继续」前激活对应关卡
export function activateQuiz(quizId: string): boolean

// 再来一局 / 放弃本关（仅清除指定 quiz_id）
export function clearQuizSession(quizId?: string): void
```

> **quiz 页 `onShow`：** 从 `activeQuizId` 对应记录恢复进度与作答；**保存并退出**只更新 archive，不删其他未完成关卡。

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

- 顶栏：品牌「知练」+ 问候语；微信环境为胶囊预留右侧安全区（`utils/layout.ts`）；连续学习火焰与日历图标
- 主标题 + 橙色下划线；主标题与问候语垂直间距压缩（`scrollPaddingTop: 0`，约上移 24px）
- 输入卡片：多行输入（内边距约 18px）、Lucide 铅笔图标、快捷主题横滑 pill + 右侧渐变遮罩、「换一换」与标签保持 ≥12px 间距
- 主 CTA：橙渐变双行按钮（`view` 实现，避免小程序 `button` 覆盖文字色）
- 热门主题：横滑 5 张卡片（一屏约 3 张），统一图标底块 + 两行标题省略；点击填入 topic
- 未完成关卡：**默认展示最近 2 条**，超出部分点「展开其余 N 个」内联展开；每条可「继续」对应 `quiz_id`
- 图标：`AppIcon` + `utils/icons.ts`（Lucide ISC，SVG data URI，无外链字体文件）
- 底栏安全区：`float-tabbar` 宿主 `position: fixed` + `env(safe-area-inset-bottom)`；`scroll-view` 底部 `bottom-spacer` ≥100px 避免内容被底栏遮挡

**MVP 必做（逻辑不变）：**

- topic 非空校验 → `loading` → API / Mock
- `TOPIC_BATCHES` + `shuffleTopics` 换批；`pickTopic` 写输入框

**不做：** 模式选择、URL 解析、底栏真实切换、全屏山水背景图（`home-bg.png` 仅资源预留，当前使用 `bt-screen` 渐变）

### 8.2 生成页 `loading`

**已实现（UI）：**

- 顶栏标题区固定在上部（`loading-header` + `layout.ts` 胶囊适配）
- 核心区块（进度卡片 + 四步指示器 + 副文案 + 取消）在顶栏与底栏之间**垂直居中**（`loading-body` / `loading-main`）
- 进度卡片：书本 `AppIcon` 微动效、心理学进度条、阶段文案（90% 后显示「快好了，再等等…」并缓爬至 98%）
- 四步指示器：每列 `width: 25%` 等分；已完成 / 进行中 / 未开始三色区分；圆圈内数字独立 `<text>` + flex 光学居中
- 取消：全宽胶囊按钮（`2rpx` 边框、白底），与副文案保持 ≥40rpx 间距
- 底栏：`FloatTabbar` 保留；宿主节点 `env(safe-area-inset-bottom)` 适配全面屏 Home 条

**心理学进度条：**

- 0–5s：快速增至 ~40%
- 之后慢速递增，最高 ~90%（不等 API 才到 100%）
- 90% 后缓增至 ~98%，完成时跳至 100%
- 阶段文案随进度切换（检索考点 → 出题校验 → 排版选项 → 准备闯关）

**API 调用（v1.1 流式 + 首题跳转）：**

```typescript
// onLoad: 从上一页 storage 取 topic
const job = await startQuizGeneration(topic)
const first = await waitForFirstQuestion(job.job_id, { intervalMs: 600 })
uni.setStorageSync('currentQuiz', {
  quiz_id: first.quiz_id,
  topic: first.topic,
  questions: first.questions,
  generating: first.status !== 'completed',
  job_id: job.job_id,
  total_expected: first.total_expected ?? 10,
})
uni.redirectTo({ url: '/pages/quiz/quiz' })
// 后台继续 pollQuizJobUntilComplete，增量 merge questions
```

**取消策略：** `onUnload` 设 `cancelled = true`；首题返回后若已 cancelled 则不跳转。

**失败：** Toast「生成失败，请重试」+ `navigateBack` 或 `reLaunch` 回首页。

**注意：** 不向用户展示 `stream_preview` 原始 JSON。

### 8.3 答题页 `quiz`

**布局：**

```
┌─────────────────────────┐
│ 顶栏：✕（左）+ 题号 pill │
├─────────────────────────┤
│ scroll-view（题干+选项） │
├─────────────────────────┤
│ FeedbackPanel（解析）    │
├─────────────────────────┤
│ 下一题 / 查看报告 按钮   │
└─────────────────────────┘
```

- 顶栏左上角 **✕** 打开退出确认 Sheet（避开微信胶囊）
- **退出 Sheet：** 继续答题 / 保存并退出 / 放弃本关；对齐原型屏 ③′
- 题干与选项同在 `scroll-view` 内；真机须 `height: 0` + `flex: 1` + `enhanced`
- **FeedbackPanel：** 对错横幅 + 解析；答错震动、答对音效
- **边答边生成：** 仅在本题已作答且下一题未就绪时进入等待页（避免首题误进等待）
- 微信小程序**左滑返回无法可靠拦截**（`onBackPress` / `page-container` 真机会挡触摸）；退出以顶栏 ✕ 为准

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

## 九、API 与真机联调

**`config.ts`：** 从 `import.meta.env.VITE_API_BASE_URL` 读取；未配置时默认 `http://127.0.0.1:8000`（仅模拟器可用）。

```bash
cd uniapp
cp .env.development.example .env.development
# 编辑 VITE_API_BASE_URL=http://<电脑局域网IP>:8000
npm run dev:mp-weixin
```

后端须监听所有网卡：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`。手机与电脑同一 Wi-Fi；微信工具勾选「不校验合法域名」。自检：手机浏览器访问 `http://<IP>:8000/health`。

## 十、API 封装（`services/api.ts`）

```typescript
import { BASE_URL } from '@/config'

export async function startQuizGeneration(topic: string): Promise<QuizJobCreateResponse> {
  const res = await uni.request({
    url: `${BASE_URL}/api/v1/quiz/generate`,
    method: 'POST',
    data: { topic },
    timeout: 15000,
  })
  if (res.statusCode !== 202) throw new Error('创建出题任务失败')
  return res.data as QuizJobCreateResponse
}

export async function getQuizJob(jobId: string): Promise<QuizJobStatusResponse> { /* GET /jobs/{id} */ }

export async function waitForFirstQuestion(jobId: string, opts?: { intervalMs?: number }) {
  // 轮询直至 ready && questions.length >= 1
}

export async function pollQuizJobUntilComplete(jobId: string, onUpdate?: (job) => void) {
  // 轮询直至 completed / failed，默认 interval 600ms
}
```

`generateReport` 仍为 `POST /report`，`timeout: 30000`。

---

## 十一、UI：Bento Token 映射

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
| Lucide 线框图标 | `components/AppIcon.vue` + `utils/icons.ts` |
| `.bt-book-flip` | loading 翻书动画 |
| `.bt-opt` | OptionList 选项 |
| `.bt-judge-btn` | 判断题按钮 |
| `.bt-teacher-note` | FeedbackPanel 解析 |
| `.bt-progress-line` | 题间进度 |
| `.bt-score-ring` | result 得分环 |
| `.bt-report-top` | result 顶栏 |

---

## 十二、Mock 数据要求（Sprint 2）

`mock/quiz.json` 须包含：

- 恰好 10 题
- 至少各 1 道 `single`、`multiple`、`judge`
- 1 道含超长 `stem`（>200 字）
- 1 道含超长 `explanation`（>300 字）
- 判断题示例：`stem` 为易错题， `answer` 为选项下标

首页增加开发开关（仅 dev）：`USE_MOCK=true` 时跳过 API，直接写入 storage 并跳转 quiz。

---

## 十三、towxml 集成（Sprint 4）

1. `npm install towxml`
2. 将 towxml 组件复制到 `uniapp/src/wxcomponents/towxml/`（按官方 uni-app 指引）
3. `pages.json` 中 result 页 `usingComponents` 注册
4. `ReportView.vue` 传入 Markdown 字符串

**备选 B（超时启用）：** 按 `\n\n` 分段，`<view class="report-p">` 渲染；`##` 行渲染为 `<view class="report-h2">`。

---

## 十四、MVP 屏与方案对照检查表

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

## 十五、G0 / G2 验收清单

**G0：**

- [ ] 四页面在 `pages.json` 注册
- [ ] index → loading → quiz → result 空页可跳转

**G2：**

- [ ] Mock 10 题走完
- [ ] 三题型 UI 与判分正确
- [ ] 答对音效 + 答错震动
- [ ] 保存并退出后首页「未完成关卡」可续玩（支持多条，默认展示 2 条可展开）
- [ ] 答题页 ✕ 打开退出 Sheet；真机可正常点选选项
- [ ] 真机 `VITE_API_BASE_URL` 联调通过
- [ ] result 展示静态报告文本

---

## 修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-29 | 初版前端实现指引 |
| v1.1.0 | 2026-05-29 | 首页参考稿 UI、layout 适配、目录与 UI 映射更新 |
| v1.2.0 | 2026-05-29 | 首页 UI 精修：Lucide 图标、底栏安全区、间距与横滑优化 |
| v1.3.0 | 2026-05-29 | 生成页 UI 精修：垂直居中、四步指示器、取消按钮与底栏安全区 |
| v1.4.0 | 2026-05-29 | 答题退出 Sheet、多关卡存档、未完成列表展开、真机 `.env` 联调 |
