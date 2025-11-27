import hashlib
from loader.vector_store import add_to_vectorstore, embed
from scraper.run import run_scraper
from scraper.utils import load_hash_db, save_hash_db

HASH_FILE = "scraper_hash.json"


def calc_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_daily_job() -> None:
    print("== Running daily scraper job ==")

    old_hash = load_hash_db(HASH_FILE)
    new_hash = {}

    # Re-scrape all articles using existing scraper graph
    final_state = run_scraper()
    scraped = final_state["results"]  # [{id, url, title, markdown}, ...]

    added, updated, skipped = 0, 0, 0

    for art in scraped:
        article_id = str(art["id"])
        content = art["markdown"]
        new_hash[article_id] = calc_hash(content)

        if article_id not in old_hash:
            print(f"[ADD] {article_id}")
            emb = embed(content)
            metadata = {
                "id": article_id,
                "url": art.get("url", ""),
                "title": art.get("title", ""),
                "hash": new_hash[article_id],
            }
            add_to_vectorstore(content, emb, metadata)
            added += 1

        elif old_hash[article_id] != new_hash[article_id]:
            print(f"[UPDATE] {article_id}")
            emb = embed(content)
            metadata = {
                "id": article_id,
                "url": art.get("url", ""),
                "title": art.get("title", ""),
                "hash": new_hash[article_id],
            }
            add_to_vectorstore(content, emb, metadata)
            updated += 1

        else:
            skipped += 1

    save_hash_db(HASH_FILE, new_hash)

    print("=== DAILY JOB RESULT ===")
    print("Added:   ", added)
    print("Updated: ", updated)
    print("Skipped: ", skipped)


if __name__ == "__main__":
    run_daily_job()
