import type { KnowledgeSummary } from "../types/knowledge";

export default function KnowledgeCard({ node, onOpen }: { node: KnowledgeSummary; onOpen: (slug: string) => void }) {
  return (
    <button className="knowledge-card" onClick={() => onOpen(node.slug)}>
      <span>L{node.layer} · {node.category}</span>
      <strong>{node.title}</strong>
      <p>{node.summary}</p>
      <div className="card-meta">
        <em>{node.difficulty}</em>
        <em>{node.tags.slice(0, 3).join(" / ")}</em>
      </div>
      <div className="relation-counts">
        <i>前置 {node.prerequisites?.length || 0}</i>
        <i>后续 {node.next_topics?.length || 0}</i>
        <i>相关 {node.related_topics?.length || 0}</i>
      </div>
      <div className="card-reveal">
        <b>知识连接</b>
        <small>前置：{node.prerequisites?.slice(0, 3).join("、") || "暂无"}</small>
        <small>后续：{node.next_topics?.slice(0, 3).join("、") || "暂无"}</small>
        <strong>查看详情 →</strong>
      </div>
    </button>
  );
}
