import requests
from bs4 import BeautifulSoup

def fetch_url_metadata(url: str) -> dict:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.title.string if soup.title else None
    description = soup.find("meta", attrs={"name": "description"})
    description = description["content"] if description else None

    return {
        "title": title,
        "description": description,
    }
