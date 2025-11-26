# run.py
from loader.graph import build_loader_graph
import glob
from dotenv import load_dotenv
load_dotenv()
def load_all():
    files = glob.glob("articles/*.md")
    graph = build_loader_graph()

    total = 0
    for f in files:
        res = graph.invoke({
            "file_paths": files,
            "current_file": f,
            "chunks": [],
            "embeddings": [],
            "metadata_list": [],
            "total_chunks": 0
        })
        total += res["total_chunks"]
        print(f"Loaded: {f} → {res['total_chunks']} chunks")

    print(f"\n=== DONE: Embedded {total} chunks ===")

if __name__ == "__main__":
    load_all()
