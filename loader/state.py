from typing import List, TypedDict, Optional, Dict

class LoaderState(TypedDict):
    file_paths: List[str]
    current_file: Optional[str]
    file_text: Optional[str]
    chunks: List[str]
    embeddings: List[List[float]]
    metadata_list: List[Dict]
    total_chunks: int
