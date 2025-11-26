import google.generativeai as genai
import chromadb
import os   
# ============================
# GEMINI CONFIG
# ============================
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")

genai.configure(api_key=API_KEY)
# ============================
# CHROMA PERSISTENT DB
# ============================
client = chromadb.PersistentClient(path="./chroma_storage")

# Create or load the same collection for ALL operations
collection = client.get_or_create_collection(
    name="optibot_articles",
    metadata={"hnsw:space": "cosine"}
)

# ============================
# EMBEDDING (Gemini)
# ============================
def embed(text: str):
    res = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return res["embedding"]

# ============================
# VECTOR SEARCH
# ============================
def vector_search(query_embedding, k=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

# ============================
# ADD TO VECTORSTORE (LOADER)
# ============================
def add_to_vectorstore(chunk, embedding, metadata):
    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[metadata["id"]]
    )
