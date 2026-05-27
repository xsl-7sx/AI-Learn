# 知练（KnowPractice）— UI HTML 原型实施指引

> **产品品牌：** 知练（KnowPractice）。

| 文档版本 | 撰写时间 | 状态 |
| -------- | -------- | ---- |
| v1.7.4 | 2026-05-27 | `02`/`03` 与 MVP 对齐；扩展组件库；§6.2 分屏验收表 |
| v1.7.3 | 2026-05-27 | Tab 并入 `03`；首页滚动区；热门主题横滑；gallery 22 屏 |
| v1.6.0 | 2026-05-27 | 参考首页 `ui.html`；Loading IP；反馈 demo；灵韵条（原型探索） |
| v1.5.0 | 2026-05-26 | 悬浮胶囊底栏；底区纸纹连续；闯关首页图标；布局/图标/进度条 |
| v1.4.0 | 2026-05-26 | Bento 暖橙主题；翻书 Loading；移除金币角标 |
| v1.3.0 | 2026-05-26 | §1.0 文档阶段说明；链到 UI 文档索引 |
| v1.2.3 | 2026-05-26 | 总览六幕业务流 + `phone-screen--act` 笔记本组件 |
| v1.2.0 | 2026-05-26 | 20 屏 gallery + 笔记本风（不规则横纹）已落盘 |
| v1.0.0 | 2026-05-26 | 初版指引 |

**相关文档：**

- [UI 设计文档索引](./UI设计文档索引.md)
- [UI 设计风格与 Design System](./UI设计风格与DesignSystem.md)
- [UI 页面原型说明](./UI页面原型说明.md)
- [UI HTML 原型迭代清单](./UI-HTML原型迭代清单.md)
- 预览入口：[`../prototypes/index.html`](../prototypes/index.html)

---

## 一、目标与边界

### 1.0 文档阶段说明

UI 设计文档集（Design System + 页面说明 + 本指引）先于 HTML 原型编写完成。静态 gallery 为**后续视觉对照**，其迭代见 [UI-HTML原型迭代清单](./UI-HTML原型迭代清单.md)。**uni-app / 后端代码不在 UI 文档集范围内。**

### 1.1 目标

在 `prototypes/` 目录产出 **静态 HTML + CSS** 页面画廊，用于：

- 产品/设计评审
- uni-app 开发视觉对照
- 对外演示路线图（含扩展屏）

### 1.2 非目标

- 不连接真实 API
- 不做页面间真实路由跳转（画廊平铺展示）
- 不替代 uni-app 源码
- 不在未获指示时修改 `uniapp/`、`backend/`

---

## 二、文件结构（当前 v1.7.3）

```
AI-Learn/prototypes/
├── index.html                    # 总览：六幕 showcase + 业务流
├── ui.html                       # ★ 网页展示稿（与 01 屏① 同步）
├── shared.css                    # 画廊布局、手机框、基础 Token
├── bento-theme.css               # ★ 主主题：Bento 暖橙 + bt-* 组件
├── ui-ref-home.css               # ★ 参考首页（.ref-home）
├── loading-steps.js              # 生成页四步进度 + IP 气泡 demo
├── quiz-feedback-demo.js         # 屏 6/7 反馈动效循环 demo
├── paper-lines-page.svg          # 画廊不规则横纹
├── paper-lines-screen.svg        # 屏内浅色不规则横纹
├── 01_mvp_core.html              # MVP 9 屏
├── 02_extended_features.html     # 扩展 6 屏
├── 03_reports_social.html        # 报告 7 屏（含 Tab ⑥题库 / ⑦勋章）
├── 04_tab_pages.html             # 跳转 → 03#tab-bank（兼容旧链接）
├── ref-home-topics.js            # 首页热门主题：换一批 + 横滑拖拽/滚轮
├── manga-heavy-mvp.html          # 归档：4 屏漫画风（未随 Bento v1.6 维护）
├── mascots.svg                   # Loading：mascot-think；其余屏待评估
├── graphic-note.css              # 归档：旧笔记本主题（gallery 未引用）
├── ux-enhancements.css           # 归档：旧 a11y 层（gallery 未引用）
├── spec-highlights.css           # 归档：旧亮点层（gallery 未引用）
└── study-char.svg                # 归档：总览插画（当前屏未引用）
```

| 文件 | 屏数 | 说明 |
| ---- | ---- | ---- |
| `01_mvp_core.html` | 9 | [§二](./UI页面原型说明.md#二mvp-核心闭环9-屏) |
| `02_extended_features.html` | 6 | [§三](./UI页面原型说明.md#三扩展功能6-屏--中保真) |
| `03_reports_social.html` | 7 | [§四](./UI页面原型说明.md#四报告与社交7-屏--中保真)（含 Tab ⑥⑦） |
| **合计** | **22** | MVP 9 + 扩展 6 + 报告 7 |

**HTML 引用顺序（`01` / `ui.html` 等 MVP 页）：**

```html
<link rel="stylesheet" href="shared.css" />
<link rel="stylesheet" href="bento-theme.css" />
<link rel="stylesheet" href="ui-ref-home.css" />  <!-- 仅屏① / ui.html -->
<script src="loading-steps.js" defer></script>
<script src="quiz-feedback-demo.js" defer></script>  <!-- 屏 6/7 -->
<script src="ref-home-topics.js"></script>           <!-- 屏① / index showcase -->
<body class="theme-bento">
```

**屏① 布局约定（v1.7.3）：** `ref-topbar` 在 `phone-screen` 内固定不滚；仅 `ref-home-scroll` 纵向滚动；`bt-tabbar-float` 与 `phone-screen` 并列于 `phone-frame`（`flex` 分配高度，避免 `height:100%` 裁切底栏）。热门主题为 `ref-topic-strip` > `ref-topic-row` 横向 `scroll-snap`。

`index.html` 总览 showcase 首页已与 `ui.html` / `01` 屏① 对齐（`.ref-home`，见 [迭代清单](./UI-HTML原型迭代清单.md)）。

---

## 三、画廊布局规范

### 3.1 响应式列数

| 视口宽度 | 列数 |
| -------- | ---- |
| ≥ 1280px | 3 列 |
| 768px – 1279px | 2 列 |
| < 768px | 1 列 |

### 3.2 单屏结构

```html
<article class="screen-item">
  <h2 class="screen-label">① 首页 · 输入</h2>
  <code class="screen-route">pages/index/index</code>
  <div class="phone-wrap">
    <div class="phone-frame">
      <div class="phone-notch"></div>
      <div class="phone-screen bt-screen">
        <div class="bt-notch-safe" aria-hidden="true"></div>
        <div class="bt-scroll">…</div>
      </div>
      <nav class="bt-tabbar bt-tabbar-float" aria-label="主导航">…</nav>
    </div>
  </div>
</article>
```

### 3.3 设备框

| 属性 | 值 |
| ---- | -- |
| 逻辑分辨率 | 393 × 852 px |
| 外框圆角 | 47px（`--phone-radius`） |
| 刘海 | `phone-notch` |
| 画廊预览缩放 | `--phone-preview-scale: 0.82`（避免裁切） |

---

## 四、Bento 暖橙实施要点（v1.5）

### 4.1 背景（保留水彩横纹）

| 区域 | 实现 |
| ---- | ---- |
| 画廊 `body.theme-bento` | 马卡龙渐变 + `paper-lines-page.svg` + 噪点 + 柔光斑 |
| 屏内 `.phone-screen` / `.bt-screen` | `--bt-screen-paper-bg`（水彩 radial + `paper-lines-screen.svg` + 暖纸渐变） |
| 有悬浮底栏的 `.phone-frame` | 同上变量铺至整列；`.phone-screen` 背景透明，底栏留白区与内容区同色 |
| 加载页卡片内 | 同屏内纸面；主视觉为 `.bt-book-flip` |

**禁止：** 方格格纹 `linear-gradient` 网格；皮质书本手机外壳。

### 4.2 主色与组件前缀

| Token | 值 | 用途 |
| ----- | -- | ---- |
| `--bt-primary` | `#F06A2A` | 主按钮、进度条、Tab 选中 |
| `--bt-primary-soft` | `#FFF0E8` | 浅橙底、输入区 |
| `--bt-success` / `--bt-error` | `#22C55E` / `#EF4444` | 对错态（实现可对齐微信色） |
| 组件 class | `bt-*` | 见 [Design System §6.3](./UI设计风格与DesignSystem.md) |

### 4.3 字体

| 范围 | 字体 | CDN |
| ---- | ---- | --- |
| 全局 UI | 霞鹜文楷屏幕版 `LXGW WenKai Screen` | jsDelivr `lxgw-wenkai-screen-web` |
| 解析区 `.bt-teacher-note` | 得意黑 `Smiley Sans` | unpkg `@fontpkg/smiley-sans` |
| 正文基准 | **16px**，行高 1.5–1.7 | 满足移动端可读性 |

### 4.4 加载页翻书动画

- 容器：`.bt-book-flip`（摊开本 + 单页 360° 循环翻页 + 轻微浮动）
- 进度：`[data-gen-progress-fill]` + `loading-steps.js` 驱动 ①–④ 文案、`.bt-step` 状态（当前步高亮、完成步绿勾）
- IP：`mascots.svg#mascot-think` + 气泡文案随步骤切换（gallery 无「小皮」署名行）
- **已移除：** 笑脸 SVG 主视觉、顶栏金币

### 4.5 顶栏与奖励示意

- 首页 / 生成 / 答题：`bt-notch-safe` + 滚动区；问候语在 `.bt-scroll` 内
- 答题顶栏：`bt-topbar--quiz`（关闭 + `bt-progress-pill`）；屏 3–7 可选 **`.bt-spirit` 五段能量条**（仅 HTML 原型探索，**产品 MVP 仍不做惩罚式生命值**）
- **无** `bt-coin-pill`、反馈条「+N 金币」、报告 `+20 XP` 徽章（原型阶段均不展示）

### 4.6 屏内布局

- 默认 `.bt-scroll` **顶对齐**（`padding-top: 12px`），内容多时可滚动
- 仅生成中：`.bt-scroll--center` 垂直居中（翻书 + 步骤条）
- 通关报告：`bt-report-top` 在滚动区外；`bt-notch-safe` 统一避刘海
- 无 Tab 的答题反馈：`.bt-btn-row` 贴底（`margin-top: auto`）

### 4.7 图标与进度

| 元素 | 类名 | 说明 |
| ---- | ---- | ---- |
| 输入框尾标 | `.bt-input-icon` | 暖橙铅笔 SVG（非笑脸） |
| 答对标记 | `.bt-opt-check` | 绿圆章 + 白勾（CSS/SVG 背景） |
| 横向进度 | `.bt-progress-line` | 8px · `#F06A2A → #FFB380` · `width` 过渡 |
| 对手进度 | `.bt-progress-line--rival` | 蓝渐变 |
| 生成步骤 | `.bt-step` | 橙/绿描边圆点，无脉冲动画 |
| 闯关 Tab | `.bt-tab` 内 SVG | 首页（房子）图标，非旗帜 |

### 4.8 悬浮底栏（`bt-tabbar-float`）

| 项 | 约定 |
| -- | ---- |
| DOM | `<nav class="bt-tabbar bt-tabbar-float">` 为 `phone-frame` 直接子节点，**不在** `phone-screen` 内 |
| 形态 | 圆角胶囊（`border-radius: 999px`）；`margin` 左右约 12px、底约 16px；轻阴影 + 可选 `backdrop-filter` |
| 选中 | `.bt-tab.is-active`：蜜桃渐变底 + `--bt-primary` 字色 |
| 备用 | 无悬浮条时仍可用贴底全宽 `.bt-tabbar`（`border-top`） |
| 禁止 | 为托底改机框灰底、全宽贴边白条破坏胶囊感 |

### 4.9 解析区

- 组件：`.bt-teacher-note`（左侧桃色边条 + 铅笔 SVG +「老师笔记」标签）
- 正文：得意黑；选项/题干：文楷

---

## 五、shared.css 要点

1. 画廊网格 `.screen-grid`、`.poster-phones-row`
2. 手机框 `.phone-frame` / `.phone-wrap`
3. 与 `bento-theme` 叠加时不覆盖 `--bt-*` Token

---

## 六、分文件验收要素

### 6.1 `01_mvp_core.html`（9 屏）

| 序号 | 屏 | Bento 必含 |
| ---- | -- | ---------- |
| 1 | 首页 | `.ref-home`：顶栏固定 + `ref-home-scroll`；compose 输入；`ref-topic-strip` 横滑（5 卡/组）；`ref-home-topics.js`；与 [`ui.html`](../prototypes/ui.html) 同步 |
| 2 | 生成中 | `bt-book-flip`、`bt-progress-line`、`data-gen-stepper`、`bt-stepper`、IP 气泡 |
| 3–5 | 三题型 | `bt-q-stem`、`bt-opt`、可选 `.bt-spirit`、`bt-progress-line` |
| 6–7 | 对错反馈 | `bt-meta-row` + `bt-progress-line`；`bt-feedback-bar`、`bt-teacher-note`；`data-feedback-demo` + `quiz-feedback-demo.js` |
| 8 | 通关报告 | `bt-report-top`、`bt-metrics`、Bento 四格 |
| 9 | skeleton | 步骤条 + skeleton 占位 |

### 6.2 `02_extended_features.html`（6 屏）

| # | 屏 | 页面类型 | Bento 必含 |
| - | -- | -------- | ---------- |
| ① | RAG | 功能页 | `bt-greeting` + `ref-input-card` + `bt-level-item` 闯关集 |
| ② | VIP | 功能页 | `bt-vip-card__row` 价签；`bt-stat-badges` 权益 |
| ③ | 生图题 | 答题页 | `bt-topbar--quiz` + `bt-img-opt-grid`（A–D） |
| ④ | PK | 功能页 | `bt-pk-scoreboard` + `bt-vs-duel` + 双 `bt-progress-line` |
| ⑤ | 排行 | 功能页 | `bt-rank-tabs` + `bt-podium-wrap` + `bt-rank-me-card` |
| ⑥ | 语音 | 答题页 | `bt-voice-bar` + `bt-voice-bar__action`（暂停无边框） |

### 6.3 `03_reports_social.html`（7 屏）

| # | 屏 | 页面类型 | Bento 必含 |
| - | -- | -------- | ---------- |
| ① | 复盘详情 | 报告页 | 对齐 MVP 屏⑧：`bt-report-top` + `bt-score-ring` + `bt-list-num` |
| ② | 知识图谱 | 报告页 | SVG + `bt-concept-row` |
| ③ | 薄弱分析 | 报告页 | 雷达 + `bt-skill-row` |
| ④ | 战绩海报 | 报告页 | `bt-poster-card` + `bt-share-card` |
| ⑤ | 错题本 | 功能页 | `bt-metrics` + `bt-wrong-item`；底栏「题库」高亮 |
| ⑥ | 题库 Tab | Tab 页 | `ref-level-card`；`#tab-bank` |
| ⑦ | 勋章 Tab | Tab 页 | `bt-medal-grid`；`#tab-medal` |

**三分页面层级（v1.7.4）：**

| 类型 | 顶栏 | 勿用 |
| ---- | ---- | ---- |
| 功能页 | `bt-greeting` + `bt-title` + `bt-subtitle` | `bt-report-top` 叠大标题 |
| 答题页 | `bt-topbar--quiz` + `bt-meta-row` | 答题中开关/解析长文 |
| 报告页 | `bt-report-top` + 滚动区单条主叙事 | 重复 bento 四格 + 长文复盘 |

**通用：** `nmvp-badge`；需要底栏时用 `bt-tabbar-float`（DOM 在 `phone-screen` 外）。

---

## 七、预览方式

```bash
npx serve d:\AI-Learn\prototypes
```

打开 `index.html`、`ui.html` 或 `01_mvp_core.html`。生成页由 `loading-steps.js` 循环 demo；屏 6/7 进入视口时由 `quiz-feedback-demo.js` 重播反馈动效。

---

## 八、验收 Checklist

- [x] 桌面三列 / 平板两列 / 手机单列
- [x] MVP 9 屏与页面说明对应
- [x] `theme-bento` + `bento-theme.css` 四页统一引用
- [x] 加载页翻书动画 + 四步 stepper（高亮/完成勾）
- [x] Loading IP（`mascot-think`）+ 步骤气泡
- [x] 参考首页 `ui.html` / 屏①（横滑热门、compose 示例）
- [x] 屏 6/7 反馈条与老师笔记入场动效（`quiz-feedback-demo.js`）
- [x] 顶栏无金币角标；无反馈金币 / 报告 XP 文案
- [x] 主导航屏：`bt-tabbar-float` 悬浮胶囊；底区纸纹与内容区连续
- [x] 生成页 `.bt-scroll--center`；其余屏顶对齐
- [x] 输入铅笔图标 + 答对圆章勾 + 克制进度条
- [x] 老师笔记区得意黑 + 全局文楷
- [x] 选项马卡龙渐变 + 对错绿/红渐变
- [x] 屏 8 / 9 结算分屏
- [x] 无单题计时
- [x] **产品**无惩罚式生命值；gallery 可选 `.bt-spirit` 仅作视觉探索
- [x] 分享按钮 MVP 置灰（屏 8）
- [x] 扩展 11 屏 Phase 标注
- [x] Tab 子页在 `03` 屏⑥⑦：`#tab-bank` / `#tab-medal`（`04` 仅跳转）
- [x] `02`/`03` 三分页面层级；领奖台 `bt-podium-wrap` 不裁切前三
- [x] 语音条「暂停」使用 `bt-voice-bar__action`（无按钮边框）
- [x] 页面说明 §1.3：底栏 Tab 与 MVP 四页栈映射
- [x] `index` 总览：Tab 双屏区 + Phase 2 错题本与 `03` 对齐
- [x] `manga-heavy-mvp.html` 标注归档、非主预览
- [x] `prefers-reduced-motion` 翻书降级
- [ ] 本地浏览器逐屏目视（请评审人勾选：`01`×9 · `04`×2 · `02`×6 · `03`×5 · `index` · `ui.html`）

---

## 九、与 uni-app 开发的衔接

| HTML 原型 | uni-app |
| --------- | ------- |
| `theme-bento` / `--bt-*` | 全局 SCSS 变量与组件库 |
| `paper-lines-*.svg` | 背景图或切图 |
| `bt-teacher-note` | `FeedbackPanel` 解析组件 |
| `bt-book-flip` | Lottie / CSS 动画或静态插画替代 |
| 对错色 | 实现层 `#07c160` / `#fa5151` |
| 金币 | 产品若保留 gamification，单独设计角标；勿与已删原型强绑 |

开发顺序仍按 [方案设计 §七 G0–G4](./交互式AI闯关学习微信小程序方案设计文档.md#七核心-mvp-开发流程)。

---

## 十、执行状态

| 任务 | 状态 |
| ---- | ---- |
| 设计文档 trio | ✅ |
| Bento 暖橙 `bento-theme.css` | ✅ v1.4 |
| 22 屏 gallery | ✅ v1.7.3 |
| 翻书 Loading 动画 | ✅ |
| 参考首页 / Loading IP / 反馈 demo | ✅ v1.6 |
| Tab 并入 `03` / 首页滚动与热门横滑 | ✅ v1.7.3 |
| `02`/`03` 与 MVP 视觉对齐 | ✅ v1.7.4 |
| 移除金币角标 | ✅ |
| 旧 `graphic-note` 主题 | 📦 归档未引用 |
| 浏览器验收 | 待评审人本地确认 |

---

## 十一、修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.7.4 | 2026-05-27 | `02`/`03` 分屏验收；三分页面层级；扩展 `bt-*` 组件 |
| v1.7.3 | 2026-05-27 | `03` 报告 7 屏含 Tab；`04` 跳转；首页顶栏/底栏滚动；`ref-home-topics.js` 横滑 |
| v1.6.0 | 2026-05-27 | `ui.html` / `ui-ref-home.css`；IP + stepper；`quiz-feedback-demo.js`；灵韵条原型说明 |
| v1.5.0 | 2026-05-26 | 悬浮胶囊底栏；底区纸纹连续；闯关首页图标；§4.8 底栏约定 |
| v1.4.0 | 2026-05-26 | 布局顶对齐；移除 +10 金币 / +20 XP；图标与克制进度条 |
| v1.4.0 | 2026-05-26 | Bento 暖橙主题；`bento-theme.css`；翻书动画；无金币角标；字体文楷+得意黑 |
| v1.2.3 | 2026-05-26 | 总览六幕业务流程 showcase + biz-flow-map |
| v1.2.0 | 2026-05-26 | 笔记本风、SVG 横纹 |
| v1.0.0 | 2026-05-26 | 初版指引 |
