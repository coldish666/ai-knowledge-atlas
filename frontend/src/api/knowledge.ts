import { request } from "./client";
import type { GraphData, KnowledgeLayer, KnowledgeList, KnowledgeNode, KnowledgeResource, KnowledgeSummary, ResourceList } from "../types/knowledge";

export const knowledgeApi = {
  list: (params: Record<string, string | number | undefined> = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== "") query.set(key, String(value));
    });
    return request<KnowledgeList>(`/api/knowledge${query.toString() ? `?${query}` : ""}`);
  },
  detail: (slug: string) => request<KnowledgeNode>(`/api/knowledge/${slug}`),
  layers: () => request<KnowledgeLayer[]>("/api/knowledge/layers"),
  tags: () => request<string[]>("/api/knowledge/tags"),
  related: (slug: string, type: "related" | "prerequisites" | "next" | "same-layer") =>
    request<{ items: KnowledgeSummary[] } | KnowledgeSummary[]>(`/api/knowledge/${slug}/${type}`),
  search: (params: Record<string, string | number | undefined>) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== "") query.set(key, String(value));
    });
    return request<(KnowledgeSummary & { highlights: string[] })[]>(`/api/search?${query}`);
  },
  graph: (layer?: number) => request<GraphData>(`/api/graph${layer !== undefined ? `?layer=${layer}` : ""}`),
  neighborhood: (slug: string) => request<GraphData>(`/api/graph/${slug}/neighborhood`),
  resourcesForSlug: (slug: string) => request<KnowledgeResource[]>(`/api/knowledge/${slug}/resources`),
  recommendedResources: (slug: string) => request<KnowledgeResource[]>(`/api/resources/recommended?slug=${encodeURIComponent(slug)}`),
  resources: (params: Record<string, string | number | undefined> = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== "") query.set(key, String(value));
    });
    return request<ResourceList>(`/api/resources${query.toString() ? `?${query}` : ""}`);
  },
};
