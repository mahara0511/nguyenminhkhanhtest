# scraper/nodes/to_markdown.py
import html2text

def to_markdown(state):
    cleaned = state["cleaned_html"]
    article = state["current_article"]

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.body_width = 0

    md = converter.handle(cleaned).strip()

    result = {
        "title": article["title"],
        "slug": article["title"].lower().replace(" ", "-"),
        "markdown": md,
    }

    # store result into results list
    results = state.get("results", [])
    results.append(result)

    return {"results": results}
