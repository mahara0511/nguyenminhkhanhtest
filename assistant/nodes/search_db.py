# assistant/nodes/search_db.py
from loader.vector_store import vector_search

def search_db(state):
    res = vector_search(state["query_embedding"])
    chunks = res["documents"][0]       # nội dung
    metas = res["metadatas"][0]        # chứa url/title/slug/article_id
    return {
        "retrieved_chunks": chunks,
        "retrieved_metadata": metas
    }
