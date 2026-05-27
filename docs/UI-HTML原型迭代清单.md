# 知练 — UI HTML 原型迭代清单（对照设计文档）

| 版本 | 日期 | 状态 |
| ---- | ---- | ---- |
| v1.6.0 | 2026-05-27 | 参考首页增强、Loading IP、答题反馈 demo、灵韵条（原型探索） |
| v1.5.0 | 2026-05-26 | 产品品牌：知练（KnowPractice） |
| v1.4.0 | 2026-05-26 | 悬浮胶囊底栏 + 底区纸纹连续；布局/图标/进度条 |
| v1.3.0 | 2026-05-26 | Bento 暖橙全量重写 + 文档同步 |
| v1.2.0 | 2026-05-26 | 笔记本风（不规则横纹）+ 文档同步 |
| v1.0.0 | 2026-05-26 | 初版清单 |

**设计依据：** [UI设计风格与DesignSystem.md](./UI设计风格与DesignSystem.md) · [UI页面原型说明.md](./UI页面原型说明.md)

**主预览：** [`prototypes/index.html`](../prototypes/index.html) → `01`（MVP 9 屏）/ `02` / `03`（报告 7 屏，含 Tab ⑥⑦）  
**网页展示稿：** [`prototypes/ui.html`](../prototypes/ui.html)（与 `01` 屏① 同步维护）

**Tab 子页：** 已并入 [`03_reports_social.html`](../prototypes/03_reports_social.html)（`#tab-bank` / `#tab-medal`）；[`04_tab_pages.html`](../prototypes/04_tab_pages.html) 仅跳转  
**归档备选：** [`manga-heavy-mvp.html`](../prototypes/manga-heavy-mvp.html)（未随 Bento v1.6 维护）

---

## 一、现状 vs 目标

| 维度 | 当前 `prototypes/` | 设计文档目标 |
| ---- | ------------------ | ------------ |
| 主主题 | `theme-bento` + `bento-theme.css` | ✅ v1.3 |
| 样式链 | `shared.css` → `bento-theme.css` | ✅ |
| MVP 屏数 | **9**（仅 `01`） | ✅ |
| Tab 子页 | `03` 屏⑥⑦（题库 / 勋章）；非 MVP；`04` 重定向 | ✅ v1.7.3 |
| 扩展屏 | **11** | ✅ |
| 顶栏 | 问候语 / 题号 pill；**无金币·无 XP 徽章** | ✅ |
| 布局 | `bt-notch-safe`；列表/答题顶对齐；生成中居中 | ✅ v1.4 |
| 图标 | 输入铅笔；答对圆章勾 | ✅ v1.4 |
| 进度条 | 暖橙 8px 渐变，无流光 | ✅ v1.4 |
| Loading 主视觉 | CSS **翻书动画** `.bt-book-flip` | ✅ |
| 解析 | `.bt-teacher-note` + 得意黑 | ✅ |
| 背景 | 水彩横纹 SVG（保留） | ✅ |
| 底栏 | `bt-tabbar-float` 悬浮胶囊；底区纸纹与内容连续 | ✅ v1.4 |
| 吉祥物 | Loading 引用 `mascots.svg#mascot-think` + 气泡文案 | ✅ v1.6（gallery） |
| 参考首页 | `ui.html` + `ui-ref-home.css`（`.ref-home`） | ✅ v1.6 |
| 灵韵（原型） | 答题顶栏 `.bt-spirit` 五段能量条；**产品 MVP 仍不做惩罚** | ⚠️ 仅原型探索 |
| 旧笔记本主题 | `graphic-note.css` 等归档 | ✅ 不阻塞 |

---

## 二、已完成里程碑

| 阶段 | 内容 | 状态 |
| ---- | ---- | ---- |
| A | 拆分 `shared.css` + gallery 20 屏 | ✅ |
| B | `graphic-note.css` Bento / 便利贴 | ✅ → 已由 Bento 层替代 |
| C | 总览六幕 showcase | ✅ |
| D | 扩展/报告页卡片化 | ✅ |
| E | 马卡龙水彩 + 横纹 SVG | ✅ |
| F | `ux-enhancements.css` | ✅ → 合入 `bento-theme` 要点 |
| G | 书本风实验 | ⏪ 已回退 |
| H | `paper-lines-*.svg` | ✅ 继续用于 Bento |
| I | 设计文档 v1.2 同步 | ✅ |
| **J** | **Bento 暖橙高保真重写** | ✅ v1.3 |
| **K** | **悬浮胶囊底栏 + 底区纸纹连续** | ✅ v1.4 |
| **K** | 翻书 Loading / 移除金币 / 解析字体 | ✅ v1.3 |
| **L** | **参考首页 UX 增强**（`ui.html` / `01` 屏①） | ✅ v1.6 |
| **M** | **Loading IP + stepper 动效** | ✅ v1.6 |
| **N** | **答题反馈动效 + `quiz-feedback-demo.js`** | ✅ v1.6 |

---

## 三、MVP 9 屏 — 验收对照

| # | 屏 | 要点 | 状态 |
| --- | -- | ---- | ---- |
| 1 | 首页 | `ref-home`：纯文案标题、compose 输入+示例、热门主题横滑、连胜、未完成关卡「继续」；`index` 总览已对齐 | ✅ |
| 2 | 生成中 | `bt-book-flip`、小皮 IP 气泡、`loading-steps.js`、四步 stepper 高亮/对勾动效 | ✅ |
| 3 | 单选 | `bt-opt`、题号 pill、顶栏 `.bt-spirit` 五段条（原型） | ✅ |
| 4 | 多选 | 确认提交、顶栏灵韵条 | ✅ |
| 5 | 判断 | `bt-judge-btn`、顶栏灵韵条 | ✅ |
| 6 | 答对 | 反馈条动效 + `bt-teacher-note`；`data-feedback-demo` 循环；题下 `bt-progress-line` | ✅ |
| 7 | 答错 | 同上；灵韵 2/5 + 低余量脉冲；无「第 1 关」副行 | ✅ |
| 8 | 通关报告 | `bt-report-top`、指标卡、Bento 格 | ✅ |
| 9 | skeleton | 步骤 + skeleton | ✅ |

---

## 四、资源文件清单

| 文件 | 用途 |
| ---- | ---- |
| `ui-ref-home.css` | ★ `ui.html` / `01` 屏① 参考首页（点阵页外 + 屏内 `.ref-home`） |
| `bento-theme.css` | ★ 主主题 `theme-bento`、`bt-*` 组件、翻书/反馈/灵韵/ stepper 动效 |
| `loading-steps.js` | 生成页进度 demo + IP 气泡文案同步 |
| `quiz-feedback-demo.js` | 屏 6/7 反馈动效循环 demo（进入视口播放） |
| `ref-home-topics.js` | 参考首页「换一批」热门主题三组轮换 demo |
| `paper-lines-page.svg` | 画廊横纹 |
| `paper-lines-screen.svg` | 屏内横纹 |
| `mascots.svg` | Loading 屏 `mascot-think`；其余屏待评估 |
| `graphic-note.css` 等 | 归档，gallery 不引用 |

---

## 五、后续可选迭代（非阻塞）

| 优先级 | 任务 | 说明 |
| ------ | ---- | ---- |
| ~~P1~~ | ~~`index.html` 首页与 `ui.html` 对齐~~ | ✅ v1.6.1：总览 showcase 已换 `.ref-home` |
| ~~P1~~ | ~~Tab 子页高保真~~ | ✅ v1.7.3：并入 `03` 报告页 ⑥⑦；`04` 跳转；IA §1.3 / §四 |
| P1 | uni-app 映射 `bt-*` | 组件化与 Token 变量 |
| ~~P2~~ | ~~答题反馈 demo 节奏~~ | ✅ v1.6.2：各阶段延时约 +40%，循环间隔加长 |
| P2 | 灵韵机制产品定稿 | 原型有 `.bt-spirit`；PRD 倾向 MVP 不做惩罚式红心 |
| P2 | 金币 gamification | 若产品保留，重新设计角标（非原型回滚） |
| P2 | 小课豆回归 | 可选：加载页副角标或结算页（gallery 不展示） |
| ~~P2~~ | ~~「换一批」热门主题~~ | ✅ v1.6.3：`ref-home-topics.js` 三组轮换 + 淡入动效 |
| P3 | 深色模式 | 当前仅浅色 Bento |
| P3 | 翻书动画 Lottie | 小程序性能评估 |
| ~~P3~~ | ~~`02` / `03` 扩展屏视觉复查~~ | ✅ v1.6.2：底栏旗帜/勋章、去 XP 徽章、画廊导航补 `ui.html` |

---

## 六、预览

```bash
npx serve d:\AI-Learn\prototypes
```

Checklist 详见 [UI-HTML原型实施指引.md §八](./UI-HTML原型实施指引.md)。

---

## 七、修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.7.2 | 2026-05-27 | Tab 移回独立 `04`；`01` 恢复纯 MVP 9 屏 |
| v1.7.1 | 2026-05-27 | Tab 曾并入 `01`（已回退） |
| v1.7.0 | 2026-05-27 | Tab 题库/勋章屏；MVP↔Tab IA；总览 Tab 区；`manga-heavy` 归档标注 |
| v1.6.3 | 2026-05-27 | 首页「换一批」热门主题 demo（`ref-home-topics.js`） |
| v1.6.2 | 2026-05-27 | 反馈 demo 节奏调慢；02/03/01/index 底栏与报告顶栏统一 |
| v1.6.1 | 2026-05-27 | `index.html` 总览首页与 `ui.html` 对齐（`.ref-home`） |
| v1.6.0 | 2026-05-27 | 参考首页增强；Loading IP；stepper/反馈动效；灵韵条原型；资源清单更新 |
| v1.4.0 | 2026-05-26 | 悬浮胶囊底栏；底区纸纹连续；布局/图标/进度条 |
| v1.3.0 | 2026-05-26 | Bento 暖橙；翻书 Loading；无金币；得意黑解析区 |
| v1.2.0 | 2026-05-26 | 笔记本不规则横纹 |
| v1.0.0 | 2026-05-26 | 初版任务清单 |
