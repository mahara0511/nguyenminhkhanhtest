import os
import hashlib
import json

# --- import pipeline ---
from scraper.run import run_scraper       # scrape + save markdown
from loader.run import load_all           # load markdown → chunk → embed → chroma


HASH_FILE = "article_hashes.json"


def load_hashes():
    if not os.path.exists(HASH_FILE):
        return {}
    with open(HASH_FILE, "r") as f:
        return json.load(f)


def save_hashes(h):
    with open(HASH_FILE, "w") as f:
        json.dump(h, f, indent=2)


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def detect_delta(articles_dir="articles"):
    old = load_hashes()
    new = {}
    added, updated, skipped = [], [], []

    for file in os.listdir(articles_dir):
        if not file.endswith(".md"):
            continue

        full = os.path.join(articles_dir, file)
        h = file_hash(full)

        new[file] = h

        if file not in old:
            added.append(file)
        elif old[file] != h:
            updated.append(file)
        else:
            skipped.append(file)

    save_hashes(new)

    return added, updated, skipped


def main():
    print("\n================ DAILY JOB START ======================")

    print("STEP 1 — Scraping fresh articles...")
    run_scraper()

    print("\nSTEP 2 — Detecting new & updated files...")
    added, updated, skipped = detect_delta()

    print(f"  Added:   {added}")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")

    print("\nSTEP 3 — Processing into vectorstore...")
    load_all()

    print("\n================ DAILY JOB DONE ======================\n")


if __name__ == "__main__":
    main()
