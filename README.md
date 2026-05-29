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

- `prototypes/` — HTML 高保真 gallery（MVP / 扩展 / 报告）
- `docs/` — 需求、方案、UI Design System、MVP 开发实施指南
- `backend/` — FastAPI + LangChain 后端（见 `backend/.env.example`）
- `uniapp/` — **官方** `dcloudio/uni-preset-vue#vite-ts` 脚手架（Vue 3 + TS + Vite）

## 本地开发

### 后端

默认使用 **智谱 GLM-4.5-air**（OpenAI 兼容接口）。在 `backend/.env` 配置：

```env
LLM_API_KEY=你的智谱APIKey
LLM_MODEL=glm-4.5-air
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_CALL_TIMEOUT=120
REQUEST_TOTAL_TIMEOUT=180
MOCK_LLM=false
```

也可改用 DeepSeek（设置 `DEEPSEEK_API_KEY` 等，且不要设置 `LLM_API_KEY`）。

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # 填入 DEEPSEEK_API_KEY
uvicorn app.main:app --reload --port 8000
pytest tests/ -v
```

### 小程序前端（官方脚手架）

```bash
cd uniapp
npm install
npm run dev:mp-weixin
```

微信开发者工具有两种导入方式：

| 方式 | 路径 | 说明 |
| ---- | ---- | ---- |
| 推荐（热更新） | `uniapp/dist/dev/mp-weixin` | 先执行 `npm run dev:mp-weixin` |
| 构建产物 | `uniapp/dist/build/mp-weixin` | 先执行 `npm run build:mp-weixin` |
| 仓库根目录 | `AI-Learn/`（根目录） | 已配置 `project.config.json` 的 `miniprogramRoot` 指向构建目录；改代码后需重新编译 |

勾选「不校验合法域名」。联调时修改 `uniapp/src/config.ts` 中 `BASE_URL`；真机请改局域网 IP。

`npm install` 后会自动将 `towxml` 复制到 `src/wxcomponents/towxml`。
