import { FormEvent, useState } from "react";

import { api } from "../api/client";

export default function TutorPage() {
  const [topic, setTopic] = useState("我不懂反向传播");
  const [style, setStyle] = useState("直觉版");
  const [compareRight, setCompareRight] = useState("自动求导");
  const [answer, setAnswer] = useState("");
  const [references, setReferences] = useState<string[]>([]);

  async function explain(event: FormEvent) {
    event.preventDefault();
    const result = await api.explain({ topic, style });
    setAnswer(result.answer);
    setReferences((result as any).references || []);
  }

  async function compare() {
    const result = await api.compare({ left: topic, right: compareRight, style });
    setAnswer(result.answer);
    setReferences(result.references || []);
  }

  async function code() {
    const result = await api.codeExample({ topic });
    setAnswer(result.answer);
    setReferences(result.references || []);
  }

  async function selfCheck() {
    const result = await api.selfCheck({ topic });
    setAnswer(result.answer);
    setReferences(result.references || []);
  }

  return (
    <section className="page-stack">
      <header className="page-header"><h1>AI 知识讲解导师</h1></header>
      <form className="panel form-grid" onSubmit={explain}>
        <input value={topic} onChange={(event) => setTopic(event.target.value)} placeholder="输入知识点或困惑" />
        <select value={style} onChange={(event) => setStyle(event.target.value)}>
          {["直觉版", "数学版", "代码版", "考试版", "项目应用版"].map((item) => <option key={item}>{item}</option>)}
        </select>
        <input value={compareRight} onChange={(event) => setCompareRight(event.target.value)} placeholder="用于比较的第二个知识点" />
        <div className="button-group">
          <button type="submit">生成解释</button>
          <button type="button" onClick={compare}>比较知识点</button>
          <button type="button" onClick={code}>代码示例</button>
          <button type="button" onClick={selfCheck}>自测问题</button>
        </div>
      </form>
      {answer && (
        <section className="panel">
          <h2>Mock 导师回复</h2>
          <p className="preline">{answer}</p>
          {references.length > 0 && <p className="muted">引用知识点：{references.join("、")}</p>}
        </section>
      )}
    </section>
  );
}
