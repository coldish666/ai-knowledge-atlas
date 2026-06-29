import { useEffect, useMemo, useState } from "react";

import { knowledgeApi } from "../api/knowledge";
import KnowledgeCard from "../components/KnowledgeCard";
import type { KnowledgeLayer, KnowledgeSummary } from "../types/knowledge";

export default function KnowledgeIndex({
  selectedLayer,
  layers,
  onOpen,
}: {
  selectedLayer?: number;
  layers: KnowledgeLayer[];
  onOpen: (slug: string) => void;
}) {
  const [items, setItems] = useState<KnowledgeSummary[]>([]);
  const [tags, setTags] = useState<string[]>([]);
  const [layer, setLayer] = useState<string>(selectedLayer === undefined ? "" : String(selectedLayer));
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [tag, setTag] = useState("");

  useEffect(() => {
    setLayer(selectedLayer === undefined ? "" : String(selectedLayer));
  }, [selectedLayer]);

  useEffect(() => {
    knowledgeApi.tags().then(setTags);
  }, []);

  useEffect(() => {
    knowledgeApi
      .list({
        layer: layer === "" ? undefined : Number(layer),
        category,
        difficulty,
        tag,
      })
      .then((data) => setItems(data.items));
  }, [layer, category, difficulty, tag]);

  const categories = useMemo(() => Array.from(new Set(items.map((item) => item.category))).sort(), [items]);
  const grouped = layers
    .filter((item) => layer === "" || item.layer === Number(layer))
    .map((item) => ({ layer: item, items: items.filter((node) => node.layer === item.layer) }))
    .filter((group) => group.items.length > 0);

  return (
    <section className="page-stack">
      <header className="page-header">
        <div>
          <p className="eyebrow">Knowledge Index</p>
          <h1>知识卡片索引</h1>
          <p>用层级、分类、难度和标签切换视角，快速定位知识点。</p>
        </div>
      </header>

      <section className="filter-panel">
        <select value={layer} onChange={(event) => setLayer(event.target.value)}>
          <option value="">全部层级</option>
          {layers.map((item) => <option key={item.layer} value={item.layer}>L{item.layer} · {item.name}</option>)}
        </select>
        <select value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="">全部分类</option>
          {categories.map((item) => <option key={item} value={item}>{item}</option>)}
        </select>
        <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>
          <option value="">全部难度</option>
          <option value="入门">入门</option>
          <option value="中等">中等</option>
          <option value="挑战">挑战</option>
        </select>
        <select value={tag} onChange={(event) => setTag(event.target.value)}>
          <option value="">全部标签</option>
          {tags.slice(0, 80).map((item) => <option key={item} value={item}>{item}</option>)}
        </select>
      </section>

      {grouped.map(({ layer: layerInfo, items: layerItems }) => (
        <section className="atlas-card index-layer" key={layerInfo.layer}>
          <div className="section-heading">
            <div>
              <p className="eyebrow">Layer {layerInfo.layer}</p>
              <h2>{layerInfo.name}</h2>
            </div>
            <span>{layerItems.length} 个知识点</span>
          </div>
          <div className="card-grid">
            {layerItems.map((node) => <KnowledgeCard key={node.slug} node={node} onOpen={onOpen} />)}
          </div>
        </section>
      ))}
    </section>
  );
}
