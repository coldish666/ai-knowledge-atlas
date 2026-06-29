import { useMemo, useState } from "react";

import type { PageKey } from "../components/Sidebar";
import type { KnowledgeLayer, KnowledgeSummary } from "../types/knowledge";

const trunk = [
  { id: "math", label: "数学与计算基础", slug: "gradient-descent", layers: [0], branches: ["向量", "矩阵", "概率分布", "交叉熵", "梯度下降", "凸优化"] },
  { id: "python", label: "Python与数据处理", slug: "numpy-array", layers: [1], branches: ["NumPy 数组", "Pandas DataFrame", "数据清洗", "数据泄漏", "可视化"] },
  { id: "ml", label: "经典机器学习", slug: "linear-regression", layers: [2], branches: ["线性回归", "逻辑回归", "KNN", "决策树", "SVM", "KMeans"] },
  { id: "deep", label: "深度学习", slug: "backpropagation", layers: [3], branches: ["多层感知机", "反向传播", "激活函数", "优化器", "BatchNorm", "Dropout"] },
  { id: "transformer", label: "Transformer", slug: "self-attention", layers: [4], branches: ["Attention", "Self-Attention", "Multi-Head Attention", "Position Encoding", "Transformer Encoder"] },
  { id: "llm", label: "大模型", slug: "language-model", layers: [5], branches: ["Tokenizer", "预训练", "指令微调", "LoRA", "RLHF", "评测"] },
  { id: "rag", label: "RAG", slug: "retrieval", layers: [6], branches: ["Embedding（RAG）", "向量数据库", "文档切分", "检索", "重排序", "引用来源"] },
  { id: "agent", label: "Agent", slug: "agent-architecture", layers: [7], branches: ["工具调用", "规划", "记忆", "工作流", "Agentic RAG"] },
  { id: "engineering-frontier", label: "工程化与前沿", slug: "model-serving", layers: [8, 9], branches: ["FastAPI", "Docker", "量化", "AI for Science", "多模态大模型", "具身智能", "AI 安全与对齐"] },
] as const;

const featureCards = [
  ["知识索引", "按层级、分类、难度和标签浏览完整知识库。", "index"],
  ["权威资源库", "按知识点索引官方文档、课程、论文、代码和中文资料。", "resources"],
  ["知识图谱", "查看 prerequisite、next、related 三类复杂依赖关系。", "graph"],
  ["交互讲解", "用导师视角解释概念、比较知识点并生成自测。", "tutor"],
  ["RAG 资料问答", "上传 md/txt 资料，与内置知识一起检索问答。", "rag"],
  ["代码示例库", "每个知识点都带最小 Python / PyTorch 示例。", "index"],
] as const;

export default function Home({
  layers,
  featured,
  onOpen,
  onLayer,
  onNavigate,
  onSearch,
}: {
  layers: KnowledgeLayer[];
  featured: KnowledgeSummary[];
  onOpen: (slug: string) => void;
  onLayer: (layer: number) => void;
  onNavigate: (page: PageKey) => void;
  onSearch: (query: string) => void;
}) {
  const [expanded, setExpanded] = useState<Set<string>>(() => new Set(trunk.map((item) => item.id)));
  const byTitle = useMemo(() => new Map(featured.map((item) => [item.title, item])), [featured]);

  function toggle(id: string) {
    setExpanded((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function stageBranches(stage: (typeof trunk)[number]) {
    const stageLayers = stage.layers as readonly number[];
    const chosen = stage.branches
      .map((title) => byTitle.get(title))
      .filter((item): item is KnowledgeSummary => Boolean(item));
    const fallback = featured.filter((item) => stageLayers.includes(item.layer)).slice(0, 8);
    const merged = [...chosen, ...fallback];
    return merged.filter((item, index) => merged.findIndex((candidate) => candidate.slug === item.slug) === index).slice(0, 8);
  }

  return (
    <section className="home-atlas">
      <header className="atlas-hero">
        <div>
          <p className="eyebrow">Interactive AI Knowledge Tree</p>
          <h1>AI Knowledge Atlas</h1>
          <p>从数学基础到大模型、Agent 与 AI for Science 的交互式知识地图。</p>
        </div>
        <form
          className="hero-search"
          onSubmit={(event) => {
            event.preventDefault();
            const value = new FormData(event.currentTarget).get("q")?.toString() || "";
            onSearch(value);
          }}
        >
          <input name="q" placeholder="搜索：反向传播、Transformer、RAG、AI for Science..." />
          <button type="submit">搜索知识</button>
        </form>
        <div className="hero-actions">
          <button onClick={() => onLayer(0)}>从主干开始</button>
          <button onClick={() => onNavigate("tree")}>查看知识树</button>
          <button onClick={() => onNavigate("graph")}>查看知识图谱</button>
          <button onClick={() => onNavigate("rag")}>进入 RAG 问答</button>
        </div>
      </header>

      <section className="knowledge-tree-stage home-tree-stage">
        <div className="tree-glow" />
        <div className="tree-title">
          <p className="eyebrow">Vertical AI Learning Trunk</p>
          <h2>AI 学习主干知识树</h2>
          <p>主干从上到下推进，枝干向左右展开。展开阶段后点击任意叶子进入知识详情。</p>
        </div>

        <div className="learning-trunk" aria-label="AI learning trunk tree">
          {trunk.map((stage, index) => {
            const isOpen = expanded.has(stage.id);
            const branches = stageBranches(stage);
            const left = branches.filter((_, branchIndex) => branchIndex % 2 === 0);
            const right = branches.filter((_, branchIndex) => branchIndex % 2 === 1);
            const stageLayers = stage.layers as readonly number[];
            const total = layers.filter((layer) => stageLayers.includes(layer.layer)).reduce((sum, layer) => sum + layer.count, 0);

            return (
              <div className={`learning-stage ${isOpen ? "expanded" : ""}`} key={stage.id}>
                <div className="stage-branches left">
                  {isOpen && left.map((branch) => <BranchNode key={branch.slug} node={branch} onOpen={onOpen} />)}
                </div>

                <div className="stage-core">
                  <button className="stage-toggle" onClick={() => toggle(stage.id)} aria-expanded={isOpen} aria-label={`${isOpen ? "折叠" : "展开"}${stage.label}`}>
                    {isOpen ? "−" : "+"}
                  </button>
                  <button className="stage-node" onClick={() => onOpen(stage.slug)}>
                    <span>L{stage.layers.join(" / L")}</span>
                    <strong>{stage.label}</strong>
                    <small>{total} 个知识点</small>
                  </button>
                  {index < trunk.length - 1 && <span className="stage-arrow" aria-hidden="true" />}
                </div>

                <div className="stage-branches right">
                  {isOpen && right.map((branch) => <BranchNode key={branch.slug} node={branch} onOpen={onOpen} />)}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="feature-grid">
        {featureCards.map(([title, text, page]) => (
          <button key={title} className="feature-card" onClick={() => onNavigate(page)}>
            <span>{title}</span>
            <p>{text}</p>
          </button>
        ))}
      </section>
    </section>
  );
}

function BranchNode({ node, onOpen }: { node: KnowledgeSummary; onOpen: (slug: string) => void }) {
  return (
    <button className={`home-branch-node layer-${node.layer}`} title={node.summary} onClick={() => onOpen(node.slug)}>
      <strong>{node.title}</strong>
      <span>{node.difficulty} · {node.category}</span>
    </button>
  );
}
