import { request } from "./client";

export const ragApi = {
  upload: (file: File) => {
    const body = new FormData();
    body.append("file", file);
    return request<{ id: number; original_name: string; chunks: number }>("/api/rag/upload", { method: "POST", body });
  },
  ask: (payload: { question: string; scope?: string; top_k?: number }) =>
    request<{ answer: string; citations: { source_label: string; content: string; source_type: string; knowledge_slug?: string }[] }>(
      "/api/rag/ask",
      { method: "POST", body: JSON.stringify(payload) },
    ),
  documents: () => request<{ id: number; original_name: string; uploaded_at: string }[]>("/api/rag/documents"),
};
