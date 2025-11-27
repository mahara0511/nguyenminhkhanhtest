# nodes/chunk_documents.py
from loader.chunker import chunk_markdown

def chunk_documents(state):
    chunks = chunk_markdown(state["markdown"])
    return {"chunks": chunks}
