from typing import List, TypedDict, Optional, Dict, Any

class LoaderState(TypedDict):
    article: Dict[str, Any]      # object trong output.json
    markdown: str                # nội dung markdown từ JSON
    title: str
    slug: str
    url: str
    id: int

    chunks: List[str]
    embeddings: List[List[float]]
    metadata_list: List[Dict]
    total_chunks: int
