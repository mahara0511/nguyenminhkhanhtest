# scraper/nodes/to_markdown.py
import html2text
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def to_markdown(state):
    article = state["current_article"]
    cleaned = state["cleaned_html"]

    if not article:
        return {}

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.body_width = 0

    md = converter.handle(cleaned).strip()

    # Create stable slug with ID + sanitized title
    article_id = article["id"]
    title = article["title"]
    html_url = article["html_url"]

    slug = f"{article_id}-{slugify(title)}"

    result = {
        "id": article_id,
        "title": title,
        "slug": slug,
        "url": html_url,        # <-- Quan trọng để bot trả link
        "markdown": md,
    }

    results = state.get("results", [])
    results.append(result)

    return {"results": results}
