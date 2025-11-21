# scraper/nodes/fetch_list.py
import requests

def fetch_list(state):
    url = state.get("page_url")
    print(f"[list] Fetching page: {url}")

    res = requests.get(url)
    res.raise_for_status()

    data = res.json()
    new_articles = data.get("articles", [])
    
    # Filter drafts or empty
    articles = [a for a in new_articles if a.get("body") and not a.get("draft")]

    return {
        "article_list": articles,
        "next_page": data.get("next_page")
    }
