# 知练（KnowPractice）— MVP 后端 API 与数据契约

> **文档性质：** 后端开发规格（Sprint 1 执行依据）。  
> **上级文档：** [MVP开发实施指南.md](./MVP开发实施指南.md)

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.1.0 | 2026-05-29 | 异步任务 + JSONL 流式出题；增量 `questions` 轮询 |
| v1.0.0 | 2026-05-29 | 初版：接口、Schema、Prompt、LangChain 链路 |

---

## 一、接口一览

| 接口 | 方法 | 说明 | 建议超时 |
| ---- | ---- | ---- | -------- |
| `/health` | GET | 健康检查 | — |
| `/api/v1/quiz/generate` | POST | 创建出题任务，立即返回 `job_id` | 15s |
| `/api/v1/quiz/jobs/{job_id}` | GET | 轮询任务状态；`questions` 随流式生成递增 | 15s |
| `/api/v1/quiz/report` | POST | 根据答题记录生成复盘 | 30s |

**Base URL（本地）：** `http://127.0.0.1:8000`

**出题流程（v1.1）：**

1. `POST /generate` → `202` + `{ job_id, status: "pending" }`
2. 后台 `astream` + JSONL 逐行解析，每完成一题即追加到 Job
3. 前端轮询 `GET /jobs/{job_id}`；`ready=true` 且 `questions.length >= 1` 即可进入答题
4. `status=completed` 时 `result` 含完整 10 题

---

## 二、请求与响应

### 2.1 POST `/api/v1/quiz/generate`

**请求：**

```json
{
  "topic": "光合作用"
}
```

**响应（202）：**

```json
{
  "job_id": "job_20260529_abc123",
  "status": "pending"
}
```

### 2.2 GET `/api/v1/quiz/jobs/{job_id}`

**响应（200）：**

```json
{
  "job_id": "job_20260529_abc123",
  "status": "running",
  "quiz_id": "q_20260529_abc123",
  "topic": "光合作用",
  "questions": [
    {
      "id": "q1",
      "type": "single",
      "stem": "光合作用的主要场所是？",
      "options": ["线粒体", "叶绿体", "细胞核", "液泡"],
      "answer": 1,
      "explanation": "叶绿体含有叶绿素，是光合作用的主要场所。"
    }
  ],
  "total_expected": 10,
  "ready": true,
  "stream_preview": "",
  "result": null,
  "error": null
}
```

| 字段 | 说明 |
| ---- | ---- |
| `status` | `pending` / `running` / `completed` / `failed` |
| `questions` | 已解析题目列表，流式递增 |
| `ready` | `questions.length > 0` |
| `result` | 仅 `completed` 时有完整 `GenerateQuizResponse` |
| `stream_preview` | 仅供调试，**前端不向用户展示** |

**错误：**

| 状态码 | 场景 |
| ------ | ---- |
| 404 | `job_id` 不存在或已过期 |
| 422 | 请求体校验失败（topic 为空等） |
| 502 | 任务失败（JSON 解析失败、LLM 未配置等） |
| 504 | 后台任务整请求超时 |

### 2.3 POST `/api/v1/quiz/report`

**请求：**

```json
{
  "quiz_id": "q_20260529_abc123",
  "topic": "光合作用",
  "questions": [ "...同上..." ],
  "answers": [
    {
      "question_id": "q1",
      "selected": 1,
      "correct": true
    }
  ]
}
```

**响应（200）：**

```json
{
  "score": 7,
  "total": 10,
  "correct_rate": 0.7,
  "report": "## 整体表现\n\n正确率 70%，...\n\n## 复习建议\n\n1. ..."
}
```

---

## 三、数据契约（snake_case）

### 3.1 命名策略

| 层 | 命名 | 示例 |
| -- | ---- | ---- |
| Python / HTTP JSON | snake_case | `quiz_id`, `correct_rate` |
| TypeScript 类型 | snake_case | 与 API 一致，不做 camelCase 转换 |

### 3.2 题型枚举

| `type` | 说明 | `options` | `answer` |
| ------ | ---- | --------- | -------- |
| `single` | 单选 | 4 个字符串 | `number`（0–3） |
| `multiple` | 多选 | ≥4 个字符串 | `number[]`（正确选项下标） |
| `judge` | 判断 | `["正确","错误"]` 或省略由前端补全 | `number`（0=正确，1=错误） |

**判断题语义：** `answer` 是**正确选项的下标**，不是布尔值。  
例：题干「TCP 使用四次握手建立连接」→ 应选「错误」→ `answer: 1`。

### 3.3 TypeScript 类型（`uniapp/src/types/quiz.ts`）

```typescript
export type QuestionType = 'single' | 'multiple' | 'judge'

export interface Question {
  id: string
  type: QuestionType
  stem: string
  options?: string[]
  answer: number | number[]
  explanation: string
}

export interface QuizSession {
  quiz_id: string
  topic: string
  questions: Question[]
  generating?: boolean
  job_id?: string
  total_expected?: number
}

export interface UserAnswer {
  question_id: string
  selected: number | number[]
  correct: boolean
}

export interface GenerateQuizResponse {
  quiz_id: string
  topic: string
  questions: Question[]
}

export interface ReportResponse {
  score: number
  total: number
  correct_rate: number
  report: string
}
```

### 3.4 Python Schema 校验规则（`backend/app/schemas/quiz.py`）

实现时需包含 `@model_validator`：

| 题型 | 校验 |
| ---- | ---- |
| `single` | `options` 长度 = 4；`answer` 为 int 且 0 ≤ answer < 4 |
| `multiple` | `options` 长度 ≥ 4；`answer` 为非空 int 列表，元素均在 options 范围内 |
| `judge` | `answer` 为 0 或 1；`options` 可选，缺省时后端或前端补 `["正确","错误"]` |
| 全局 | `questions` 长度必须 = 10；每题 `id` 唯一；`stem` / `explanation` 非空 |

---

## 四、LangChain 链路设计

### 4.1 MVP 使用 / 不使用

| 模块 | MVP | 说明 |
| ---- | --- | ---- |
| `ChatOpenAI`（DeepSeek / 智谱） | ✅ | 大模型调用 |
| `ChatPromptTemplate` | ✅ | Prompt 版本化 |
| `astream` + JSONL 解析 | ✅ | 流式出题，逐题追加 Job |
| `PydanticOutputParser` | ✅ | 单行题目 JSON 校验 |
| `response_format: json_object` | ✅ | 非流式/复盘路径可选 |
| `OutputFixingParser` | ⚠️ | 仅非 JSON Mode 流式失败时兜底 |
| Tavily / Retriever | ❌ | Phase 2 RAG |
| LangGraph / Vector DB | ❌ | Phase 2 |

### 4.2 Chain 1：QuizStreamGenerationChain

- **输入：** `{ topic: string }`
- **输出：** 后台任务增量写入 `questions[]`，完成后 `{ quiz_id, topic, questions[10] }`
- **格式：** JSONL（每行一道题），`id` 为 `q1`…`q10`
- **选项：** 文本**不带** `A.` / `B.` 前缀（前端单独渲染字母徽标）

**解析失败：**

1. 单行 `Question` Pydantic 校验
2. 完成后 `questions` 数量 ≠ 10 → 任务 `failed`
3. HTTP 轮询侧看到 `status=failed` + `error`

### 4.3 Chain 2：ReportGenerationChain

- **输入：** `{ topic, questions[], answers[] }`
- **输出：** Markdown 字符串（放入 `report` 字段）
- **格式约束：** 标题、列表、加粗为主；**避免复杂表格**（towxml 兼容）

### 4.4 超时策略

| 约束 | 数值 |
| ---- | ---- |
| `POST /generate` | 立即 `202`，< 1s |
| 首题就绪 | 通常 5–20s（视模型） |
| 10 题全部完成 | 通常 15–90s |
| 轮询间隔 | 前端 600ms（等待下一题时 350ms） |
| 后台任务 `request_total_timeout` | 180s |
| `POST /report` | 30s |

**MVP 应对：**

1. 首题就绪即跳转答题，后续题后台同步
2. `beginQuizSession()` 重置 `quizProgress` / `quizAnswers`
3. 轮询失败 Toast + 返回首页；任务 `failed` 显示 `error`

---

## 五、环境变量（`.env.example`）

```env
DEEPSEEK_API_KEY=sk-xxxxxxxx
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
LLM_CALL_TIMEOUT=25
REQUEST_TOTAL_TIMEOUT=55
```

> **注意：** `DEEPSEEK_BASE_URL` 必须含 `/v1` 后缀。

可选开发开关（文档建议，实现时按需）：

```env
# MOCK_LLM=true  # 无 API Key 时返回 fixture，仅供本地 UI 联调
```

---

## 六、Prompt 模板骨架

### 6.1 出题 Prompt（`backend/app/prompts/quiz_generation.py`）

**System：**

```
你是知练（KnowPractice）的出题助手。根据用户给出的学习主题，生成恰好 10 道练测题。

要求：
1. 题型在 single（单选）、multiple（多选）、judge（判断）中自动搭配，三种题型都应出现
2. 单选题 4 个选项；多选题 4 个选项，正确答案 2–3 个
3. 判断题 answer 为正确选项的下标：0=「正确」，1=「错误」
4. 每题必须有通俗易懂的 explanation
5. 严格输出 JSON，符合以下 schema：{format_instructions}
6. 不要输出 markdown 代码块包裹，只输出纯 JSON
```

**User：**

```
学习主题：{topic}
```

### 6.2 复盘 Prompt（`backend/app/prompts/report_generation.py`）

**System：**

```
你是知练的学习复盘助手。根据用户的答题记录，生成 Markdown 格式的学习复盘报告。

要求：
1. 包含：整体表现、核心知识点回顾、易错题分析、复习建议
2. 语气鼓励、专业克制
3. 使用 ## 标题、列表和加粗，不要使用表格
4. 篇幅 300–600 字
```

**User：**

```
主题：{topic}
答题记录：
{answers_summary}
```

---

## 七、后端目录与文件清单

```
backend/
├── app/
│   ├── main.py                 # FastAPI 入口、CORS、路由挂载
│   ├── config.py               # pydantic-settings 读取 .env
│   ├── routers/
│   │   └── quiz.py             # generate / report 端点
│   ├── chains/
│   │   ├── quiz_generation.py
│   │   └── report_generation.py
│   ├── schemas/
│   │   └── quiz.py             # Pydantic 模型 + validator
│   └── prompts/
│       ├── quiz_generation.py
│       └── report_generation.py
├── tests/
│   └── test_schemas.py         # 三题型校验单测
├── requirements.txt
└── .env.example
```

### 7.1 `requirements.txt` 建议依赖

```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic>=2.9.0
pydantic-settings>=2.6.0
python-dotenv>=1.0.0
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-core>=0.3.0
pytest>=8.3.0
httpx>=0.27.0
```

---

## 八、Schema 单元测试用例（`tests/test_schemas.py`）

| # | 用例 | 期望 |
| - | ---- | ---- |
| 1 | 合法 single 题 | 通过 |
| 2 | single answer=4（越界） | 422 |
| 3 | multiple answer 非列表 | 422 |
| 4 | multiple 漏选/多选与 answer 长度不一致（前端判分逻辑单测另写） | — |
| 5 | judge answer=2 | 422 |
| 6 | questions 长度 ≠ 10 | 422 |
| 7 | 重复 question id | 422 |

---

## 九、G1 验收清单

- [ ] `GET /health` → `{"status":"ok"}`
- [ ] `POST /api/v1/quiz/generate` 返回 `202` + `job_id`
- [ ] `GET /api/v1/quiz/jobs/{id}` 流式递增 `questions`，最终 `completed` 含 10 题
- [ ] `POST /api/v1/quiz/report` 返回 Markdown 字符串
- [ ] `/docs` OpenAPI 可浏览、可 Try it out
- [ ] `pytest tests/` 全部通过
- [ ] `.env` 不入 Git（见 `.gitignore`）

---

## 修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.1.0 | 2026-05-29 | 异步任务 + 流式 JSONL 出题；轮询契约 |
| v1.0.0 | 2026-05-29 | 初版 API 与数据契约 |
