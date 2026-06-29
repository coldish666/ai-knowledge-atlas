import { FormEvent, useEffect, useState } from "react";

import { api } from "../api/client";
import type { Settings as SettingsData } from "../types/knowledge";

export default function Settings() {
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [saved, setSaved] = useState("");

  useEffect(() => { api.settings().then(setSettings); }, []);
  if (!settings) return <section className="panel">加载设置...</section>;

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!settings) return;
    const next = await api.updateSettings(settings);
    setSettings(next);
    setSaved("设置已保存");
  }

  return (
    <section className="page-stack">
      <header className="page-header"><h1>设置</h1></header>
      <form className="panel form-grid" onSubmit={submit}>
        <label>用户名称<input value={settings.user_name} onChange={(event) => setSettings({ ...settings, user_name: event.target.value })} /></label>
        <label>默认解释风格<select value={settings.preferred_style} onChange={(event) => setSettings({ ...settings, preferred_style: event.target.value })}>
          {["直觉版", "数学版", "代码版", "考试版", "项目应用版"].map((item) => <option key={item}>{item}</option>)}
        </select></label>
        <label>LLM Provider<select value={settings.llm_provider} onChange={(event) => setSettings({ ...settings, llm_provider: event.target.value })}>
          <option value="mock">mock</option>
          <option value="openai-compatible">openai-compatible</option>
        </select></label>
        <label>API Base URL<input value={settings.api_base_url} onChange={(event) => setSettings({ ...settings, api_base_url: event.target.value })} /></label>
        <label>RAG 片段数<input type="number" value={settings.max_rag_chunks} onChange={(event) => setSettings({ ...settings, max_rag_chunks: Number(event.target.value) })} /></label>
        <label className="inline-check"><input type="checkbox" checked={settings.ai_enabled} onChange={(event) => setSettings({ ...settings, ai_enabled: event.target.checked })} /> 启用 AI 功能</label>
        <button type="submit">保存设置</button>
        {saved && <p>{saved}</p>}
      </form>
    </section>
  );
}
