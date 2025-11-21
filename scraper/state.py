# scraper/state.py

from typing import TypedDict, List, Dict

class ScraperState(TypedDict, total=False):
    page_url: str
    article_list: List[Dict]
    current_article: Dict
    cleaned_html: str
    markdown: str
    results: List[Dict]   
