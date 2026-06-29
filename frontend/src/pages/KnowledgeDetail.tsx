import { useEffect, useMemo, useState } from "react";

import { knowledgeApi } from "../api/knowledge";
import CodeBlock from "../components/CodeBlock";
import FormulaBlock from "../components/FormulaBlock";
import ResourceCard, { resourceTypeLabels } from "../components/ResourceCard";
import type { KnowledgeNode, KnowledgeResource, KnowledgeSummary } from "../types/knowledge";

const resourceGroups = ["official_doc", "video", "course", "book", "paper", "code", "chinese_note", "blog"];
const resourceFilters = [
  ["all", "全部资源"],
  ["official", "只看官方"],
  ["video", "只看视频"],
  ["zh", "只看中文"],
  ["beginner", "只看入门"],
  ["must", "只看必看"],
] as const;

export default function KnowledgeDetail({
  slug,
  onOpen,
  onTree,
}: {
  slug: string;
  onOpen: (slug: string) => void;
  onTree: () => void;
}) {
  const [node, setNode] = useState<KnowledgeNode | null>(null);
  const [resources, setResources] = useState<KnowledgeResource[]>([]);
  const [prerequisites, setPrerequisites] = useState<KnowledgeSummary[]>([]);
  const [next, setNext] = useState<KnowledgeSummary[]>([]);
  const [related, setRelated] = useState<KnowledgeSummary[]>([]);
  const [sameLayer, setSameLayer] = useState<KnowledgeSummary[]>([]);
  const [openChecks, setOpenChecks] = useState(true);
  const [resourceFilter, setResourceFilter] = useState<(typeof resourceFilters)[number][0]>("all");
  const [showAllResources, setShowAllResources] = useState(false);

  useEffect(() => {
    knowledgeApi.detail(slug).then(setNode);
    knowledgeApi.resourcesForSlug(slug).then(setResources);
    knowledgeApi.related(slug, "prerequisites").then((data: any) => setPrerequisites(data.items || data));
    knowledgeApi.related(slug, "next").then((data: any) => setNext(data.items || data));
    knowledgeApi.related(slug, "related").then((data: any) => setRelated(data.items || data));
    knowledgeApi.related(slug, "same-layer").then((data: any) => setSameLayer(data.items || data));
    setOpenChecks(true);
    setResourceFilter("all");
    setShowAllResources(false);
  }, [slug]);

  const directory = useMemo(() => {
    if (!node) return [];
    const unique = [node, ...sameLayer].filter((item, index, all) => all.findIndex((candidate) => candidate.slug === item.slug) === index);
    const categories = Array.from(new Set(unique.map((item) => item.category))).sort();
    return categories.map((category) => ({
      category,
      items: unique.filter((item) => item.category === category),
    }));
  }, [node, sameLayer]);

  const filteredResources = resources.filter((resource) => {
    if (resourceFilter === "official") return resource.resource_type === "official_doc";
    if (resourceFilter === "video") return resource.resource_type === "video" || resource.resource_type === "course";
    if (resourceFilter === "zh") return resource.language === "zh" || resource.resource_type === "chinese_note";
    if (resourceFilter === "beginner") return resource.difficulty === "beginner";
    if (resourceFilter === "must") return resource.authority_level === "S";
    return true;
  });
  const visibleResources = showAllResources ? filteredResources : filteredResources.slice(0, 6);
  const groupedResources = resourceGroups
    .map((type) => ({ type, items: visibleResources.filter((resource) => resource.resource_type === type) }))
    .filter((group) => group.items.length > 0);

  if (!node) return <section className="panel">加载知识点...</section>;

  return (
    <section className="detail-three-column">
      <aside className="detail-left">
        <button className="tree-return" onClick={onTree}>返回 AI 知识树</button>
        <div className="side-card detail-tree-card">
          <p className="eyebrow">Tree Position</p>
          <h3>当前树状目录</h3>
          <div className="detail-tree">
            <div className="detail-tree-root">AI 学习主干</div>
            <div className={`detail-tree-layer layer-${node.layer}`}>
              <strong>L{node.layer}</strong>
              <span>{node.category}</span>
            </div>
            {directory.map((group) => (
              <div className="detail-tree-category" key={group.category}>
                <button className={group.category === node.category ? "active" : ""}>
                  {group.category}
                  <span>{group.items.length}</span>
                </button>
                <div className="detail-tree-topics">
                  {group.items.map((item) => (
                    <button key={item.slug} className={item.slug === node.slug ? "current" : ""} title={item.summary} onClick={() => onOpen(item.slug)}>
                      <strong>{item.title}</strong>
                      <span>{item.difficulty}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </aside>

      <article className="detail-main">
        <header className="detail-hero atlas-card">
          <p className="eyebrow">L{node.layer} · {node.category} · {node.difficulty}</p>
          <h1>{node.title}</h1>
          <p>{node.summary}</p>
          <div className="tag-row">{node.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>
        </header>

        <Section title="概念定义" text={node.definition} />
        <Section title="直觉理解" text={node.intuition} />
        <Section title="为什么重要" text={node.why_it_matters} />
        <Section title="数学形式" text={node.math_form} />
        <section className="atlas-card">
          <h2>核心公式</h2>
          <FormulaBlock formulas={node.formulas} />
        </section>
        <section className="atlas-card">
          <h2>代码示例</h2>
          <CodeBlock code={node.code_example} />
        </section>
        <ListSection title="典型应用" items={node.applications} />
        <ListSection title="常见误区" items={node.misconceptions} />
        <section className="atlas-card">
          <button className="collapse-button" onClick={() => setOpenChecks(!openChecks)}>
            自测问题 {openChecks ? "收起" : "展开"}
          </button>
          {openChecks && <ul className="check-list">{node.self_check_questions.map((item) => <li key={item}>{item}</li>)}</ul>}
        </section>

        <section className="atlas-card resource-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Resource Index</p>
              <h2>推荐学习资源</h2>
            </div>
            <span>{resources.length} 条外部资源</span>
          </div>
          <div className="resource-filter-row">
            {resourceFilters.map(([key, label]) => (
              <button key={key} className={resourceFilter === key ? "active" : ""} onClick={() => setResourceFilter(key)}>
                {label}
              </button>
            ))}
          </div>
          {groupedResources.length === 0 && <p className="muted">当前筛选条件下暂无资源。</p>}
          {groupedResources.map((group) => (
            <div className="resource-group" key={group.type}>
              <h3>{resourceTypeLabels[group.type] || group.type}</h3>
              <div className="resource-grid">
                {group.items.map((resource) => <ResourceCard key={resource.id} resource={resource} compact />)}
              </div>
            </div>
          ))}
          {filteredResources.length > 6 && (
            <button className="resource-more" onClick={() => setShowAllResources(!showAllResources)}>
              {showAllResources ? "收起资源" : `展开更多（${filteredResources.length - 6}）`}
            </button>
          )}
        </section>
      </article>

      <aside className="detail-right">
        <RelationGroup title="前置知识" items={prerequisites} onOpen={onOpen} />
        <RelationGroup title="后续知识" items={next} onOpen={onOpen} />
        <RelationGroup title="相关知识" items={related} onOpen={onOpen} />
        <div className="side-card graph-position">
          <p className="eyebrow">Graph Position</p>
          <h3>图谱中的关系位置</h3>
          <div className="mini-node">
            <i>{prerequisites.length}</i>
            <strong>{node.title}</strong>
            <i>{next.length + related.length}</i>
          </div>
          <p>左侧数字表示前置入口，右侧数字表示后续与相关出口。</p>
        </div>
        <div className="side-card">
          <h3>资源优先级</h3>
          <ul>
            <li>S 级资源优先展示。</li>
            <li>官方文档、课程和论文优先。</li>
            <li>入门资料排在高级资料之前。</li>
          </ul>
        </div>
      </aside>
    </section>
  );
}

function Section({ title, text }: { title: string; text: string }) {
  return <section className="atlas-card"><h2>{title}</h2><p>{text}</p></section>;
}

function ListSection({ title, items }: { title: string; items: string[] }) {
  return <section className="atlas-card"><h2>{title}</h2><ul>{items.map((item) => <li key={item}>{item}</li>)}</ul></section>;
}

function RelationGroup({ title, items, onOpen }: { title: string; items: KnowledgeSummary[]; onOpen: (slug: string) => void }) {
  return (
    <div className="side-card">
      <h3>{title}</h3>
      {items.length === 0 && <p className="muted">暂无</p>}
      {items.map((item) => (
        <button key={item.slug} className="relation-link" onClick={() => onOpen(item.slug)}>
          <strong>{item.title}</strong>
          <span>{item.summary}</span>
        </button>
      ))}
    </div>
  );
}
