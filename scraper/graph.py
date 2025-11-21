# scraper/graph.py
from langgraph.graph import StateGraph, END
from scraper.state import ScraperState

from scraper.nodes.fetch_list import fetch_list
from scraper.nodes.fetch_article import fetch_article
from scraper.nodes.clean_html import clean_html
from scraper.nodes.to_markdown import to_markdown

def build_scraper_graph():
    graph = StateGraph(ScraperState)

    graph.add_node("fetch_list", fetch_list)
    graph.add_node("fetch_article", fetch_article)
    graph.add_node("clean", clean_html)
    graph.add_node("md", to_markdown)

    # Entry point
    graph.set_entry_point("fetch_list")

    # Flow
    graph.add_edge("fetch_list", "fetch_article")
    graph.add_edge("fetch_article", "clean")
    graph.add_edge("clean", "md")

    # After markdown: loop back to "fetch_article" if more
    graph.add_conditional_edges(
        "md",
        lambda state: "fetch_article" if state["article_list"] else END,
        {
            "fetch_article": "fetch_article",
            END: END
        }
    )

    return graph.compile()
