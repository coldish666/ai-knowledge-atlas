import { FormEvent, useState } from "react";

import { ragApi } from "../api/rag";

export default function RagPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadInfo, setUploadInfo] = useState("");
  const [question, setQuestion] = useState("Transformer 和 Self-Attention 的关系是什么？");
  const [scope, setScope] = useState("all");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<{ source_label: string; content: string; source_type: string }[]>([]);

  async function upload(event: FormEvent) {
    event.preventDefault();
    if (!file) return;
    const result = await ragApi.upload(file);
    setUploadInfo(`${result.original_name} 已上传，切分为 ${result.chunks} 个片段`);
  }

  async function ask(event: FormEvent) {
    event.preventDefault();
    const result = await ragApi.ask({ question, scope, top_k: 5 });
    setAnswer(result.answer);
    setCitations(result.citations);
  }

  return (
    <section className="page-stack">
      <header className="page-header"><h1>RAG 资料问答</h1></header>
      <div className="two-column">
        <form className="panel form-grid" onSubmit={upload}>
          <h2>上传资料</h2>
          <input type="file" accept=".md,.markdown,.txt" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          <button type="submit">上传并切分</button>
          {uploadInfo && <p>{uploadInfo}</p>}
        </form>
        <form className="panel form-grid" onSubmit={ask}>
          <h2>围绕内置知识或上传资料提问</h2>
          <select value={scope} onChange={(event) => setScope(event.target.value)}>
            <option value="all">内置知识 + 上传资料</option>
            <option value="knowledge">仅内置知识</option>
            <option value="uploads">仅上传资料</option>
          </select>
          <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
          <button type="submit">检索并回答</button>
        </form>
      </div>
      {answer && (
        <section className="panel">
          <h2>Mock RAG 回答</h2>
          <p className="preline">{answer}</p>
          <h3>引用片段</h3>
          {citations.map((citation) => (
            <blockquote key={`${citation.source_label}-${citation.content.slice(0, 20)}`}>
              <strong>{citation.source_type} · {citation.source_label}</strong>
              <p>{citation.content}</p>
            </blockquote>
          ))}
        </section>
      )}
    </section>
  );
}
