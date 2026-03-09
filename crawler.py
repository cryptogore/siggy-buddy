import requests
from bs4 import BeautifulSoup

BASE="https://www.ritualfoundation.org"

pages=[
"/docs/overview/what-is-ritual"
]

text=""

for p in pages:

    url=BASE+p
    r=requests.get(url)

    soup=BeautifulSoup(r.text,"html.parser")

    text+=soup.get_text()

with open("ritual_docs_full.txt","w",encoding="utf-8") as f:
    f.write(text)

print("Docs downloaded")
