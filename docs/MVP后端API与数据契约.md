# 知练（KnowPractice）— MVP 后端 API 与数据契约

> **文档性质：** 后端开发规格（Sprint 1 执行依据）。  
> **上级文档：** [MVP开发实施指南.md](./MVP开发实施指南.md)

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-29 | 初版：接口、Schema、Prompt、LangChain 链路 |

---

## 一、接口一览

| 接口 | 方法 | 说明 | 建议超时 |
| ---- | ---- | ---- | -------- |
| `/health` | GET | 健康检查 | — |
| `/api/v1/quiz/generate` | POST | 根据 topic 生成 10 题 | 60s |
| `/api/v1/quiz/report` | POST | 根据答题记录生成复盘 | 30s |

**Base URL（本地）：** `http://127.0.0.1:8000`

---

## 二、请求与响应

### 2.1 POST `/api/v1/quiz/generate`

**请求：**

```json
{
  "topic": "光合作用"
}
```

**响应（200）：**

```json
{
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
  ]
}
```

**错误：**

| 状态码 | 场景 |
| ------ | ---- |
| 422 | 请求体校验失败（topic 为空等） |
| 502 | LLM 输出 JSON 解析失败（含 1 次 OutputFixingParser 后仍失败） |
| 504 | 整请求超时（> 55s） |

### 2.2 POST `/api/v1/quiz/report`

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
| `ChatOpenAI`（DeepSeek） | ✅ | 大模型调用 |
| `ChatPromptTemplate` | ✅ | Prompt 版本化 |
| `PydanticOutputParser` | ✅ | 强制 JSON 结构 |
| `OutputFixingParser` | ✅ | 解析失败自动修复，**最多 1 次** |
| Tavily / Retriever | ❌ | Phase 2 RAG |
| LangGraph / Vector DB | ❌ | Phase 2 |

### 4.2 Chain 1：QuizGenerationChain

- **输入：** `{ topic: string }`
- **输出：** `{ quiz_id, topic, questions[10] }`
- **quiz_id 生成：** 服务端生成，如 `q_{date}_{uuid8}`

**JSON 解析失败重试：**

1. `PydanticOutputParser` 校验
2. 失败 → `OutputFixingParser` 修复，最多 1 次
3. 仍失败 → HTTP 502

### 4.3 Chain 2：ReportGenerationChain

- **输入：** `{ topic, questions[], answers[] }`
- **输出：** Markdown 字符串（放入 `report` 字段）
- **格式约束：** 标题、列表、加粗为主；**避免复杂表格**（towxml 兼容）

### 4.4 超时策略

| 约束 | 数值 |
| ---- | ---- |
| 单次 LLM 调用 | 通常 15–30s |
| OutputFixingParser 重试 | 再加 15–30s |
| 前端 `uni.request` timeout | 60s（微信硬上限） |

**MVP 应对：**

1. Prompt 强约束 + JSON mode（若 DeepSeek 支持）
2. 单次 LLM `timeout=25s`，整请求 `timeout=55s`
3. Fix 失败直接 502，由用户重试

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
- [ ] `POST /api/v1/quiz/generate` 返回 10 题，含三种题型
- [ ] `POST /api/v1/quiz/report` 返回 Markdown 字符串
- [ ] `/docs` OpenAPI 可浏览、可 Try it out
- [ ] `pytest tests/` 全部通过
- [ ] `.env` 不入 Git（见 `.gitignore`）

---

## 修订记录

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-29 | 初版 API 与数据契约 |
