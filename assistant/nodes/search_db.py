# assistant/nodes/search_db.py
from loader.vector_store import vector_search

def search_db(state):
    res = vector_search(state["query_embedding"])
    documents = res["documents"][0]  # list of chunks
    return {
        "retrieved_chunks": documents
    }
