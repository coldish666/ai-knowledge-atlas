import type { ReactNode } from "react";

import SearchBar from "./SearchBar";
import Sidebar, { type PageKey } from "./Sidebar";
import type { KnowledgeLayer } from "../types/knowledge";

export default function Layout({
  page,
  setPage,
  layers,
  onLayer,
  onSearch,
  children,
}: {
  page: PageKey;
  setPage: (page: PageKey) => void;
  layers: KnowledgeLayer[];
  onLayer: (layer: number) => void;
  onSearch: (query: string) => void;
  children: ReactNode;
}) {
  return (
    <div className="app-shell">
      <Sidebar page={page} layers={layers} onNavigate={setPage} onLayer={onLayer} />
      <main className="content">
        <SearchBar onSearch={onSearch} />
        {children}
      </main>
    </div>
  );
}
