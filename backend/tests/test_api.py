import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_knowledge_atlas.db"
os.environ["DATA_DIR"] = "./test_data"
os.environ["UPLOAD_DIR"] = "./test_data/uploads"

db_path = Path("test_knowledge_atlas.db")
if db_path.exists():
    db_path.unlink()

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_knowledge_list_has_required_content_volume():
    response = client.get("/api/knowledge")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 60
    first = data["items"][0]
    assert first["title"]
    assert first["summary"]


def test_single_knowledge_node_is_complete():
    response = client.get("/api/knowledge/gradient-descent")
    assert response.status_code == 200
    node = response.json()
    assert node["definition"]
    assert node["intuition"]
    assert node["formulas"]
    assert node["code_example"]
    assert len(node["self_check_questions"]) >= 3


def test_search_finds_transformer():
    response = client.get("/api/search", params={"q": "Transformer"})
    assert response.status_code == 200
    results = response.json()
    assert any("Transformer" in item["title"] for item in results)


def test_graph_and_neighborhood():
    graph = client.get("/api/graph")
    assert graph.status_code == 200
    data = graph.json()
    assert len(data["nodes"]) >= 60
    assert len(data["edges"]) >= 50

    neighborhood = client.get("/api/graph/embedding/neighborhood")
    assert neighborhood.status_code == 200
    assert any(node["id"] == "embedding" for node in neighborhood.json()["nodes"])


def test_resources_api_has_seeded_authoritative_links():
    resources = client.get("/api/resources")
    assert resources.status_code == 200
    data = resources.json()
    assert data["total"] >= 80
    first = data["items"][0]
    assert first["url"].startswith("http")
    assert first["authority_level"] in {"S", "A", "B", "C"}

    node_resources = client.get("/api/knowledge/self-attention/resources")
    assert node_resources.status_code == 200
    assert any(item["resource_type"] in {"paper", "blog", "book"} for item in node_resources.json())

    recommended = client.get("/api/resources/recommended", params={"slug": "self-attention"})
    assert recommended.status_code == 200
    assert 1 <= len(recommended.json()) <= 6

    official = client.get("/api/resources", params={"type": "official_doc", "authority_level": "S"})
    assert official.status_code == 200
    assert official.json()["total"] >= 10


def test_rag_upload_and_ask_returns_citations():
    files = {"file": ("atlas.md", b"# Transformer\n\nSelf-Attention connects tokens with citations.", "text/markdown")}
    upload = client.post("/api/rag/upload", files=files)
    assert upload.status_code == 200
    assert upload.json()["chunks"] >= 1

    ask = client.post("/api/rag/ask", json={"question": "What connects tokens?", "top_k": 3})
    assert ask.status_code == 200
    data = ask.json()
    assert data["answer"]
    assert data["citations"]


def test_tutor_mock_explain():
    response = client.post("/api/tutor/explain", json={"topic": "反向传播", "style": "直觉版"})
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "mock"
    assert data["answer"]
