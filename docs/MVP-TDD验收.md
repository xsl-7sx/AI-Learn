# MVP TDD 验收报告

> 对照 [MVP开发实施指南.md](./MVP开发实施指南.md) §一、§三 闸门 G0–G4。  
> 自动化测试：**后端 35 项 + 前端 17 项**，执行时间约 10s（Mock LLM）。

## 如何运行

```bash
# 后端（需在 backend/.venv 内）
cd backend
.venv\Scripts\activate          # Windows
pytest tests/ -v

# 前端
cd uniapp
npm test
```

---

## 验收矩阵

| 闸门 | 验收项 | 自动化 | 结果 |
| ---- | ------ | ------ | ---- |
| **G0** | 四页面 `pages.json` 注册 | `test_repo_has_mvp_frontend_pages` / `mvp_static.test.ts` | ✅ |
| **G0** | index→loading→quiz→result 可跳转 | 源码存在；**真机路径需人工点验** | ⚠️ 人工 |
| **G1** | `/health` | `test_g1_health_endpoint` | ✅ |
| **G1** | `POST /generate` → 202 + job_id | `test_g1_generate_returns_job_202` | ✅ |
| **G1** | 10 题 + 三题型 | `test_g1_quiz_has_ten_questions_and_three_types` | ✅ |
| **G1** | `POST /report` 结构化 JSON | `test_g1_report_returns_structured_json` | ✅ |
| **G2** | 单选/多选/判断本地判分 | `scoring.test.ts` | ✅ |
| **G2** | 多选集合相等 | `scoring.test.ts` | ✅ |
| **G2** | 判断题 answer 为下标 | `scoring.test.ts` | ✅ |
| **G2** | 多关卡存档 / 未完成列表 | `storage.test.ts` | ✅ |
| **G2** | 退出 Sheet + 震动 + 音效代码 | `mvp_static.test.ts`（静态） | ✅ |
| **G2** | Mock 10 题走完 UI | **需微信开发者工具** | ⚠️ 人工 |
| **G3** | 流式首题就绪 | `test_g3_streaming_first_question_ready_before_complete` | ✅ |
| **G3** | 真实 AI 出题 | **需配置 DEEPSEEK_API_KEY + MOCK_LLM=false** | ⚠️ 人工 |
| **G4** | 完整闭环 generate→report | `test_g4_full_closed_loop_*` / `test_full_quiz_flow` | ✅ |
| **G4** | 结构化复盘 JSON 解析 | `structuredReport.test.ts` | ✅ |
| **G4** | 知识点面板 + AI 报告分卡 | `mvp_static.test.ts` | ✅ |
| **G4** | 再来一局 `clearQuizSession` | `mvp_static.test.ts` | ✅ |
| **G4** | 分享按钮置灰 | 源码人工确认 | ⚠️ 人工 |
| **—** | 真机 `VITE_API_BASE_URL` 联调 | **需同一 Wi-Fi 真机** | ⚠️ 人工 |
| **—** | 微信体验版内测 | **需上传体验版** | ⚠️ 人工 |

---

## 结论

### 已通过（自动化）

- **后端 MVP 契约**：异步出题、流式增量、10 题三题型、结构化 JSON 复盘、Job 持久化、Schema 校验。
- **前端核心逻辑**：判分、存档、复盘 JSON 解析、四页与结算页组件结构。

### 未纳入自动化（需人工 smoke test）

1. 微信开发者工具内 **完整 UI 交互**（滚动、Sheet、音效播放）
2. **真机联调**（局域网 IP、域名白名单）
3. **真实 LLM** 出题质量与偶发 5 题失败（流式解析边界）
4. 体验版发布与内测

### MVP 是否「全部实现」？

| 维度 | 判定 |
| ---- | ---- |
| 代码与 API 契约 | **是** — 52 项自动化测试全部通过 |
| 文档定义的成功标准（含真机/体验版） | **部分** — 尚需 1 次真机 smoke + 可选真实 LLM 抽测 |

建议最小人工验收清单：

1. `npm run dev:mp-weixin` → 导入开发者工具 → 输入 topic → 答完 10 题 → 结算页展开「知识点」与「AI 复盘」
2. 真机同一 Wi-Fi 重复上述流程
3. （可选）`MOCK_LLM=false` 下抽测 2–3 个 topic，确认稳定出 10 题

---

## 测试文件索引

| 路径 | 覆盖 |
| ---- | ---- |
| `backend/tests/test_mvp_acceptance.py` | G1/G3/G4 闸门 |
| `backend/tests/test_api.py` | API 冒烟 |
| `backend/tests/test_integration.py` | 端到端 |
| `uniapp/tests/scoring.test.ts` | G2 判分 |
| `uniapp/tests/storage.test.ts` | G2 存档 |
| `uniapp/tests/structuredReport.test.ts` | G4 复盘解析 |
| `uniapp/tests/mvp_static.test.ts` | G0/G2/G4 静态结构 |

---

| 版本 | 日期 | 说明 |
| ---- | ---- | ---- |
| v1.0.0 | 2026-05-30 | 初版：52 项自动化 + 人工项清单 |
