import type { KnowledgeResource } from "../types/knowledge";

export const resourceTypeLabels: Record<string, string> = {
  official_doc: "官方文档",
  course: "课程",
  video: "视频课程",
  book: "教材章节",
  paper: "论文",
  code: "代码仓库",
  blog: "文章",
  chinese_note: "中文辅助",
};

export const difficultyLabels: Record<string, string> = {
  beginner: "入门",
  intermediate: "进阶",
  advanced: "高级",
};

export const languageLabels: Record<string, string> = {
  en: "English",
  zh: "中文",
  other: "Other",
};

export default function ResourceCard({
  resource,
  onOpenKnowledge,
  compact = false,
}: {
  resource: KnowledgeResource;
  onOpenKnowledge?: (slug: string) => void;
  compact?: boolean;
}) {
  return (
    <article className={`resource-card type-${resource.resource_type} ${compact ? "compact" : ""}`}>
      <div className="resource-card-head">
        <div>
          <p className="resource-source">{resource.source}</p>
          <h3>{resource.title}</h3>
        </div>
        <span className={`authority-pill level-${resource.authority_level}`}>{resource.authority_level === "S" ? "S · 必看" : `${resource.authority_level} 级`}</span>
      </div>
      <div className="resource-meta">
        <span className={`type-pill type-${resource.resource_type}`}>{resourceTypeLabels[resource.resource_type] || resource.resource_type}</span>
        <span>{difficultyLabels[resource.difficulty] || resource.difficulty}</span>
        <span>{languageLabels[resource.language] || resource.language}</span>
        <span>{resource.estimated_time}</span>
      </div>
      {!compact && <p>{resource.description}</p>}
      <p className="resource-reason">{resource.why_recommended}</p>
      <div className="resource-actions">
        <a href={resource.url} target="_blank" rel="noreferrer">点击访问</a>
        {onOpenKnowledge && (
          <button onClick={() => onOpenKnowledge(resource.knowledge_slug)}>关联知识点</button>
        )}
      </div>
    </article>
  );
}
