import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

catalog = []

# scrape multiple pages
for start in range(0, 120, 12):

    url = f"https://www.shl.com/products/product-catalog/?start={start}&type=1"

    print("Scraping:", url)

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:

        text = link.get_text(strip=True)
        href = link.get("href")

        if text and href:

            if "/products/product-catalog/view/" in href and not text.isdigit():

                item = {
                    "name": text,
                    "url": href if href.startswith("http") else "https://www.shl.com" + href,
                    "test_type": (
    "Technical" if any(word in text.lower() for word in [
        "java", ".net", "python", "coding",
        "technical", "sql", "developer"
    ])
    else "Personality" if any(word in text.lower() for word in [
        "opq", "personality", "behavioral",
        "motivation"
    ])
    else "Cognitive" if any(word in text.lower() for word in [
        "cognitive", "ability", "verify",
        "reasoning", "aptitude"
    ])
    else "General"
),
                    "skills": []
                }

                catalog.append(item)

    time.sleep(1)

# remove duplicates
unique_catalog = []

seen = set()

for item in catalog:

    if item["url"] not in seen:

        unique_catalog.append(item)
        seen.add(item["url"])

# save json
with open("catalog.json", "w") as file:

    json.dump(unique_catalog, file, indent=4)

print("Saved", len(unique_catalog), "assessments.")