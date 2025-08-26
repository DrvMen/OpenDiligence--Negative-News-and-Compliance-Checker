# google_news.py
import requests
from bs4 import BeautifulSoup


def fetch_news_google(query):
    """
    Fetch latest news from Google News RSS feed
    """
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    res = requests.get(url, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.content, "xml")  # using XML parser for RSS feeds
    articles = []

    for item in soup.find_all("item")[:10]:
        articles.append({
            "title": item.title.text,
            "link": item.link.text,
            "source": item.source.text if item.source else "Google News",
            "pubDate": item.pubDate.text if item.pubDate else ""
        })

    return articles
