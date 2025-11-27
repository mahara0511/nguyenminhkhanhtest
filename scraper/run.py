# scraper/run.py
import json
import os
from scraper.graph import build_scraper_graph
import re

def safe_slug(text: str) -> str:
    # lowercase
    text = text.lower().strip()
    # replace slash or backslash with dash
    text = text.replace("/", "-").replace("\\", "-")
    # replace all invalid filename characters with dash
    text = re.sub(r"[^a-z0-9\-\_]+", "-", text)
    # remove duplicated dashes
    text = re.sub(r"-+", "-", text)
    # trim dash at edges
    text = text.strip("-")
    return text

def save_markdown_files(results):
    os.makedirs("articles", exist_ok=True)

    for item in results:
        slug = safe_slug(item["slug"])
        md = item["markdown"]

        filepath = os.path.join("articles", f"{slug}.md")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"[saved] {filepath}")


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
    with open("scraper/output.json", "w", encoding="utf-8") as f:
        json.dump(final_state["results"], f, ensure_ascii=False, indent=2)

    save_markdown_files(final_state["results"])
    print("\n[scraper] DONE.")
    print(f"Total articles scraped: {len(final_state['results'])}")

    return final_state


if __name__ == "__main__":
    run_scraper()
