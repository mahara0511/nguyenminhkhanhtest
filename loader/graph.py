# graph_loader.py
from langgraph.graph import StateGraph, END
from loader.state import LoaderState
from loader.nodes.read_article import read_article
from loader.nodes.chunk_documents import chunk_documents
from loader.nodes.embed_chunks import embed_chunks
from loader.nodes.save_to_vectorstore import save_to_vectorstore

def build_loader_graph():
    graph = StateGraph(LoaderState)

    graph.add_node("read_article", read_article)
    graph.add_node("chunk_documents", chunk_documents)
    graph.add_node("embed_chunks", embed_chunks)
    graph.add_node("save_to_vectorstore", save_to_vectorstore)

    graph.set_entry_point("read_article")
    graph.add_edge("read_article", "chunk_documents")
    graph.add_edge("chunk_documents", "embed_chunks")
    graph.add_edge("embed_chunks", "save_to_vectorstore")
    graph.add_edge("save_to_vectorstore", END)

    return graph.compile()
