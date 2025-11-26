from loader.vector_store import add_to_vectorstore
import os

def save_to_vectorstore(state):
    """
    Save chunks + embeddings to vector store.

    Required:
    - state["current_file"]
    - state["chunks"]
    - state["embeddings"]
    """
    file_path = state["current_file"]
    slug = os.path.splitext(os.path.basename(file_path))[0]   # NEW — create slug properly

    chunks = state["chunks"]
    embeddings = state["embeddings"]

    print(f"[VectorStore] Saving {len(chunks)} chunks for {slug}")

    for i, chunk in enumerate(chunks):
        chunk_id = f"{slug}-{i}"

        metadata = {
            "id": chunk_id,
            "slug": slug,
            "file": file_path,
            "chunk_index": i,
        }

        add_to_vectorstore(chunk, embeddings[i], metadata)

    return {"saved": slug, "total_chunks": len(chunks)}
