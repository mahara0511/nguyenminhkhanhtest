def read_article(state):
    article = state["article"]

    return {
        "markdown": article["markdown"],
        "title": article["title"],
        "slug": article["slug"],
        "url": article["url"],
        "id": article["id"]
    }