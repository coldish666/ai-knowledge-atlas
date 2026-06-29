import { useEffect, useState } from "react";

import { knowledgeApi } from "./api/knowledge";
import Layout from "./components/Layout";
import type { PageKey } from "./components/Sidebar";
import GraphView from "./pages/GraphView";
import Home from "./pages/Home";
import KnowledgeDetail from "./pages/KnowledgeDetail";
import KnowledgeIndex from "./pages/KnowledgeIndex";
import KnowledgeTree from "./pages/KnowledgeTree";
import RagPage from "./pages/RagPage";
import ResourceLibrary from "./pages/ResourceLibrary";
import SearchPage from "./pages/SearchPage";
import Settings from "./pages/Settings";
import TutorPage from "./pages/TutorPage";
import type { KnowledgeLayer, KnowledgeSummary } from "./types/knowledge";

export default function App() {
  const [page, setPage] = useState<PageKey>("home");
  const [layers, setLayers] = useState<KnowledgeLayer[]>([]);
  const [featured, setFeatured] = useState<KnowledgeSummary[]>([]);
  const [selectedLayer, setSelectedLayer] = useState<number | undefined>(undefined);
  const [selectedSlug, setSelectedSlug] = useState("gradient-descent");
  const [query, setQuery] = useState("");

  useEffect(() => {
    knowledgeApi.layers().then(setLayers);
    knowledgeApi.list().then((data) => setFeatured(data.items));
  }, []);

  function openKnowledge(slug: string) {
    setSelectedSlug(slug);
    setPage("detail");
  }

  function openLayer(layer: number) {
    setSelectedLayer(layer);
    setPage("index");
  }

  function search(nextQuery: string) {
    setQuery(nextQuery);
    setPage("search");
  }

  return (
    <Layout page={page} setPage={setPage} layers={layers} onLayer={openLayer} onSearch={search}>
      {page === "home" && (
        <Home
          layers={layers}
          featured={featured}
          onOpen={openKnowledge}
          onLayer={openLayer}
          onNavigate={setPage}
          onSearch={search}
        />
      )}
      {page === "tree" && <KnowledgeTree layers={layers} nodes={featured} onOpen={openKnowledge} />}
      {page === "index" && <KnowledgeIndex selectedLayer={selectedLayer} layers={layers} onOpen={openKnowledge} />}
      {page === "resources" && <ResourceLibrary layers={layers} onOpen={openKnowledge} />}
      {page === "detail" && <KnowledgeDetail slug={selectedSlug} onOpen={openKnowledge} onTree={() => setPage("tree")} />}
      {page === "graph" && <GraphView layers={layers} onOpen={openKnowledge} />}
      {page === "search" && <SearchPage query={query} layers={layers} onOpen={openKnowledge} />}
      {page === "rag" && <RagPage />}
      {page === "tutor" && <TutorPage />}
      {page === "settings" && <Settings />}
    </Layout>
  );
}
