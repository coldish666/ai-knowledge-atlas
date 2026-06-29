import re


def keywords(text: str) -> list[str]:
    tokens = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
    stop_words = {"the", "and", "for", "with", "this", "that", "一个", "我们", "以及", "可以", "知识"}
    result = []
    for token in tokens:
        if len(token) < 2 or token in stop_words:
            continue
        if token not in result:
            result.append(token)
    return result[:40]


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    chunks = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
    return chunks
