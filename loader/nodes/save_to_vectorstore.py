# loader/nodes/save_to_vectorstore.py
from loader.vector_store import add_to_vectorstore

def save_to_vectorstore(state):
    article_id = state["id"]
    title = state["title"]
    slug = state["slug"]
    url = state["url"]

    for idx, (chunk, emb) in enumerate(zip(state["chunks"], state["embeddings"])):
        metadata = {
            "article_id": article_id,
            "title": title,
            "slug": slug,
            "url": url,              # 🔥 để assistant trả link
            "id": f"{article_id}-{idx}",
        }

        add_to_vectorstore(chunk, emb, metadata)

    return {"total_chunks": len(state["chunks"])}
