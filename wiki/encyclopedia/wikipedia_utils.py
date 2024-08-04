# encyclopedia/wikipedia_utils.py

import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def fetch_wikipedia_entries(keyword="Nigeria"):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": keyword,
        "format": "json"
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    return data["query"]["search"] if "query" in data else []

def fetch_wikipedia_page(title):
    params = {
        "action": "query",
        "prop": "extracts|pageimages",
        "exintro": True,
        "explaintext": True,
        "titles": title,
        "format": "json",
        "piprop": "original",
        "pithumbsize": 500
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    pages = data["query"]["pages"]
    page_id = next(iter(pages))
    return pages[page_id] if page_id != "-1" else None

def import_wikipedia_entries():
    keywords = ["Nigeria", "Nigerian culture", "Nigerian history", "Nigerian geography"]
    for keyword in keywords:
        entries = fetch_wikipedia_entries(keyword=keyword)
        for entry in entries:
            page = fetch_wikipedia_page(entry["title"])
            if page:
                title = page["title"]
                content = page.get("extract", "")
                image = page["thumbnail"]["source"] if "thumbnail" in page else None
                print(f"Importing: {title}, Content length: {len(content)}, Image: {image}")
                save_entry(title=title, content=content, image=image)
            else:
                print(f"Failed to fetch page for: {entry['title']}")


def save_entry(title, content, image):
    from .models import Entry  # Import here to avoid circular import issues

    # Check if the entry already exists
    if Entry.objects.filter(title=title).exists():
        print(f"Entry '{title}' already exists. Skipping.")
    else:
        entry = Entry(title=title, content=content)
        if image:
            entry.image = image
        entry.save()
        print(f"Created new entry: {title}")
