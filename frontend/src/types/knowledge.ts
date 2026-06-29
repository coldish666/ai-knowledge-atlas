export interface KnowledgeSummary {
  id: number;
  slug: string;
  title: string;
  layer: number;
  category: string;
  difficulty: string;
  summary: string;
  tags: string[];
  prerequisites: string[];
  next_topics: string[];
  related_topics: string[];
}

export interface KnowledgeNode extends KnowledgeSummary {
  definition: string;
  intuition: string;
  why_it_matters: string;
  math_form: string;
  formulas: string[];
  code_example: string;
  applications: string[];
  misconceptions: string[];
  prerequisites: string[];
  next_topics: string[];
  related_topics: string[];
  recommended_resources: string[];
  self_check_questions: string[];
  extension_questions: string[];
}

export interface KnowledgeList {
  items: KnowledgeSummary[];
  total: number;
}

export interface KnowledgeResource {
  id: number;
  knowledge_slug: string;
  title: string;
  url: string;
  source: string;
  resource_type: string;
  authority_level: "S" | "A" | "B" | "C" | string;
  difficulty: "beginner" | "intermediate" | "advanced" | string;
  language: "en" | "zh" | "other" | string;
  estimated_time: string;
  description: string;
  why_recommended: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface ResourceList {
  items: KnowledgeResource[];
  total: number;
}

export interface KnowledgeLayer {
  layer: number;
  name: string;
  count: number;
}

export interface GraphNode {
  id: string;
  title: string;
  layer: number;
  category: string;
  difficulty: string;
  tags: string[];
}

export interface GraphEdge {
  source: string;
  target: string;
  relation_type: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface Settings {
  id: number;
  user_name: string;
  preferred_style: string;
  llm_provider: string;
  api_base_url: string;
  ai_enabled: boolean;
  max_rag_chunks: number;
}
