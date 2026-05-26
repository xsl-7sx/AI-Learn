# AI 闯关学习小程序 — UI 设计风格与 Design System

| 文档版本 | 撰写时间 | 状态 | 依据 |
| -------- | -------- | ---- | ---- |
| v1.4.0 | 2026-05-26 | 当前 HTML：Bento 暖橙；翻书 Loading；无顶栏金币 | 同上 |
| v1.3.0 | 2026-05-26 | 扩充市面参考、阿衰意境转译、混合文案对照表（文档计划 doc-market-ref） |
| v1.2.1 | 2026-05-26 | `ux-enhancements.css`：焦点可见、触控 48px、减少动效、色盲友好对错态 | 同上 |
| v1.2.0 | 2026-05-26 | 笔记本风定稿：不规则横纹 SVG、水彩屏内底、HTML 已落盘 | 同上 |
| v1.1.0 | 2026-05-26 | 增加「图文笔记风」视觉层（参考高效学习法笔记） | 同上 |
| v1.0.0 | 2026-05-26 | 设计定稿（文档阶段） | 同上 |

**相关文档：**

- [UI 设计文档索引](./UI设计文档索引.md) — 三份 UI 文档导航与验收清单
- [UI HTML 原型实施指引](./UI-HTML原型实施指引.md) — 静态 gallery（**v1.4 Bento 暖橙**）
- [UI HTML 原型迭代清单](./UI-HTML原型迭代清单.md) — 里程碑与资源清单
- HTML 原型（当前主预览）：[`../prototypes/`](../prototypes/) — `index.html` + `01/02/03` gallery
- 备选样例：[`../prototypes/manga-heavy-mvp.html`](../prototypes/manga-heavy-mvp.html)（4 屏重度漫画风）

---

## 一、设计定位

### 1.0 视觉参考

#### 1.0.1 当前 HTML 原型（v1.4 · Bento 暖橙）

**主参考：** 高保真 Bento 暖橙稿 — 大圆角卡片、底部 Tab、暖橙主色 `#F06A2A`、Duolingo 式单题流。

**叠合保留：** 水彩马卡龙纸面 + **不规则横纹 SVG**（`paper-lines-*.svg`），与早期笔记本风一致。

**实现栈（gallery 四页）：**

| 文件 | 职责 |
| ---- | ---- |
| [`prototypes/shared.css`](../prototypes/shared.css) | 画廊网格、手机框 |
| [`prototypes/bento-theme.css`](../prototypes/bento-theme.css) | `theme-bento`、`--bt-*` Token、`bt-*` 组件、翻书动画 |
| [`prototypes/loading-steps.js`](../prototypes/loading-steps.js) | 生成页四步进度 demo |
| [`prototypes/paper-lines-page.svg`](../prototypes/paper-lines-page.svg) | 画廊横纹 |
| [`prototypes/paper-lines-screen.svg`](../prototypes/paper-lines-screen.svg) | 屏内横纹 |

| 元素 | 原型实现 |
| ---- | -------- |
| 主按钮 / Tab | `.bt-btn-primary`、`.bt-tabbar` |
| 选项 | `.bt-opt` 马卡龙渐变；对错绿/红渐变态 |
| 解析 | `.bt-teacher-note` + 得意黑正文 |
| Loading | `.bt-book-flip` CSS 翻书（替代笑脸/小课豆主视觉） |
| 顶栏 | `.bt-topbar` / `.bt-quiz-header`；**无金币角标** |
| 字体 | 文楷全局 + 得意黑仅解析区 |

**明确不做：** 方格格纹、皮质书本手机外壳、顶栏金币数字（原型阶段）。

#### 1.0.2 归档参考（v1.2 笔记本风 · 未引用）

早期 `graphic-note.css` + `theme-graphic-note` + `mascot-chip` 方案仍保留于仓库，供对比与 uni-app 选型；**当前 gallery 不引用**。

**保留交互：** Duolingo 单题闯关 + 混合文案 + iPhone 15 Pro 设备框（含刘海）。

**归档文件：** `graphic-note.css`、`ux-enhancements.css`、`spec-highlights.css`、`mascots.svg`、`study-char.svg`。

### 1.0.3 历史说明（v1.2 · 笔记本风）

### 1.1 产品气质

**一句话：** 用 **图文笔记式 Bento** 呈现 Duolingo 式闯关学习，气质偏可爱手账而非重度黑白漫画。

| 维度 | 目标 |
| ---- | ---- |
| 情绪 | 轻松、好笑、不压迫；答错也要「学到就好」 |
| 场景 | 初中生～大学生碎片学习；一句话开练 |
| 差异 | 不是严肃题库 App，也不是纯儿童向；是「会吐槽的同桌带你刷题」 |

### 1.2 与《漫画阿衰》的意境对齐（非 IP 复刻）

《阿衰 online》为猫小乐创作的校园幽默 Q 版漫画。UI **不直接使用**阿衰、大脸妹、金乘五等官方角色与商标，仅转译其**视觉语法**：

#### 1.2.1 IP 边界（必须遵守）

| 允许 | 禁止 |
| ---- | ---- |
| 原创 Q 版「小课豆」、怕踢中学**气质** | 阿衰/大脸妹/金乘五等官方角色立绘、台词、Logo |
| 校园日常、作业本、涂鸦、倒霉又好笑 | 猫小乐作品截图、周边素材、商标色组合复刻 |
| 「同桌带你刷题」式口语梗 | 对外宣传称「阿衰联名/官方授权」 |

#### 1.2.2 视觉语法转译表

| 漫画特征 | 阿衰式表现 | UI 转译 | 落地组件/Token |
| -------- | ---------- | ------- | -------------- |
| Q 版比例、粗黑描边 | 头身比约 1:3，墨线 2–3px | 卡片/选项 **2.5px** 墨线；拒绝毛玻璃 | `border-comic`、`border-note` |
| 全彩明亮、黄帽衫 | 阿衰标志性黄 + 红点缀 | 草稿纸 `#FFF6DC`、便签黄 `#FFBF00`、强调红 `#E53935` | `paper-bg`、`accent-yellow`、`accent-red` |
| 分格叙事 | 多格连环、倾斜格 | 微倾 `comic-panel`；Bento 分区叙事 | `note-card`、`bento-grid` |
| 拟声词、速度线 | 「嗡～」「砰！」 | Display 字体 SFX；SVG 速度线装饰 | `sfx-label`、`.speed-lines` |
| 作业本、涂鸦 | 横线本、红笔批注 | 不规则横纹 SVG；手写体副标题 | `paper-lines-*`、`Ma Shan Zheng` |
| 对话框、吐槽 | 尖角气泡、夸张字号 | 解析 `speech-bubble`；Loading 气泡轮播 | `nb-bubble`、`speech-bubble` |
| 倒霉又好笑 | 摔倒、汗滴、X 眼 | 答错 `mascot--sad` + shake；文案「错了也学到」 | `screen-shake`、`mascot-sad` |
| 热血逆袭 | 通关爆炸字、竖拇指 | 结算 `pass-banner`、星眼 `mascot--happy` | `pass-banner`、`nb-stamp` |

#### 1.2.3 与「笔记本风」的叠合

v1.2 在阿衰漫画语法之上叠加 **Graphic Note / Bento**（马卡龙水彩、和纸胶带、便利贴）。原则：**交互骨架仍 Duolingo 单题流**；视觉层可偏手账治愈，不必全屏黑白漫画分格。

### 1.3 交互骨架（Duolingo / 刷题类借鉴）

| 来源 | 借鉴点 | 本项目用法 |
| ---- | ------ | ---------- |
| Duolingo | 单题一屏、即时绿/红、进度条、大点击区、按压阴影按钮 | MVP 答题流全部采用 |
| Duolingo | 生命值、连胜、排行榜 | **MVP 不做**；扩展 P3 再议 |
| 驾考宝典 / 刷题 App | 题号进度、解析区、成绩环 | 顶栏 `3/10`、结算 ScoreRing |
| 游戏化 Quiz | 倒计时、炫彩背景 | **MVP 不做倒计时** |

---

## 二、市面参考摘要（2024–2026）

> 本节为 **doc-market-ref** 交付：汇总竞品可借鉴点与本项目取舍，供设计与评审对照。

### 2.1 语言学习 / 游戏化

| 产品 | 可借鉴 | 本项目用法 | 明确不做 |
| ---- | ------ | ---------- | -------- |
| **Duolingo** | 单题一屏、即时绿/红、进度条、大点击区、3D 底阴影按钮、Feather 级圆体标题 | MVP 答题流全部采用；`comic-btn` / `nb-btn-*` 按压阴影 | 猫头鹰 IP、生命值、连胜 streak（MVP） |
| **百词斩** | 图像联想、单词卡、轻游戏化 | 扩展 E3「AI 生图题」参考 | MVP 不做配图生成 |
| **多邻国式音效** | 答对短促 positive SFX | 方案 §6.3 可选音效 | 不做复杂 BGM |

### 2.2 刷题 / 驾考 / 垂直题库

| 产品/类型 | 可借鉴 | 本项目用法 | 明确不做 |
| --------- | ------ | ---------- | -------- |
| **驾考宝典** 等 | 题号 `3/10`、解析气泡、成绩环、错题沉淀 | 顶栏进度、结算 ScoreRing；Phase 2 错题本 | 海量题库静态刷题模式 |
| **小猿搜题** 类 | 拍照搜题、解析长文 | 不在 MVP；RAG 扩展为「资料入库出题」 | 拍照 OCR 主路径 |
| **公考/考研 App** | 章节练习、薄弱点标签 | 结算「掌握点/薄弱点」chip；R3 雷达 | MVP 不做章节树导航 |

### 2.3 手账 / 学习笔记视觉

| 产品/类型 | 可借鉴 | 本项目用法 |
| --------- | ------ | ---------- |
| **GoodNotes / Notability** | 圆点/横纹纸、手写批注、分区贴纸 | 不规则横纹 SVG、`Ma Shan Zheng` 复盘、`sticky-note` |
| **马卡龙学习海报** | 低饱和多色 Bento、箭头引导、编号卡 | `bento-grid`、`nb-bento-4`、学习闭环 stepper |
| **Notion 学习模板** | 复习节奏表、行动清单 | `review-table`、`action-checklist` |

### 2.4 实时互动 / 社交（扩展）

| 产品 | 可借鉴 | 本项目用法 | Phase |
| ---- | ------ | ---------- | ----- |
| **Kahoot** | 房间号、同步答题、排行榜 | E4 PK、E5 排行 | P3 |
| **Quizlet Live** | 组队、进度对抗 | E4 双栏进度条 | P3 |

### 2.5 小程序设计规范

| 来源 | 可借鉴 | 本项目用法 |
| ---- | ------ | ---------- |
| **TDesign / uni-ui** | 触控 ≥44px、组件一致性 | `ux-enhancements.css`；uni-app 落地对齐 |
| **微信设计指南** | 正误色 `#07c160` / `#fa5151` | 实现层双轨 Token（§4.1） |
| **AI 学习小程序通用** | Loading 焦虑缓解、步骤文案轮播、假进度 | `loading` 四步 stepper + 心理学进度（方案 §6.8） |

### 2.6 综合取舍一句话

**交互学 Duolingo，气质学校园漫画/手账，增长学刷题 App 的进度与复盘，社交与商业化全部后置到 Phase 2+。**

---

## 三、设计决策记录（已人工确认）

| # | 维度 | 决策 |
| --- | ---- | ---- |
| 1 | 视觉方向 | **Bento 暖橙** + 水彩横纹；交互 Duolingo 单题闯关 |
| 2 | 文案 | **混合**：主流程温暖；Loading / 对错 / 结算可加漫画梗 |
| 3 | 字体 | **文楷**（全局 16px）+ **得意黑**（解析区）；归档方案含站酷快乐体/思源 |
| 4 | MVP 原型屏 | **9 屏**（含独立结算 skeleton 态） |
| 5 | 吉祥物 | 规范仍定义小课豆；**当前 Bento gallery 未挂载** |
| 5b | 顶栏金币 | **原型已移除**；gamification 留待产品/uni-app |
| 6 | 正误色 | 文档/原型可用漫画微调色；**实现**对齐 `#07c160` / `#fa5151` |
| 7 | 单题计时 | MVP **不做** |
| 8 | 生命值/灵韵 | MVP **不做** |
| 9 | 扩展页保真 | 中保真（同风格，Mock 可简化） |
| 10 | HTML 原型 | **已完成** 20 屏 gallery；见 [实施指引](./UI-HTML原型实施指引.md) |
| 11 | 背景纹理 | **不规则横纹 SVG**；屏内 + 画廊；**无方格** |

---

## 四、Design Token

### 4.1 色彩

#### 品牌 / 漫画层（背景与强调）

| Token | 色值 | 用途 |
| ----- | ---- | ---- |
| `paper-bg` | `#FFF6DC` | 页面背景、草稿纸 |
| `paper-warm` | `#FFEFB8` | 面板高亮、吉祥物肤色辅助 |
| `ink-black` | `#141414` | 描边、主文字 |
| `ink-muted` | `#4A4A4A` | 次要说明 |
| `accent-red` | `#E53935` | 拟声词、警示、漫画强调 |
| `accent-yellow` | `#FFBF00` | 帽衫色、高亮条、进度点缀 |
| `panel-white` | `#FFFDF7` | 卡片内底 |
| `halftone` | `rgba(20,20,20,0.06)` | 网点叠层 |

#### 反馈层（双轨）

| Token | 原型/文档建议色 | 生产实现（方案 §6.3） | 说明 |
| ----- | --------------- | --------------------- | ---- |
| `correct-comic` | `#6BCB77` 等偏黄绿 + 墨线描边 | **`#07c160`** | 答对选项、解析左边框 |
| `wrong-comic` | `#E53935` 或 `#FA5151` + 墨线 | **`#fa5151`** | 答错选项、震动反馈 |
| `correct-green-dark` | `#059652` | 按钮按下态 | 仅实现层 |
| `wrong-red-dark` | — | 按下/描边加深 | 仅实现层 |

> **原则：** HTML 原型演示可用漫画色；uni-app 提测前必须切换到微信规范绿/红。

### 4.2 字体

#### 当前 HTML 原型（v1.4）

| 角色 | 字体 | 回退 | 用途 |
| ---- | ---- | ---- | ---- |
| UI 正文 | 霞鹜文楷屏幕版 `LXGW WenKai Screen` | PingFang SC, 微软雅黑 | 全局 ` --bt-font` |
| 解析区 | 得意黑 `Smiley Sans` | 文楷 | `--bt-font-note` · `.bt-teacher-note` |

- 正文最小字号：**16px**
- 行高：正文 **1.5–1.7**
- 禁止使用 emoji 作为功能图标

#### 归档 / uni-app 备选

| 角色 | 字体 | 用途 |
| ---- | ---- | ---- |
| Display | 站酷快乐体 `ZCOOL KuaiLe` | 漫画层标题（`shared.css` / 旧原型） |
| Body | 思源宋体 `Noto Serif SC` | 漫画层正文 |
| Hand | 马善政 `Ma Shan Zheng` | 旧笔记本装饰 |

### 4.3 圆角、描边、阴影

| Token | 值 | 用途 |
| ----- | -- | ---- |
| `border-comic` | `2.5px solid #141414` | 面板、选项、按钮外轮廓 |
| `radius-card` | `12px`–`16px` | 选项卡、comic-panel |
| `radius-btn` | `12px` | 主按钮 |
| `shadow-hard` | `5px 5px 0 #141414` | 默认按钮/卡片立体 |
| `shadow-hard-sm` | `3px 3px 0 #141414` | 次要按钮 |
| 按下态 | `transform: translate(3px,3px)` + 阴影归零 | 模拟漫画按压 |

### 4.4 间距与触控

| 规则 | 值 |
| ---- | -- |
| 页面水平内边距 | `16px`（小程序 `32rpx`） |
| 选项最小高度 | **56px**（满足触控） |
| 选项间距 | ≥ **8px** |
| 手机逻辑画布 | **393 × 852**（iPhone 15 Pro） |
| 外壳圆角 | **44px** |

### 4.5 动效（语义描述）

| 场景 | 动效 | 时长建议 | 备注 |
| ---- | ---- | -------- | ---- |
| 面板入场 | 略带上移 + 微旋转归正 | 300ms | `panelDrop` |
| 答对 | 选项 bounce + 拟声词 pop | 200–300ms | 配合短音效 |
| 答错 | 容器 `shake` | 400ms | + `uni.vibrateShort()` |
| 进度条 | 填充 pulse（生成中） | 循环 | 非真进度，心理学曲线 |
| 减少动效 | `prefers-reduced-motion` 时禁用 shake/bounce | — | 无障碍 |

---

## 五、吉祥物规范（原创 IP）

### 5.1 角色设定（工作标题：**小课豆**）

| 属性 | 说明 |
| ---- | ---- |
| 定位 | 怕踢中学风格的原创 Q 版男生，**不是**阿衰本人 |
| 造型 | 圆脸、豆豆眼、**黄色连帽衫**（致敬漫画气质）、咖啡色短发 |
| 线条 | 与 UI 一致：2.5px 黑色描边，平涂色块 |
| 尺寸 | 角落头像 **48×48px**；庆祝态可放大至 72px |

### 5.2 出现规则

**设计规范（产品向）：** 各屏可固定展示 `mascot-chip`（推荐右上角）。

**当前 Bento HTML gallery：** 未引用 `mascots.svg`；加载页主视觉为 **`.bt-book-flip` 翻书动画**。uni-app 实现时可再评估是否恢复角落吉祥物。

### 5.3 情绪变体

| 类名（实现参考） | 表情/动作 | 使用页面 |
| ---------------- | --------- | -------- |
| `mascot--wave` | 挥手笑 | 首页 |
| `mascot--think` | 托腮/抱试卷 | 生成中、答题中 |
| `mascot--happy` | 竖大拇指、星星眼 | 答对、结算通关 |
| `mascot--sad` | 扁嘴、汗滴 | 答错 |
| `mascot--cheer` | 举小旗 | 结算复盘生成中（可选） |

### 5.4 与 Loading 插画关系

- **当前 gallery：** `.bt-book-flip` CSS 摊开本翻页 + `loading-steps.js` 四步文案
- **归档方案：** 小课豆抱题卷 / `mascot--think`
- 淘汰：孤立「大脑」作为主角色

---

## 六、组件语义清单

以下为设计层命名，uni-app 实现时可映射为 Vue 组件。

| 组件 | 说明 | 关键样式 |
| ---- | ---- | -------- |
| `comic-panel` | 漫画分格容器，可 `tilt-l/r` 微倾 | 白底、墨线、硬阴影 |
| `comic-title` | 首页大标题 | Display 字体 |
| `comic-subtitle` | 副标题说明 | Body、muted |
| `comic-textarea` | 单一大输入区 | 纸纹底、墨线框 |
| `comic-btn` | 主 CTA | 黄底或绿底、硬阴影、全宽 |
| `comic-btn--secondary` | 取消/次要 | 白底描边 |
| `option-card` | 答题选项 | 字母圆标 A/B/C/D |
| `option-card.selected` | 选中未提交（多选） | 黄底描边 |
| `option-card.correct` | 判分后正确 | 绿底+墨线 |
| `option-card.wrong` | 判分后错误 | 红底+墨线 |
| `speech-bubble` | 解析区 | 上三角指向选项；`.wrong` 红标 |
| `progress-bar` | 题号/生成共用 | 圆角 pill，黄/绿填充 |
| `score-ring` | 结算正确率环 | SVG 圆环 `stroke-dashoffset` |
| `report-section` | 复盘 Markdown 容器 | 标题+列表；接 towxml |
| `skeleton-line` | 复盘生成中占位 | 灰色条动画 |
| `mascot-chip` | 角落吉祥物 | 见 §5 |
| `sfx-label` | 拟声词「对了！」「啊哦」 | Display、倾斜、accent-red |
| `tip-card` | Loading 轮播贴士 | 浅黄底、虚线框 |
| `pass-banner` | 结算通关横幅 | 爆炸字「通关！」 |

### 6.3 Bento 暖橙层组件（`bento-theme.css` · 当前）

| 组件 | 说明 |
| ---- | ---- |
| `bt-screen` / `bt-scroll` | 屏内滚动区 |
| `bt-topbar` / `bt-quiz-header` | 顶栏；题号 `bt-progress-pill` |
| `bt-title` / `bt-section-title` | 标题阶梯 |
| `bt-btn` / `bt-btn-primary` / `bt-btn-secondary` | 主/次按钮 |
| `bt-card` / `bt-input-card` | 卡片容器 |
| `bt-opt` / `bt-opt-letter` | 选项；渐变底 + 对错态 |
| `bt-judge-btn` | 判断题大按钮 |
| `bt-feedback-bar` | 答对/错反馈条 |
| `bt-teacher-note` | 老师笔记解析（得意黑） |
| `bt-progress-line` | 进度条 |
| `bt-stepper` / `bt-step` | 生成四步 |
| `bt-book-flip` | 加载翻书动画 |
| `bt-tabbar` / `bt-tab` | 底部导航（≤5） |
| `bt-report-top` / `bt-metrics` | 通关报告顶区 |
| `theme-bento` | 挂载于 `<body>` |

### 6.4 归档：图文笔记层（`graphic-note.css`）

| 组件 | 说明 |
| ---- | ---- |
| `note-card` + `--yellow/blue/pink/green/red` | Bento 分区卡片 |
| `bento-grid` / `bento-card` / `bento-num` | 2×N 编号技巧大卡 |
| `sticky-note` / `--pink` | 便利贴解析/贴士 |
| `review-table` | 艾宾浩斯式复习节奏表 |
| `action-checklist` | 今日行动清单（☐/☑） |
| `note-screen-footer` | 屏底三图标说明条 |
| `note-hero-title` / `note-hero-sub` | 屏内主副标题 |
| `char-illus` + `study-char.svg` | 首页/总览角色区 |
| `phone-screen--dense` | 高密度屏内排版 |
| `theme-graphic-note` | 挂载于 `<body>`，启用全套笔记本风 |

### 6.2 背景分层（实现约定）

```
画廊 body
  ├─ 马卡龙渐变底
  ├─ ::before  paper-lines-page.svg（不规则横纹）+ 纸纹噪点
  └─ ::after   四角柔光斑

.phone-screen（屏内）
  ├─ 水彩 radial 渐变（粉/蓝/黄，按屏 3n 略变色相）
  ├─ paper-lines-screen.svg 平铺（浅色不规则横纹 + 弯河线）
  ├─ ::before  额外暖光斑
  └─ ::after   纸纹噪点（multiply）
```

- 各 `screen-item` 对横纹层使用 **不同 `background-position`**，避免多屏纹路完全对齐。
- 修改横纹疏密/弯曲度：编辑 SVG 源文件，勿改方格 CSS。

---

## 七、文案规范（混合语气）

### 7.1 原则

- **主流程**（输入、提交、下一题、再来一局）：温暖、清晰、少梗
- **等待与反馈**（Loading、答对/错、通关）：可加校园漫画口语与拟声

### 7.2 混合文案对照表（温暖 × 漫画）

| 场景 | 页面 | 语气档位 | 温暖版（主流程推荐） | 漫画版（可选/反馈） | 禁止 |
| ---- | ---- | -------- | -------------------- | ------------------- | ---- |
| 首页标题 | index | 温暖 | 「今天想学点什么？」 | 「今天学什么？」 | 说教、恐吓 |
| 首页副标题 | index | 温暖 | 「用一句话告诉 AI，剩下的交给我」 | 「写一句话就行～」 | 过长条款 |
| 吉祥物招呼 | index | 漫画 | — | 气泡：「我帮你拆成闯关题！」 | — |
| 主按钮 | index | 温暖 | 「开始学习」 | 「开始闯关」「开整」（A/B） | 含糊「确定」 |
| 输入占位 | index | 温暖 | 「例如：用比喻解释 TCP 三次握手」 | — | 空占位 |
| Loading 主文案 | loading | 漫画 | — | 「等等，我去翻翻笔记…」「正在出怪题…」 | 仅「加载中 0%」 |
| Loading 步骤 | loading | 温暖 | 「正在检索考点…」 | 四步 stepper ①–④ | 暴露真实 API 错误码 |
| Loading 贴士 | loading | 漫画 | — | 「别走开，题马上就来！」 | — |
| 题号进度 | quiz | 温暖 | 「3/10 题」 | 「第 3/10」+ 星级 | — |
| 单选提示 | quiz | 温暖 | 「点选一项即可提交」 | — | — |
| 多选提示 | quiz | 温暖 | 「选完后点确认提交」 | — | 自动提交 |
| 答对 SFX | quiz | 漫画 | — | 「对了！」「漂亮！」 | 嘲讽对手 |
| 答错 SFX | 漫画+安慰 | — | 「啊哦…」「错了也学到！」 | 人身攻击 |
| 老师笔记/解析 | quiz | 温暖+手写 | 「知识点」+ 正文 | `nb-teacher-note` 手写体 | 过长无结构 |
| 下一题按钮 | quiz | 温暖 | 「继续下一题」 | 「下一题 →」 | 末题仍显示下一题 |
| 末题按钮 | quiz | 温暖 | 「查看报告」 | — | — |
| 结算标题 | result | 温暖+轻梗 | 「闯关完成！」 | 「战报来啦！」 | — |
| 印章/评语 | result | 漫画 | — | 「及格啦！」「再来一次！」 | 羞辱低分用户 |
| 三句总结 | result | 温暖 | 结构化 bullet | — | 整页 Markdown 墙 |
| 再来一局 | result | 温暖 | 「再来一局」 | — | — |
| 分享 | result | — | 按钮置灰「即将上线」 | — | 诱导分享文案 |
| 取消生成 | loading | 温暖 | 「取消」 | — | 无反馈直接关页 |

### 7.3 场景对照表（精简索引）

| 场景 | 语气 | 推荐文案 | 避免 |
| ---- | ---- | -------- | ---- |
| 首页标题 | 温暖 | 「今天想学点什么？」 | 过长说教 |
| Loading 主文案 | 漫画 | 「正在翻课本…」「正在出怪题…」 | 冷冰冰「加载中」 |
| 答对 SFX | 漫画 | 「对了！」「漂亮！」 | — |
| 答错 SFX | 漫画+安慰 | 「啊哦…」「错了也学到！」 | 嘲讽用户 |
| 分享（MVP） | — | 按钮置灰「即将上线」 | 可点假分享 |

### 7.4 Mock 主题

全文档与原型统一使用 topic：**「TCP 三次握手」**，便于评审连贯性。

---

## 八、无障碍与合规

| 项 | 要求 | HTML 原型（v1.2.1） |
| -- | ---- | ------------------- |
| 对比度 | 正文与背景 ≥ 4.5:1；大字 ≥ 3:1 | `--ink-muted` 加深；屏内 `16px` 正文 |
| 色盲 | 对错除颜色外须有 ✓/✗ 或文案 | `.wrong::after` 显示 ✗；`.correct` 左边框强调 |
| 触控 | 可点击区域 ≥ 44×44px | 选项/按钮 `min-height` 48–52px |
| 焦点 | 键盘可见焦点环 | `:focus-visible` 马卡龙描边 |
| 动效 | 支持系统减少动态效果 | `@media (prefers-reduced-motion: reduce)` |
| 导航 | 画廊可跳过页头 | `.skip-link` → `#main-content` |
| IP | 禁止官方阿衰素材；吉祥物为原创 | `mascots.svg` 原创小课豆 |
| 内容安全 | MVP 不做 msgSecCheck；上线前见方案 Phase 2c | — |

实现要点已合入 [`prototypes/bento-theme.css`](../prototypes/bento-theme.css)（触控 ≥44px、`prefers-reduced-motion`、焦点态）。

归档：[`prototypes/ux-enhancements.css`](../prototypes/ux-enhancements.css)（gallery 未引用）。

---

## 九、与 uni-app 实现的映射提示

| 设计 Token / 组件 | uni-app 建议 |
| ----------------- | ------------ |
| 字体 | 小程序需 `@font-face` 或降级系统圆体 |
| 震动/音效 | `uni.vibrateShort` + 内置短音频（方案 §6.3） |
| 复盘 | `towxml` 或备选 B（方案 §2.3） |
| 颜色 | `pages.json` / CSS 变量统一 `correct-green`、`wrong-red` |
| 吉祥物 | 静态 PNG 或 inline SVG；按页面切换 image src |

---

## 十、修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.4.0 | 2026-05-26 | Bento 暖橙为当前 HTML；`bt-*` 组件；翻书 Loading；无顶栏金币；文楷+得意黑 |
| v1.3.0 | 2026-05-26 | §1.2 阿衰转译扩充；§2 市面参考分节；§7.2 混合文案对照表 |
| v1.2.1 | 2026-05-26 | UX 增强层：焦点环、最小触控、减少动效、页脚色点替代 emoji 图标 |
| v1.2.0 | 2026-05-26 | 笔记本风：不规则横纹 SVG、屏内+画廊分层；弃方格/书本外壳；HTML 20 屏已落盘 |
| v1.1.0 | 2026-05-26 | 图文笔记风 Bento 层；`graphic-note.css` |
| v1.0.0 | 2026-05-26 | 初版：阿衰意境 + Duolingo 交互定稿 |
