import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ritualfoundation.org"

pages = [
"/docs/overview/what-is-ritual",
"/docs/overview/architecture",
"/docs/overview/vision",
"/docs/developers",
"/docs/tutorials"
]

all_text = ""

for page in pages:

    url = BASE_URL + page

    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    text = soup.get_text()

    all_text += text + "\n\n"

with open("ritual_docs_full.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Ritual docs downloaded.")