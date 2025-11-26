# assistant/state.py
from typing import List, TypedDict, Optional

class RAGState(TypedDict):
    query: str
    query_embedding: Optional[List[float]]
    retrieved_chunks: Optional[List[str]]
    prompt: Optional[str]
    answer: Optional[str]
