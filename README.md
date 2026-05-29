# 知练 · KnowPractice

**输入学习目标，获得 AI 结构化练测与复盘。**

面向大学生自学、职场考证与企业内训的微信小程序（uni-app），以「以测代学」为核心：用户描述想学的内容 → AI 生成练测 → 单题作答与讲解 → 通关复盘报告。

| 项 | 说明 |
| --- | --- |
| 产品名 | **知练**（英文 **KnowPractice**） |
| 交互形态 | 关卡式练测（导航仍可用「闯关」等功能文案，非对外品牌名） |
| 静态原型 | [`prototypes/index.html`](prototypes/index.html)（Bento 暖橙 · `bento-theme.css`） |
| **网页 UI 展示稿** | [`prototypes/ui.html`](prototypes/ui.html)（`ui-ref-home.css` · 与 01 屏① 同步） |
| 设计文档 | [`docs/UI设计文档索引.md`](docs/UI设计文档索引.md) |
| **MVP 开发文档** | [`docs/文档总索引.md`](docs/文档总索引.md) → [开发实施指南](docs/MVP开发实施指南.md) |

## 本地预览原型

```bash
npx serve prototypes
```

浏览器打开 `http://localhost:3000/index.html`（端口以终端为准）。

## 仓库说明

- `prototypes/` — HTML 高保真 gallery（MVP / 扩展 / 报告）；脚本 `loading-steps.js`、`quiz-feedback-demo.js`
- `docs/` — 需求、方案、UI Design System、**MVP 开发实施指南**（文档先行，代码未启动）
- `backend/`、`uniapp/` — **待 Sprint 1–2 创建**（见开发文档）
- 历史文档文件名仍含「交互式AI闯关学习」，内容为项目早期称谓；**对外品牌统一为知练**
