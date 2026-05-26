# UI HTML 原型 — 迭代清单（对照设计文档）

| 版本 | 日期 | 状态 |
| ---- | ---- | ---- |
| v1.3.0 | 2026-05-26 | Bento 暖橙全量重写 + 文档同步 |
| v1.2.0 | 2026-05-26 | 笔记本风（不规则横纹）+ 文档同步 |
| v1.0.0 | 2026-05-26 | 初版清单 |

**设计依据：** [UI设计风格与DesignSystem.md](./UI设计风格与DesignSystem.md) · [UI页面原型说明.md](./UI页面原型说明.md)

**主预览：** [`prototypes/index.html`](../prototypes/index.html) → `01` / `02` / `03`

**备选：** [`manga-heavy-mvp.html`](../prototypes/manga-heavy-mvp.html)（4 屏重度漫画风，未随 Bento 更新）

---

## 一、现状 vs 目标

| 维度 | 当前 `prototypes/` | 设计文档目标 |
| ---- | ------------------ | ------------ |
| 主主题 | `theme-bento` + `bento-theme.css` | ✅ v1.3 |
| 样式链 | `shared.css` → `bento-theme.css` | ✅ |
| MVP 屏数 | **9** | ✅ |
| 扩展屏 | **11** | ✅ |
| 顶栏 | 问候语 / 题号 pill；**无金币** | ✅ |
| Loading 主视觉 | CSS **翻书动画** `.bt-book-flip` | ✅ |
| 解析 | `.bt-teacher-note` + 得意黑 | ✅ |
| 背景 | 水彩横纹 SVG（保留） | ✅ |
| 吉祥物 | gallery **未引用** `mascots.svg` | ⚠️ 设计规范仍保留 IP，实现时再定 |
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
| **K** | 翻书 Loading / 移除金币 / 解析字体 | ✅ v1.3 |

---

## 三、MVP 9 屏 — 验收对照

| # | 屏 | 要点 | 状态 |
| --- | -- | ---- | ---- |
| 1 | 首页 | `bt-title`、输入卡、话题卡、底 Tab；无金币 | ✅ |
| 2 | 生成中 | `bt-book-flip`、`loading-steps.js`、四步 stepper | ✅ |
| 3 | 单选 | `bt-opt` 渐变、题号 pill | ✅ |
| 4 | 多选 | 确认提交 | ✅ |
| 5 | 判断 | `bt-judge-btn` | ✅ |
| 6 | 答对 | `bt-feedback-bar` + `bt-teacher-note` | ✅ |
| 7 | 答错 | 红选项 + 老师笔记 | ✅ |
| 8 | 通关报告 | `bt-report-top`、指标卡、Bento 格 | ✅ |
| 9 | skeleton | 步骤 + skeleton | ✅ |

---

## 四、资源文件清单

| 文件 | 用途 |
| ---- | ---- |
| `bento-theme.css` | ★ 主主题 `theme-bento`、`bt-*` 组件、翻书动画 |
| `loading-steps.js` | 生成页进度 demo |
| `paper-lines-page.svg` | 画廊横纹 |
| `paper-lines-screen.svg` | 屏内横纹 |
| `graphic-note.css` 等 | 归档，gallery 不引用 |
| `mascots.svg` | 归档，待 uni-app 再评估 |

---

## 五、后续可选迭代（非阻塞）

| 优先级 | 任务 | 说明 |
| ------ | ---- | ---- |
| P1 | uni-app 映射 `bt-*` | 组件化与 Token 变量 |
| P2 | 金币 gamification | 若产品保留，重新设计角标（非原型回滚） |
| P2 | 小课豆回归 | 可选：加载页副角标或结算页 |
| P3 | 深色模式 | 当前仅浅色 Bento |
| P3 | 翻书动画 Lottie | 小程序性能评估 |

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
| v1.3.0 | 2026-05-26 | Bento 暖橙；翻书 Loading；无金币；得意黑解析区 |
| v1.2.0 | 2026-05-26 | 笔记本不规则横纹 |
| v1.0.0 | 2026-05-26 | 初版任务清单 |
