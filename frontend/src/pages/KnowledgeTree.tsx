import { useEffect, useMemo, useState, type CSSProperties } from "react";

import type { KnowledgeLayer, KnowledgeSummary } from "../types/knowledge";

type TreeNodeData = {
  id: string;
  title: string;
  kind: "root" | "layer" | "category" | "topic";
  layer?: number;
  slug?: string;
  difficulty?: string;
  summary: string;
  children?: TreeNodeData[];
};

export default function KnowledgeTree({
  layers,
  nodes,
  onOpen,
}: {
  layers: KnowledgeLayer[];
  nodes: KnowledgeSummary[];
  onOpen: (slug: string) => void;
}) {
  const [layerFilter, setLayerFilter] = useState("");
  const [query, setQuery] = useState("");
  const [expanded, setExpanded] = useState<Set<string>>(new Set(["root"]));

  const normalized = query.trim().toLowerCase();

  const tree = useMemo(() => {
    const visibleLayers = layers.filter((layer) => layerFilter === "" || layer.layer === Number(layerFilter));
    const layerChildren = visibleLayers.map((layer) => {
      const layerNodes = nodes.filter((node) => node.layer === layer.layer);
      const categories = Array.from(new Set(layerNodes.map((node) => node.category))).sort();
      return {
        id: `layer-${layer.layer}`,
        title: `L${layer.layer} · ${layer.name}`,
        kind: "layer" as const,
        layer: layer.layer,
        summary: `${layer.count} 个知识点，沿 AI 学习主干继续展开。`,
        children: categories.map((category) => {
          const topics = layerNodes.filter((node) => node.category === category);
          return {
            id: `category-${layer.layer}-${category}`,
            title: category,
            kind: "category" as const,
            layer: layer.layer,
            summary: `${topics.length} 个知识点`,
            children: topics.map((node) => ({
              id: `topic-${node.slug}`,
              title: node.title,
              kind: "topic" as const,
              layer: node.layer,
              slug: node.slug,
              difficulty: node.difficulty,
              summary: node.summary,
            })),
          };
        }),
      };
    });
    return {
      id: "root",
      title: "AI 学习主干",
      kind: "root" as const,
      summary: "从基础到前沿的可折叠知识树。",
      children: layerChildren,
    };
  }, [layerFilter, layers, nodes]);

  useEffect(() => {
    if (!tree.children?.length) return;
    setExpanded((current) => {
      if (current.size > 1) return current;
      const next = new Set(current);
      tree.children?.forEach((layer) => next.add(layer.id));
      tree.children?.slice(0, 3).forEach((layer) => layer.children?.slice(0, 2).forEach((category) => next.add(category.id)));
      return next;
    });
  }, [tree]);

  const visibleTree = useMemo(() => filterTree(tree, normalized), [normalized, tree]);

  function toggle(id: string) {
    setExpanded((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function expandAll() {
    setExpanded(collectExpandableIds(tree));
  }

  function collapseAll() {
    setExpanded(new Set(["root"]));
  }

  return (
    <section className="page-stack">
      <header className="page-header tree-page-header">
        <div>
          <p className="eyebrow">Knowledge Tree</p>
          <h1>AI 知识树</h1>
          <p>按“主干层级 → 分类枝干 → 知识点叶子”展开，和图谱页的复杂依赖关系区分开。</p>
        </div>
        <div className="tree-tools atlas-card">
          <label>
            层级筛选
            <select value={layerFilter} onChange={(event) => setLayerFilter(event.target.value)}>
              <option value="">全部层级</option>
              {layers.map((layer) => (
                <option key={layer.layer} value={layer.layer}>L{layer.layer} · {layer.name}</option>
              ))}
            </select>
          </label>
          <label>
            搜索高亮
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="输入知识点、分类或标签" />
          </label>
          <div className="tree-tool-actions">
            <button onClick={expandAll}>全部展开</button>
            <button className="ghost" onClick={collapseAll}>全部折叠</button>
          </div>
        </div>
      </header>

      <div className="collapsible-tree atlas-card">
        {visibleTree ? (
          <TreeNode node={visibleTree} depth={0} expanded={expanded} query={normalized} onToggle={toggle} onOpen={onOpen} forceOpen={Boolean(normalized)} />
        ) : (
          <p className="muted">没有匹配的知识点。</p>
        )}
      </div>
    </section>
  );
}

function TreeNode({
  node,
  depth,
  expanded,
  query,
  onToggle,
  onOpen,
  forceOpen,
}: {
  node: TreeNodeData;
  depth: number;
  expanded: Set<string>;
  query: string;
  onToggle: (id: string) => void;
  onOpen: (slug: string) => void;
  forceOpen: boolean;
}) {
  const hasChildren = Boolean(node.children?.length);
  const isOpen = forceOpen || expanded.has(node.id);
  const isHighlighted = Boolean(query && nodeMatches(node, query));

  return (
    <div className={`tree-node-wrap depth-${depth} ${isOpen ? "open" : ""}`}>
      <div className={`tree-node-line ${node.kind} layer-${node.layer ?? 0} ${isHighlighted ? "highlighted" : ""}`} style={{ "--depth": depth } as CSSProperties}>
        {hasChildren ? (
          <button className="tree-expander" onClick={() => onToggle(node.id)} aria-expanded={isOpen} aria-label={`${isOpen ? "折叠" : "展开"}${node.title}`}>
            {isOpen ? "−" : "+"}
          </button>
        ) : (
          <span className="tree-expander placeholder" />
        )}
        <button className="tree-node-content" title={node.summary} onClick={() => node.slug ? onOpen(node.slug) : onToggle(node.id)}>
          <strong>{node.title}</strong>
          <span>
            {node.kind === "topic" && node.difficulty ? `${node.difficulty} · ` : ""}
            {node.summary}
          </span>
        </button>
      </div>

      {hasChildren && isOpen && (
        <div className="tree-children">
          {node.children?.map((child) => (
            <TreeNode
              key={child.id}
              node={child}
              depth={depth + 1}
              expanded={expanded}
              query={query}
              onToggle={onToggle}
              onOpen={onOpen}
              forceOpen={forceOpen}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function nodeMatches(node: TreeNodeData, query: string) {
  return `${node.title} ${node.summary} ${node.difficulty || ""}`.toLowerCase().includes(query);
}

function filterTree(node: TreeNodeData, query: string): TreeNodeData | null {
  if (!query) return node;
  const children = node.children?.map((child) => filterTree(child, query)).filter((child): child is TreeNodeData => Boolean(child));
  if (nodeMatches(node, query) || children?.length) {
    return { ...node, children };
  }
  return null;
}

function collectExpandableIds(node: TreeNodeData) {
  const ids = new Set<string>();
  function walk(current: TreeNodeData) {
    if (current.children?.length) {
      ids.add(current.id);
      current.children.forEach(walk);
    }
  }
  walk(node);
  return ids;
}
