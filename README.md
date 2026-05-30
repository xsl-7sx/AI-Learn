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

默认使用 **DeepSeek**（OpenAI 兼容接口 + JSON Mode）。在 `backend/.env` 配置：

```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的DeepSeekKey
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_JSON_MODE=true
MOCK_LLM=false
```

也可改用智谱（`LLM_PROVIDER=zhipu` 并设置 `LLM_API_KEY` 等）。

出题接口为**异步任务 + 流式 JSONL**：

1. `POST /api/v1/quiz/generate` → `202` + `job_id`
2. 轮询 `GET /api/v1/quiz/jobs/{job_id}`，`questions` 逐题递增
3. **首题就绪**即进入答题页，其余题目后台继续拉取

复盘接口返回**结构化 JSON**（`学习复盘报告` 对象）；前端解析为卡片 UI，并在 AI 返回前用本地摘要兜底。

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # 填入 DEEPSEEK_API_KEY
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pytest tests/ -v
```

**MVP TDD 验收（Mock LLM）：** 见 [MVP-TDD验收.md](./MVP-TDD验收.md)；前端在 `uniapp/` 执行 `npm test`。

真机预览时后端必须加 `--host 0.0.0.0`，否则手机连不上电脑。

### 小程序前端（官方脚手架）

```bash
cd uniapp
npm install
cp .env.development.example .env.development   # Windows: copy .env.development.example .env.development
# 编辑 .env.development，把 VITE_API_BASE_URL 改成你电脑的局域网 IP
npm run dev:mp-weixin
```

微信开发者工具有两种导入方式：

| 方式 | 路径 | 说明 |
| ---- | ---- | ---- |
| 推荐（热更新） | `uniapp/dist/dev/mp-weixin` | 先执行 `npm run dev:mp-weixin` |
| 构建产物 | `uniapp/dist/build/mp-weixin` | 先执行 `npm run build:mp-weixin` |
| 仓库根目录 | `AI-Learn/`（根目录） | 已配置 `project.config.json` 的 `miniprogramRoot` 指向构建目录；改代码后需重新编译 |

勾选「不校验合法域名」。

**真机联调：** `127.0.0.1` 在手机上指向手机自身，会报 `ERR_CONNECTION_REFUSED`。在 `uniapp/.env.development` 配置：

```env
VITE_API_BASE_URL=http://192.168.x.x:8000
```

查电脑 IP：Windows 运行 `ipconfig`，手机与电脑需在同一 Wi-Fi。

`npm install` 后会自动将 `towxml` 复制到 `src/wxcomponents/towxml`。

### 结算页结构（result）

| 区块 | 组件 | 说明 |
| ---- | ---- | ---- |
| 成绩环 + 鼓励语 | `BentoEnergyPool` | 本地即时展示正确率；底部「知识点掌握情况」为快捷入口 |
| 知识点掌握情况 | `BentoKnowledgePanel` | **独立卡片**，默认收起；由答题解析/题干即时生成，AI 返回后合并 |
| AI 复盘报告 | `BentoReportCards` | **独立卡片**，默认收起；整体表现 / 易错题分析 / 复习建议 |
| 兜底 | `ReportView` | 仅当 JSON 解析失败且无本地摘要时展示 Markdown |
