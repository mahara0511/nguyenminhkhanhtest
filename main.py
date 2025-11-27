import json
import hashlib
import os
from datetime import datetime
from scraper.graph import build_scraper_graph
from uploader import upload_delta

STATE_FILE = "state.json"
SCRAPE_OUTPUT_FILE = "output.json"
RUN_LOG = "last_run_log.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(sta0te):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def compute_hash(md_text):
    return hashlib.sha256(md_text.encode("utf-8")).hexdigest()


def detect_changes(articles, prev_state):
    added = []
    updated = []
    skipped = []

    new_state = {}

    for art in articles:
        article_id = str(art["id"])
        content = art["markdown"]
        slug = art["slug"]
        last_modified = art.get("updated_at") or art.get("modified") or None

        h = compute_hash(content)

        new_state[article_id] = {
            "hash": h,
            "last_modified": last_modified,
            "slug": slug,
            "url": art["url"]
        }

        if article_id not in prev_state:
            added.append(art)

        else:
            if h != prev_state[article_id]["hash"]:
                updated.append(art)
            else:
                skipped.append(art)

    return added, updated, skipped, new_state


def write_run_log(added, updated, skipped):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "added": len(added),
        "updated": len(updated),
        "skipped": len(skipped),
        "details": {
            "added_ids": [a["id"] for a in added],
            "updated_ids": [u["id"] for u in updated],
            "skipped_ids": [s["id"] for s in skipped]
        }
    }

    with open(RUN_LOG, "w") as f:
        json.dump(log, f, indent=2)

    print("\n=== Run Summary ===")
    print(json.dumps(log, indent=2))
    print("===================")

    return log


def main():
    print("Starting daily scraper job...")

    graph = build_scraper_graph()
    result = graph.invoke({
        "page_url": "https://support.optisigns.com/api/v2/help_center/en-us/articles.json",
        "results": [],
        "next_page": None
    })

    articles = result["results"]

    # Save scrape output
    with open(SCRAPE_OUTPUT_FILE, "w") as f:
        json.dump(articles, f, indent=2)

    prev_state = load_state()

    added, updated, skipped, new_state = detect_changes(articles, prev_state)

    print(f"Added: {len(added)}")
    print(f"Updated: {len(updated)}")
    print(f"Skipped: {len(skipped)}")

    # Upload only the delta
    delta = added + updated
    if delta:
        upload_delta(delta)
    else:
        print("No changes detected → Nothing to upload.")

    # Save new state
    save_state(new_state)

    # Save run log for DigitalOcean to display
    write_run_log(added, updated, skipped)

    print("Job completed.")


if __name__ == "__main__":
    main()
