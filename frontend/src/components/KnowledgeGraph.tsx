import { useMemo } from "react";

import type { GraphData } from "../types/knowledge";

const colors = ["#51d6b4", "#7c8cff", "#ff9f66", "#c591ff", "#65c7ff", "#f0bd62", "#a6df70", "#d19d66", "#89a7ff", "#ff85aa"];

export default function KnowledgeGraph({
  data,
  onOpen,
  zoom = 1,
}: {
  data: GraphData;
  onOpen: (slug: string) => void;
  zoom?: number;
}) {
  const { positioned, height } = useMemo(() => {
    const grouped = new Map<number, typeof data.nodes>();
    data.nodes.slice(0, 180).forEach((node) => {
      grouped.set(node.layer, [...(grouped.get(node.layer) || []), node]);
    });
    const nodes = data.nodes.slice(0, 180).map((node, index) => {
      const layerNodes = grouped.get(node.layer) || [];
      const layerIndex = layerNodes.findIndex((item) => item.id === node.id);
      return {
        ...node,
        x: 92 + node.layer * 132,
        y: 72 + layerIndex * 54 + (index % 2) * 8,
      };
    });
    const maxY = nodes.reduce((value, node) => Math.max(value, node.y), 0);
    return { positioned: nodes, height: Math.max(780, maxY + 96) };
  }, [data.nodes]);

  const byId = new Map(positioned.map((node) => [node.id, node]));

  return (
    <div className="graph-scroll">
      <div className="graph-wrap" style={{ transform: `scale(${zoom})`, transformOrigin: "0 0" }}>
        <svg viewBox={`0 0 1420 ${height}`} role="img" aria-label="AI knowledge graph">
          <defs>
            <marker id="arrow-next" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#79e2c5" />
            </marker>
            <filter id="node-glow" x="-80%" y="-80%" width="260%" height="260%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          {data.edges.map((edge) => {
            const source = byId.get(edge.source);
            const target = byId.get(edge.target);
            if (!source || !target) return null;
            const isRelated = edge.relation_type === "related";
            const isNext = edge.relation_type === "next";
            return (
              <line
                key={`${edge.source}-${edge.target}-${edge.relation_type}`}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke={edge.relation_type === "prerequisite" ? "#ffb86b" : isNext ? "#79e2c5" : "#7b8aa8"}
                strokeWidth={isRelated ? 1.2 : 2.1}
                strokeDasharray={isRelated ? "7 8" : undefined}
                markerEnd={isNext ? "url(#arrow-next)" : undefined}
                opacity={isRelated ? 0.52 : 0.72}
              />
            );
          })}
          {positioned.map((node) => (
            <g key={node.id} onClick={() => onOpen(node.id)} className="graph-node">
              <circle cx={node.x} cy={node.y} r={17} fill={colors[node.layer] || "#51d6b4"} filter="url(#node-glow)" />
              <circle cx={node.x} cy={node.y} r={27} fill="transparent" stroke={colors[node.layer] || "#51d6b4"} strokeOpacity="0.34" />
              <text x={node.x + 25} y={node.y - 2}>{node.title}</text>
              <text className="graph-node-meta" x={node.x + 25} y={node.y + 14}>L{node.layer} · {node.difficulty}</text>
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
}
