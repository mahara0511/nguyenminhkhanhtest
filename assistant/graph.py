# assistant/graph.py
from langgraph.graph import StateGraph, END
from assistant.state import RAGState
from assistant.nodes.embed_query import embed_query
from assistant.nodes.search_db import search_db
from assistant.nodes.build_prompt import build_prompt
from assistant.nodes.llm_answer import llm_answer
from assistant.nodes.format_output import format_output

def build_assistant_graph():
    graph = StateGraph(RAGState)

    graph.add_node("embed_query", embed_query)
    graph.add_node("search_db", search_db)
    graph.add_node("build_prompt", build_prompt)
    graph.add_node("llm_answer", llm_answer)
    graph.add_node("format_output", format_output)

    # Define flow
    graph.set_entry_point("embed_query")
    graph.add_edge("embed_query", "search_db")
    graph.add_edge("search_db", "build_prompt")
    graph.add_edge("build_prompt", "llm_answer")
    graph.add_edge("llm_answer", "format_output")
    graph.add_edge("format_output", END)

    return graph.compile()
