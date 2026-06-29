import { useEffect, useState } from "react";

import { knowledgeApi } from "../api/knowledge";
import KnowledgeCard from "../components/KnowledgeCard";
import type { KnowledgeLayer, KnowledgeSummary } from "../types/knowledge";

export default function SearchPage({ query, layers, onOpen }: { query: string; layers: KnowledgeLayer[]; onOpen: (slug: string) => void }) {
  const [results, setResults] = useState<(KnowledgeSummary & { highlights: string[] })[]>([]);
  const [layer, setLayer] = useState("");
  const [difficulty, setDifficulty] = useState("");

  useEffect(() => {
    knowledgeApi.search({ q: query, layer: layer || undefined, difficulty }).then(setResults);
  }, [query, layer, difficulty]);

  return (
    <section className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Search</p>
          <h1>全文搜索：{query || "全部知识"}</h1>
        </div>
        <div className="filters">
          <select value={layer} onChange={(event) => setLayer(event.target.value)}>
            <option value="">全部层级</option>
            {layers.map((item) => <option key={item.layer} value={item.layer}>L{item.layer} · {item.name}</option>)}
          </select>
          <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>
            <option value="">全部难度</option>
            <option value="入门">入门</option>
            <option value="中等">中等</option>
            <option value="挑战">挑战</option>
          </select>
        </div>
      </header>
      <div className="card-grid">
        {results.map((node) => (
          <div className="search-result" key={node.slug}>
            <KnowledgeCard node={node} onOpen={onOpen} />
            {node.highlights?.map((item) => <p key={item} className="highlight">{item.split("**").join("")}</p>)}
          </div>
        ))}
      </div>
    </section>
  );
}
