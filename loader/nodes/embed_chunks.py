# nodes/embed_chunks.py
from loader.embeddings import embed_text

def embed_chunks(state):
    embeddings = [embed_text(c) for c in state["chunks"]]
    return {"embeddings": embeddings}
