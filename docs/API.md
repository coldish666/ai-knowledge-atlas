# API Reference

## 基础

- `GET /health`：服务健康检查。

## 知识

- `GET /api/knowledge`：知识点列表，支持 `layer`、`tag`、`difficulty`、`category`。
- `GET /api/knowledge/{slug}`：知识点详情。
- `GET /api/knowledge/layers`：层级列表和数量。
- `GET /api/knowledge/tags`：标签列表。
- `GET /api/knowledge/{slug}/related`：相关知识。
- `GET /api/knowledge/{slug}/prerequisites`：前置知识。
- `GET /api/knowledge/{slug}/next`：后续知识。

## 权威资源

- `GET /api/knowledge/{slug}/resources`：获取某知识点的资源列表。
- `POST /api/knowledge/{slug}/resources`：为知识点新增资源。
- `GET /api/resources`：资源库列表，支持 `type`、`authority_level`、`difficulty`、`language`、`layer`、`q`。
- `GET /api/resources/recommended?slug=self-attention`：按推荐优先级返回某知识点前 6 条资源。
- `PUT /api/resources/{id}`：更新资源。
- `DELETE /api/resources/{id}`：删除资源。

资源只保存标题、原始 URL、来源、类型、权威等级、难度、语言、预计时间、简介和推荐理由，不复制原文或视频内容。

## 搜索

- `GET /api/search?q=Transformer`
- `GET /api/search?layer=4&difficulty=中等`

返回搜索结果和高亮片段。

## 图谱

- `GET /api/graph`：完整图谱。
- `GET /api/graph?layer=6`：按层级过滤。
- `GET /api/graph/{slug}/neighborhood`：某个节点邻域。

## RAG

- `POST /api/rag/upload`：multipart 上传 `file`，支持 `.md`、`.markdown`、`.txt`。
- `POST /api/rag/ask`：`{"question":"...", "scope":"all", "top_k":5}`。
- `GET /api/rag/documents`：上传文档列表。

## 导师

- `POST /api/tutor/explain`：解释知识点。
- `POST /api/tutor/compare`：比较两个知识点。
- `POST /api/tutor/code-example`：生成/解释代码示例。
- `POST /api/tutor/self-check`：生成自测问题。

## 设置

- `GET /api/settings`
- `PUT /api/settings`
