import type { Settings } from "../types/knowledge";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = options.body instanceof FormData ? undefined : { "Content-Type": "application/json" };
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers: { ...headers, ...options.headers } });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json();
}

export const api = {
  explain: (payload: { topic: string; style?: string }) =>
    request<{ answer: string; provider: string; references: string[] }>("/api/tutor/explain", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  compare: (payload: { left: string; right: string; style?: string }) =>
    request<{ answer: string; provider: string; references: string[] }>("/api/tutor/compare", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  codeExample: (payload: { topic: string; language?: string }) =>
    request<{ answer: string; provider: string; references: string[] }>("/api/tutor/code-example", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  selfCheck: (payload: { topic: string; difficulty?: string }) =>
    request<{ answer: string; provider: string; references: string[] }>("/api/tutor/self-check", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  settings: () => request<Settings>("/api/settings"),
  updateSettings: (payload: Partial<Settings>) =>
    request<Settings>("/api/settings", { method: "PUT", body: JSON.stringify(payload) }),
};
