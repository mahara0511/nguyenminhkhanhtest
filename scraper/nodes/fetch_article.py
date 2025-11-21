# scraper/nodes/fetch_article.py

def fetch_article(state):
    if not state["article_list"]:
        print("[article] No more articles.")
        return {"current_article": None}

    article = state["article_list"][0]

    # Pop one article out of the list
    remaining = state["article_list"][1:]

    return {
        "current_article": article,
        "article_list": remaining
    }
