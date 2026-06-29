import { useEffect, useMemo, useState } from "react";

import { knowledgeApi } from "../api/knowledge";
import KnowledgeGraph from "../components/KnowledgeGraph";
import type { GraphData, KnowledgeLayer } from "../types/knowledge";

export default function GraphView({
  layers,
  onOpen,
}: {
  layers: KnowledgeLayer[];
  onOpen: (slug: string) => void;
}) {
  const [data, setData] = useState<GraphData>({ nodes: [], edges: [] });
  const [layer, setLayer] = useState("");
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [focusSlug, setFocusSlug] = useState("");
  const [zoom, setZoom] = useState(1);
  const [mode, setMode] = useState("全局图谱");

  useEffect(() => {
    knowledgeApi.graph().then(setData);
  }, []);

  const categories = useMemo(() => Array.from(new Set(data.nodes.map((node) => node.category))).sort(), [data.nodes]);
  const difficulties = useMemo(() => Array.from(new Set(data.nodes.map((node) => node.difficulty))).sort(), [data.nodes]);

  const filtered = useMemo(() => {
    const nodes = data.nodes.filter((node) => {
      const byLayer = !layer || node.layer === Number(layer);
      const byCategory = !category || node.category === category;
      const byDifficulty = !difficulty || node.difficulty === difficulty;
      return byLayer && byCategory && byDifficulty;
    });
    const visible = new Set(nodes.map((node) => node.id));
    return {
      nodes,
      edges: data.edges.filter((edge) => visible.has(edge.source) && visible.has(edge.target)),
    };
  }, [category, data, difficulty, layer]);

  function resetGraph() {
    setLayer("");
    setCategory("");
    setDifficulty("");
    setFocusSlug("");
    setZoom(1);
    setMode("全局图谱");
    knowledgeApi.graph().then(setData);
  }

  function loadNeighborhood() {
    const slug = focusSlug.trim();
    if (!slug) return;
    knowledgeApi.neighborhood(slug).then((nextData) => {
      setData(nextData);
      setMode(`局部邻域：${slug}`);
      setLayer("");
      setCategory("");
      setDifficulty("");
      setZoom(1.08);
    });
  }

  return (
    <section className="page-stack graph-page">
      <header className="page-header graph-header">
        <div>
          <p className="eyebrow">Knowledge Graph</p>
          <h1>AI 知识图谱</h1>
          <p>用节点和关系线查看前置、后续与相关知识。点击节点进入交互教材。</p>
        </div>
        <div className="graph-mode">{mode}</div>
      </header>

      <div className="graph-controls atlas-card">
        <label>
          层级
          <select value={layer} onChange={(event) => setLayer(event.target.value)}>
            <option value="">全部层级</option>
            {layers.map((item) => (
              <option key={item.layer} value={item.layer}>
                L{item.layer} · {item.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          分类
          <select value={category} onChange={(event) => setCategory(event.target.value)}>
            <option value="">全部分类</option>
            {categories.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
        </label>
        <label>
          难度
          <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>
            <option value="">全部难度</option>
            {difficulties.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
        </label>
        <label className="focus-field">
          局部邻域
          <input
            value={focusSlug}
            list="graph-node-slugs"
            onChange={(event) => setFocusSlug(event.target.value)}
            placeholder="输入知识点 slug，如 self-attention"
          />
          <datalist id="graph-node-slugs">
            {data.nodes.map((node) => (
              <option key={node.id} value={node.id}>{node.title}</option>
            ))}
          </datalist>
        </label>
        <button onClick={loadNeighborhood}>查看邻域</button>
        <button className="ghost" onClick={resetGraph}>重置视图</button>
      </div>

      <div className="graph-workbench">
        <div className="graph-panel atlas-card">
          <div className="graph-toolbar">
            <div className="graph-legend">
              <span><i className="edge prerequisite" /> prerequisite</span>
              <span><i className="edge next" /> next</span>
              <span><i className="edge related" /> related</span>
            </div>
            <div className="zoom-controls">
              <button onClick={() => setZoom((value) => Math.max(0.62, Number((value - 0.12).toFixed(2))))}>-</button>
              <span>{Math.round(zoom * 100)}%</span>
              <button onClick={() => setZoom((value) => Math.min(1.55, Number((value + 0.12).toFixed(2))))}>+</button>
            </div>
          </div>
          <KnowledgeGraph data={filtered} onOpen={onOpen} zoom={zoom} />
        </div>

        <aside className="graph-side atlas-card">
          <h3>图谱概览</h3>
          <p className="muted">{filtered.nodes.length} 个节点 · {filtered.edges.length} 条关系</p>
          <svg className="graph-minimap" viewBox="0 0 220 150" role="img" aria-label="graph minimap">
            {filtered.nodes.slice(0, 120).map((node, index) => (
              <circle
                key={node.id}
                cx={16 + node.layer * 20}
                cy={16 + (index % 18) * 7}
                r="2.8"
                className={`mini-layer-${node.layer}`}
              />
            ))}
          </svg>
          <div className="graph-tip">
            <strong>阅读建议</strong>
            <p>先沿 next 箭头看主干，再用 prerequisite 回查基础，最后打开 related 扩展到同类方法。</p>
          </div>
        </aside>
      </div>
    </section>
  );
}
