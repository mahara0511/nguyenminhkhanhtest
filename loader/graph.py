# graph_loader.py
from langgraph.graph import StateGraph, END
from loader.state import LoaderState
from loader.nodes.read_file import read_file
from loader.nodes.chunk_documents import chunk_documents
from loader.nodes.embed_chunks import embed_chunks
from loader.nodes.save_to_vectorstore import save_to_vectorstore

def build_loader_graph():
    graph = StateGraph(LoaderState)

    graph.add_node("read_file", read_file)
    graph.add_node("chunk_documents", chunk_documents)
    graph.add_node("embed_chunks", embed_chunks)
    graph.add_node("save_to_vectorstore", save_to_vectorstore)

    graph.set_entry_point("read_file")
    graph.add_edge("read_file", "chunk_documents")
    graph.add_edge("chunk_documents", "embed_chunks")
    graph.add_edge("embed_chunks", "save_to_vectorstore")
    graph.add_edge("save_to_vectorstore", END)

    return graph.compile()
