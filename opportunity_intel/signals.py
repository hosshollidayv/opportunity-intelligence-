import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class RawSignal:
    source_url: str
    retrieved_at_iso: str
    title: str
    excerpt: str
    raw_text: str

def fetch_signal(signal_url):
    response = requests.get(signal_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string if soup.title else None
    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'] if meta_description else None

    raw_text = soup.get_text()
    excerpt = raw_text[:2000]  # Get the first 2000 characters of visible text

    return RawSignal(
        source_url=signal_url,
        retrieved_at_iso=datetime.utcnow().isoformat(),
        title=title,
        excerpt=excerpt,
        raw_text=raw_text
    )
