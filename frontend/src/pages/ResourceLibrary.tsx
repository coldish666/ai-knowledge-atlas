import { useEffect, useMemo, useState } from "react";

import { knowledgeApi } from "../api/knowledge";
import ResourceCard, { difficultyLabels, languageLabels, resourceTypeLabels } from "../components/ResourceCard";
import type { KnowledgeLayer, KnowledgeResource, KnowledgeSummary } from "../types/knowledge";

const resourceTypes = ["official_doc", "course", "video", "book", "paper", "code", "blog", "chinese_note"];
const authorityLevels = ["S", "A", "B", "C"];
const difficulties = ["beginner", "intermediate", "advanced"];
const languages = ["en", "zh", "other"];

export default function ResourceLibrary({
  layers,
  onOpen,
}: {
  layers: KnowledgeLayer[];
  onOpen: (slug: string) => void;
}) {
  const [items, setItems] = useState<KnowledgeResource[]>([]);
  const [knowledge, setKnowledge] = useState<KnowledgeSummary[]>([]);
  const [layer, setLayer] = useState("");
  const [type, setType] = useState("");
  const [authority, setAuthority] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [language, setLanguage] = useState("");
  const [query, setQuery] = useState("");

  useEffect(() => {
    knowledgeApi.list().then((data) => setKnowledge(data.items));
  }, []);

  useEffect(() => {
    knowledgeApi.resources({
      layer: layer === "" ? undefined : Number(layer),
      type,
      authority_level: authority,
      difficulty,
      language,
      q: query,
    }).then((data) => setItems(data.items));
  }, [authority, difficulty, language, layer, query, type]);

  const knowledgeBySlug = useMemo(() => new Map(knowledge.map((node) => [node.slug, node])), [knowledge]);

  return (
    <section className="page-stack resource-library-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Resource Library</p>
          <h1>权威资源库</h1>
          <p>按知识点索引官方文档、课程、教材、论文、代码和中文辅助资料，只保存链接与简短说明。</p>
        </div>
      </header>

      <section className="resource-library-filters atlas-card">
        <label>
          搜索
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索标题、来源、描述或标签" />
        </label>
        <label>
          知识层级
          <select value={layer} onChange={(event) => setLayer(event.target.value)}>
            <option value="">全部层级</option>
            {layers.map((item) => <option key={item.layer} value={item.layer}>L{item.layer} · {item.name}</option>)}
          </select>
        </label>
        <label>
          资源类型
          <select value={type} onChange={(event) => setType(event.target.value)}>
            <option value="">全部类型</option>
            {resourceTypes.map((item) => <option key={item} value={item}>{resourceTypeLabels[item]}</option>)}
          </select>
        </label>
        <label>
          权威等级
          <select value={authority} onChange={(event) => setAuthority(event.target.value)}>
            <option value="">全部等级</option>
            {authorityLevels.map((item) => <option key={item} value={item}>{item}{item === "S" ? " · 必看" : " 级"}</option>)}
          </select>
        </label>
        <label>
          难度
          <select value={difficulty} onChange={(event) => setDifficulty(event.target.value)}>
            <option value="">全部难度</option>
            {difficulties.map((item) => <option key={item} value={item}>{difficultyLabels[item]}</option>)}
          </select>
        </label>
        <label>
          语言
          <select value={language} onChange={(event) => setLanguage(event.target.value)}>
            <option value="">全部语言</option>
            {languages.map((item) => <option key={item} value={item}>{languageLabels[item]}</option>)}
          </select>
        </label>
      </section>

      <section className="atlas-card resource-library-results">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Results</p>
            <h2>{items.length} 条资源</h2>
          </div>
          <button className="ghost" onClick={() => {
            setLayer("");
            setType("");
            setAuthority("");
            setDifficulty("");
            setLanguage("");
            setQuery("");
          }}>
            清空筛选
          </button>
        </div>
        <div className="resource-grid library-grid">
          {items.map((resource) => {
            const node = knowledgeBySlug.get(resource.knowledge_slug);
            return (
              <div className="resource-library-item" key={resource.id}>
                <ResourceCard resource={resource} onOpenKnowledge={onOpen} />
                {node && (
                  <button className="knowledge-backlink" onClick={() => onOpen(node.slug)}>
                    关联知识点：L{node.layer} · {node.title}
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </section>
  );
}
