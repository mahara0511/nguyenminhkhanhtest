# scraper/nodes/clean_html.py
from bs4 import BeautifulSoup

def clean_html(state):
    article = state["current_article"]
    if not article:
        return state

    html = article["body"]
    soup = BeautifulSoup(html, "lxml")

    # remove scripts, styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    # remove empty tags
    for tag in soup.find_all(["p", "div"]):
        if not tag.text.strip():
            tag.decompose()

    for tag in soup.find_all():
        tag.attrs = {k:v for k,v in tag.attrs.items() if k in ["href", "src"]}

    cleaned_html = str(soup)
    return {"cleaned_html": cleaned_html}
