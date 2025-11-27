# loader/run.py
from loader.graph import build_loader_graph
from dotenv import load_dotenv
import json

load_dotenv()

def load_all():

    # ---- Load articles from scraper/output.json ----
    with open("scraper/output.json", "r") as f:
        articles = json.load(f)

    graph = build_loader_graph()

    total = 0
    for article in articles:
        res = graph.invoke({
            "article": article,
            "chunks": [],
            "embeddings": [],
            "metadata_list": [],
            "total_chunks": 0
        })
        total += res["total_chunks"]
        print(f"Loaded: {article['slug']} → {res['total_chunks']} chunks")

    print(f"\n=== DONE: Embedded {total} chunks ===")

if __name__ == "__main__":
    load_all()
