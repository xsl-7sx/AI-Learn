import type { IconName } from './icons'

export interface TopicItem {
  title: string
  heat: string
  tone: 'orange' | 'blue' | 'mint' | 'lavender'
  /** 仅用于 UI 展示 */
  desc?: string
  /** Lucide 图标名 */
  icon?: IconName
}

export const TOPIC_BATCHES: TopicItem[][] = [
  [
    { title: 'RAG 基础概念', heat: '92%', tone: 'orange', desc: '检索增强生成核心知识速通', icon: 'layers' },
    { title: '提示词工程', heat: '88%', tone: 'blue', desc: '让 AI 听懂你的话', icon: 'lightbulb' },
    { title: 'TCP 三次握手', heat: '85%', tone: 'mint', desc: '网络连接建立全过程', icon: 'link' },
    { title: 'Transformer', heat: '81%', tone: 'lavender', desc: '注意力机制与编码解码', icon: 'zap' },
    { title: 'Embedding 入门', heat: '78%', tone: 'blue', desc: '文本向量化入门', icon: 'puzzle' },
  ],
  [
    { title: '向量数据库', heat: '90%', tone: 'blue', desc: '相似度检索与索引', icon: 'database' },
    { title: 'LoRA 微调入门', heat: '86%', tone: 'lavender', desc: '轻量模型适配方法', icon: 'target' },
    { title: 'Redis 缓存策略', heat: '83%', tone: 'orange', desc: '高性能缓存策略', icon: 'settings' },
    { title: 'Agent 工具调用', heat: '79%', tone: 'mint', desc: '函数调用与任务编排', icon: 'bot' },
    { title: 'MCP 协议速览', heat: '76%', tone: 'lavender', desc: '模型上下文协议速览', icon: 'radio' },
  ],
  [
    { title: 'Kotlin 协程', heat: '87%', tone: 'mint', desc: '异步并发编程基础', icon: 'refresh-cw' },
    { title: '设计模式速记', heat: '84%', tone: 'blue', desc: '常见模式速记与应用', icon: 'blocks' },
    { title: 'Git 分支策略', heat: '82%', tone: 'orange', desc: '团队协作分支策略', icon: 'git-branch' },
    { title: '注意力机制', heat: '80%', tone: 'lavender', desc: 'Self-Attention 原理', icon: 'eye' },
    { title: 'Docker 网络', heat: '77%', tone: 'orange', desc: '容器网络模式详解', icon: 'container' },
  ],
]

