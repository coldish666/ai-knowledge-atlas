import type { KnowledgeSummary } from "../types/knowledge";

export default function RelatedPanel({
  prerequisites,
  next,
  related,
  sameLayer,
  onOpen,
}: {
  prerequisites: KnowledgeSummary[];
  next: KnowledgeSummary[];
  related: KnowledgeSummary[];
  sameLayer: KnowledgeSummary[];
  onOpen: (slug: string) => void;
}) {
  return (
    <aside className="related-panel">
      <LinkGroup title="前置知识" items={prerequisites} onOpen={onOpen} />
      <LinkGroup title="后续知识" items={next} onOpen={onOpen} />
      <LinkGroup title="相关知识" items={related} onOpen={onOpen} />
      <LinkGroup title="同层知识" items={sameLayer} onOpen={onOpen} />
    </aside>
  );
}

function LinkGroup({ title, items, onOpen }: { title: string; items: KnowledgeSummary[]; onOpen: (slug: string) => void }) {
  return (
    <section>
      <h3>{title}</h3>
      {items.length === 0 && <p className="muted">暂无</p>}
      {items.map((item) => (
        <button key={item.slug} onClick={() => onOpen(item.slug)}>
          <strong>{item.title}</strong>
          <span>{item.summary}</span>
        </button>
      ))}
    </section>
  );
}
