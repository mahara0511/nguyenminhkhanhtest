# assistant/nodes/embed_query.py
from loader.vector_store import embed
from assistant.state import RAGState

def embed_query(state: RAGState):
    return {
        "query_embedding": embed(state["query"])
    }
