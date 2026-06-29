import { FormEvent, useState } from "react";

export default function SearchBar({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState("");

  function submit(event: FormEvent) {
    event.preventDefault();
    onSearch(query.trim());
  }

  return (
    <form className="search-bar" onSubmit={submit}>
      <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索 Transformer、梯度下降、RAG、Agent..." />
      <button type="submit">搜索</button>
    </form>
  );
}
