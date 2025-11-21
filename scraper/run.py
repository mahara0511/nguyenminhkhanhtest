# scraper/run.py
import json
from scraper.graph import build_scraper_graph

def run_scraper():
    graph = build_scraper_graph()
    initial_state = {
        "page_url": "https://support.optisigns.com/api/v2/help_center/en-us/articles.json",
        "results": []
    }

    final_state = graph.invoke(
        initial_state,
        config={
            "recursion_limit": 200,          
            "timeout": None                  
        }
    )
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(final_state, f, ensure_ascii=False, indent=2)
    print("\n[scraper] DONE.")
    print(f"Total articles scraped: {len(final_state['results'])}")

    return final_state


if __name__ == "__main__":
    run_scraper()
