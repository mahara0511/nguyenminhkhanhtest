import google.generativeai as genai
from loader.vector_store import embed
def embed_text(text: str):
    res = embed(text)
    return res