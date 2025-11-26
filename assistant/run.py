# run.py
from assistant.graph import build_assistant_graph
from dotenv import load_dotenv
load_dotenv()
graph = build_assistant_graph()

while True:
    q = input("Ask: ")
    out = graph.invoke({"query": q})
    print("\nANSWER:\n", out["answer"])
    print("\n-----------------------------------------\n")
