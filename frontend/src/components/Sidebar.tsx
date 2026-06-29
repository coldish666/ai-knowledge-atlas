import type { KnowledgeLayer } from "../types/knowledge";

export type PageKey = "home" | "tree" | "index" | "resources" | "detail" | "graph" | "search" | "rag" | "tutor" | "settings";

export default function Sidebar({
  page,
  layers,
  onNavigate,
  onLayer,
}: {
  page: PageKey;
  layers: KnowledgeLayer[];
  onNavigate: (page: PageKey) => void;
  onLayer: (layer: number) => void;
}) {
  const nav = [
    ["home", "首页地图"],
    ["tree", "AI 知识树"],
    ["index", "知识索引"],
    ["resources", "权威资源库"],
    ["graph", "知识图谱"],
    ["search", "全文搜索"],
    ["rag", "RAG 问答"],
    ["tutor", "AI 导师"],
    ["settings", "设置"],
  ] as const;

  return (
    <aside className="sidebar">
      <div className="brand">
        <strong>AI Knowledge Atlas</strong>
        <span>AI 学习知识索引</span>
      </div>
      <nav>
        {nav.map(([key, label]) => (
          <button key={key} className={page === key ? "active" : ""} onClick={() => onNavigate(key)}>
            {label}
          </button>
        ))}
      </nav>
      <div className="sidebar-section">
        <span>知识层级</span>
        {layers.map((layer) => (
          <button key={layer.layer} onClick={() => onLayer(layer.layer)}>
            L{layer.layer} · {layer.name} <b>{layer.count}</b>
          </button>
        ))}
      </div>
    </aside>
  );
}
